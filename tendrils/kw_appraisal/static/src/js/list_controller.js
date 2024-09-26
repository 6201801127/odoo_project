odoo.define('kw_appraisal.ListController', function (require) {
    "use strict";
    
    var ListController = require('web.ListController');
    
    ListController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            if (typeof this !== "undefined" && this.hasOwnProperty('modelName') && this.hasOwnProperty('viewType')){
                if(this.modelName == 'hr.appraisal' && this.viewType == 'list'){
                    $(".o_menu_apps").find('.dropdown-menu[role="menu"]').removeClass("show");
                }
            }  
            
        }
    });
    
    return ListController;
    
    });
    