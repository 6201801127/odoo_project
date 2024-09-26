odoo.define('kw_recruitment.kwapplicant_workexp_validation', function (require) {
    'use strict';
    var work = {
        current_id: '',
        clone: '',
        dateFormat: 'dd-mm-yyyy',
        // 'yyyy-mm-dd'
        init: function(){
            this.validate();
            // this.dateRestrict('0');
            this.showHideBlock();
            this.showHideButton();
            this.select2();
            this.updateCounter();

            
            var datepickerelmts = $('.work_datepicker').length
            if (datepickerelmts>0){
                var totpicklength = datepickerelmts/2
                for (let index = 0; index < datepickerelmts/2; index++) {                    
                    this.dateRestrict(index);
                } 
            }

//            this.addRules($("#parent-block"));

            this.current_id = $('.item-block').size();
            this.clone = $('#main_00').clone();
            $('#btnadd').click(function(){
                work.addMore();
            });
            $(document).on("click",".close_row", function(){
                work.removeItem(this);
            });


            $("input[name='experience']:checked"). val() == '1' ? $('.hide').hide() : $('.hide').show();
            $('.workexperience').on('change',function(){
                ($(this).val()==1) ? $('.hide').hide() : $('.hide').show();
            });

            $(document).on("keydown keyup", "input[type=text]", function(){
                var $el = $(this);
                var val = $el.val().replace(new RegExp("^[ ]+", "g"), "");
                //Organisation name
                if ($el.hasClass("orgval")) {
                    val = val.replace(/[^a-z\d\@\.\s\,]/gi, '');
                }
                //Designation name
                if ($el.hasClass("desgval")){
                    val = val.replace(/[^a-z\-\s]/gi, '');
                }
                $el.val( val );
            });


            
            
        },
        validate: function(){

                $.validator.messages.accept     = 'File must be .jpeg,.png, .pdf format';
                $.validator.messages.filesize   = 'File size must be less than 4 MB';
                
                $.validator.addClassRules({  
                    workexp_file_upload: {
                        required    : function(element) {                         
                            //if experienced and hidden field is empty then mandatory 
                            return ($("input[name='experience']:checked").val() == '2' && $(element).closest('.filesection').find('input[type="hidden"]').val() == '' );
                        },
                        accept      : "image/png,image/jpeg,image/jpg,application/pdf",
                        filesize    : 4194304
                    }, 
                    clsrequired: {
                        required    : true,                    
                    },  
                    clsoptrequired: {
                        selectListItem: "0",
                    },                     
                });



            var frm = $("form#frm_work_experience").validate({
                ignore:':hidden',
                rules: {
                    experience: { selectListItem: "0" }
                },
                
                // Specify validation error messages
                messages: {
                    experience: { selectListItem: "Please select experience  !" }
                },
                // Make sure the form is submitted to the destination defined
                // in the "action" attribute of the form when valid
                submitHandler: function (frm) {
                    frm.submit();
                },
                errorElement: "div",
                highlight: function (element) {
                    $(element).css('background', '#ffdddd');
                },
                // Called when the element is valid:
                unhighlight: function (element) {
                    $(element).css('background', '#ffffff');
                },
            });

            $('#btnSubmitED').click(function(){
                if($("form#frm_work_experience").valid()){
                    var experience = $('input[type=radio][name=experience]:checked').val() == '2' ? "<p style='text-align:left !important;'>Please mention the names of the previous employment only for which you have Experience letters/Service Certificates available with you.</p>"+ 

                    "<p style='text-align:left !important;'>If you have not received the Current company's experience letter we can consider the same within 45 days.</p>":"Are you sure submit the data?";
                    swal({
                        title: "Applicant Data Submit",
                        text: experience,
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: 'OK',
                        cancelButtonText: 'Cancel',
                        dangerMode: true,
                        textAlign: "left",
                        html: true,
                        width: '800px',
                    },
                    function(isConfirm){
                        if (isConfirm){
                            document.getElementById("frm_work_experience").submit();
                        } else {
                            //  swal("Cancelled", "error");
                            //  swal.close();
                        }
                    });
                }
            });
        },
        dateRestrict: function(cnt){

                var from = $("#work_dufrom_"+cnt).datepicker({
                    minDate: new Date(1954, 1 - 1, 1), 
                    maxDate: '0d', 
                    dateFormat: 'dd-M-yy',
                    changeMonth: true,
                    changeYear: true,
                    yearRange: "-60: + new Date().getFullYear()"
                })
                .on("change", function() {
                    to.datepicker('option', 'minDate', work.getDate(this));
                });
                var to = $("#work_duto_"+cnt).datepicker({
                    minDate: new Date(1954, 1 - 1, 1), 
                    maxDate: '0d', 
                    dateFormat: 'dd-M-yy',
                    changeMonth: true,
                    changeYear: true,
                    yearRange: "-60: + new Date().getFullYear()"
                })
                .on("change", function() {
                    from.datepicker('option', 'maxDate', work.getDate(this));
                });

                $("#work_dufrom_"+cnt).datepicker("option", "showAnim", "slideDown");
                $("#work_duto_"+cnt).datepicker("option", "showAnim", "slideDown");

        },
        getDate: function( element ) {
            var date;
            try {
                date = $(element).datepicker('getDate');
            } catch( error ) {
                date = null;
            }
            return date;
        },
        showHideBlock: function(){
            $("#workexperience").val()=='1'?$("#parent-block").hide() :$("#parent-block").show();
            $("#workexperience").val()=='1'?$(".hide").hide():$(".hide").show();
        },
        showHideButton: function(){
            $('.item-block').size()>1?$(".close_row").show():$(".close_row").hide();
        },
        addMore: function(){
            
            var newElement  = this.clone.clone();
            var current_id  = this.current_id++;
            newElement.find('select').val("0");
            newElement.find("input").val("");
            newElement.find(".txt-filename").text("");
            newElement.find(".select2-container").remove();
            current_id      = this.current_id++;

            newElement.find('input, select').each(function(){
                // console.log($(this))
                $(this).attr('id',$(this).attr('id').replace(/\d+/,current_id));
                $(this).find('span').attr('id', $(this).attr('id').replace(/\d+/,current_id));
                if($(this).attr('name')){
                    $(this).attr('name',$(this).attr('name').replace(/\d+/,current_id));
                    $(this).find('span').attr('name', $(this).attr('name').replace(/\d+/,current_id));
                }
            });
            newElement.find('label').each(function(){
                $(this).attr('for', $(this).attr('for').replace(/\d+/,current_id));
            });
            newElement.find(".work_datepicker").removeClass('hasDatepicker');
            // newElement.find(".work_datepicker").datepicker({changeMonth : true, changeYear : true, minDate: new Date(1954, 1 - 1, 1), maxDate: new Date(), yearRange: '1954:', dateFormat: 'yy-mm-dd'});

            $("#parent-block").append(newElement);

            this.dateRestrict(current_id);
            this.showHideButton();
            //this.addRules(newElement);
            this.select2();
            this.updateCounter();
        },
        removeItem: function(el){
            $(el).closest('.item-block').remove();
            this.showHideButton();
            this.updateCounter();
        },

        select2: function(){
            $('select').select2();
            $('[data-rel="tooltip"]').tooltip();
        },
        updateCounter: function(){
            var cnt_index = 0;
            $('.block-counter-message').each(function(){
                $(this).html(++cnt_index);
            });
        }
    };
    $(function(){
        work.init();
    });
});

