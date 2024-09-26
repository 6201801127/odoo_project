odoo.define('kw_skill_assessment.skill_report', function (require) {
    "use strict";
    
    var core = require('web.core');
    var framework = require('web.framework');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var ActionManager = require('web.ActionManager');
    var view_registry = require('web.view_registry');
    var Widget = require('web.Widget');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var QWeb = core.qweb;
    
    var _t = core._t;
    var _lt = core._lt;

    
    var SkillReportView = AbstractAction.extend(ControlPanelMixin, {
        init: function(parent, value) {
            this._super(parent, value);
            var skill_master = [];
            var self = this;
            if (value.tag == 'kw_skill_assessment.skill_report') {
                self._rpc({
                    route: '/skill-report',
                }, []).then(function(result){
                    self.skill_master = result
                    console.log("result :",result);
                    self.render();
                    self.href = window.location.href;
                    self.render_Datatable();
                });
            }
        },
        events :{
            "click .buttons-excel": function(){
                $('#empModal').find('table').table2excel({
                    exclude:".noExl",
                    name:"Worksheet Name",
                    filename:"Organisation-Skill-Report",
                    fileext:".xls",
                    preserveColors:true
                })
            } 
        },
        render_Datatable: function()
        {
            var skill_report_table = $('#skill_report').DataTable({
                dom: 'Bfrtip',
                buttons: [
                    'excel',
                    // {
                    //     extend: 'pdf',
                    //     footer: 'true',
                    //     orientation: 'landscape',
                    //     text: 'PDF',
                    //     exportOptions: {
                    //         modifier: {
                    //             selected: true
                    //         }
                    //     }
                    // },
                ],
                paging:         false,
                "info":     false,
                "order": [[ 1, 'desc' ], [ 0, 'asc' ]], 
                "footerCallback": function ( row, data, start, end, display ) {
                    var api = this.api(), data;
                    // converting to interger to find total
                    var intVal = function ( i ) {
                      if(typeof i !== 'number'){
                        i = $(i).eq(0).html() || '';
                        i = strip_tags(i);
                        i = i.replace(/[^0-9]/g, "");
                      }
                        return typeof i === 'string' ?
                            i.replace(/[\$,]/g, '')*1 :
                            typeof i === 'number' ?
                                i : 0;
                    };
         
                    // computing column Total of the complete result 
                    var empTotal = api.column( 1 ).data().reduce( function (a, b) {return intVal(a) + intVal(b);}, 0 );
                    var poorTotal = api.column( 3 ).data().reduce( function (a, b) {return intVal(a) + intVal(b);}, 0 );
                    var averageTotal = api.column( 4 ).data().reduce( function (a, b) {return intVal(a) + intVal(b);}, 0 );
                    var goodTotal = api.column( 5 ).data().reduce( function (a, b) {return intVal(a) + intVal(b);}, 0 );
                    
                        
                    // Update footer by showing the total with the reference of the column index 
                    $( api.column( 0 ).footer() ).html('Total');
                    $( api.column( 1 ).footer() ).html(empTotal);
                    $( api.column( 3 ).footer() ).html(poorTotal);
                    $( api.column( 4 ).footer() ).html(averageTotal);
                    $( api.column( 5 ).footer() ).html(goodTotal);
                }
            });
            
            $(".buttons-excel").addClass("btn btn-primary");
            $(".buttons-excel").removeClass("dt-button");
            $(".buttons-pdf").addClass("btn btn-primary");
            $(".buttons-pdf").removeClass("dt-button");
            skill_report_table.columns().every(function () {
                var that = this;
    
                $('#skill_report_filter > input', this.header()).on('keyup change clear', function () {
                    if (that.search() !== this.value) {
                        that
                            .search(this.value)
                            .draw();
                    }
                });
            });
            // console.log('columns',$('#skill_report').columnCount())
            
        },
        willStart: function() {
            return $.when(ajax.loadLibs(this), this._super());
        },
        start: function() {
            var self = this;
            return this._super();
        },
        render: function() {
            var super_render = this._super;
            var self = this;
            var kw_skill = QWeb.render( 'kw_skill_assessment.skill_report', {
                widget:self.skill_master,
            });
            $(kw_skill).prependTo(self.$el);
            return kw_skill;
        },
        reload: function () {
                window.location.href = this.href;
        },
    });
    function _castString (value) {
        const type = typeof value
      
        switch (type) {
          case 'boolean':
            return value ? '1' : ''
          case 'string':
            return value
          case 'number':
            if (isNaN(value)) {
              return 'NAN'
            }
      
            if (!isFinite(value)) {
              return (value < 0 ? '-' : '') + 'INF'
            }
      
            return value + ''
          case 'undefined':
            return ''
          case 'object':
            if (Array.isArray(value)) {
              return 'Array'
            }
      
            if (value !== null) {
              return 'Object'
            }
      
            return ''
          case 'function':
            // fall through
          default:
            throw new Error('Unsupported value type')
        }
      }
    function strip_tags (input, allowed) { 
        
        // making sure the allowed arg is a string containing only tags in lowercase (<a><b><c>)
        allowed = (((allowed || '') + '').toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []).join('')
        const tags = /<\/?([a-z0-9]*)\b[^>]*>?/gi
        const commentsAndPhpTags = /<!--[\s\S]*?-->|<\?(?:php)?[\s\S]*?\?>/gi
        let after = _castString(input)
        // removes tha '<' char at the end of the string to replicate PHP's behaviour
        after = (after.substring(after.length - 1) === '<') ? after.substring(0, after.length - 1) : after
        // recursively remove tags to ensure that the returned string doesn't contain forbidden tags after previous passes (e.g. '<<bait/>switch/>')
        while (true) {
          const before = after
          after = before.replace(commentsAndPhpTags, '').replace(tags, function ($0, $1) {
            return allowed.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : ''
          })
          // return once no more tags are removed
          if (before === after) {
            return after
          }
        }
      }

    core.action_registry.add('kw_skill_assessment.skill_report', SkillReportView);
    return SkillReportView
});

