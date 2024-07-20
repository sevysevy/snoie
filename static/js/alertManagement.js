$(document).ready(function () {

    $("#step").val(1)
    var options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-top-full-width",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
    }
    var current_fs, next_fs;
    $(".form-control").on('input' , function(){
        $('.form-control').removeClass("field-error")
        $('.invalid').text('')
    })

    $('#region').select2({
        allowClear: true,
        placeholder: {
            id: "0",
            text:"Choisir dans la liste",
            selected:'selected'
          },
    });

    $('#department').select2({
        allowClear: true,
        placeholder: {
            id: "0",
            text:"Choisir dans la liste",
            selected:'selected'
          },
    })
    $('#arrondissement').select2({
        allowClear: true,
        placeholder: {
            id: "0",
            text:"Choisir dans la liste",
            selected:'selected'
          },
    })

    $('#canal').select2({
        allowClear: true,
        placeholder: {
            id: "0",
            text:"Choisir dans la liste",
            selected:'selected'
          },
    })

    $('#region').on('select2:select', function (e) {
        var data = e.params.data;
        var region_id = data.id
        var departments = load_departments(region_id)
        
        $('#department').select2().empty().select2({
            data:[{"id":0, "text":"Choisir dans la liste"}].concat(departments.map((obj)=>{return {"id":obj.id , "text":obj.name}}))
        }).trigger("change");

        $(".department").removeAttr("hidden")
    });

    $('#department').on('select2:select', function (e) {
        var data = e.params.data;
        var department_id = data.id
        var arrs = load_arrs(department_id)

        $('#arrondissement').select2().empty().select2({
            data: [{"id":0, "text":"Choisir dans la liste"}].concat(arrs.map((obj)=>{return {"id":obj.id , "text":obj.name}}))
        }).trigger("change");

        $(".arrondissement").removeAttr("hidden")
    });


    $('#arrondissement').on('select2:select', function (e) {
        
        $(".village").removeAttr("hidden")
    });


    $('.next').click(function (e) { 
        e.preventDefault();

        current_fs = $(this).parent();
        next_fs = $(this).parent().next();
        var donnee = current_fs.serializeArray();
        donnee.push({name : 'csrfmiddlewaretoken', value : $("input[name='csrfmiddlewaretoken']").val()})
        donnee.push({name: "step", value : $("#step").val()})

        function validate(){
            result = true

            if ($("#step").val() == "1"){
                if ($("#alert_declaration").val().length < 2) {
                    $('.alert-declaration-error').text('ce champ ne peut être vide');
                    result = false
                    $("#alert_declaration").addClass("field-error")
                }

                if(!Date.parse($("#date_alert").val())){
                    $('.date-error').text('ce champ ne peut être vide')
                    result = false
                    $("#date_alert").addClass("field-error")
                }
            }

            if ($("#step").val() == "2"){  

                if ($("#region").select2('val') == 0) {
                    $('.region-error').text('ce champ ne peut être vide');
                    result = false
                    $("#region").addClass("field-error")
                }
                if ($("#department").select2('val') == 0) {
                    $('.department-error').text('ce champ ne peut être vide');
                    result = false
                    $("#department").addClass("field-error")
                }
                if ($("#arrondissement").select2('val')== 0) {
                    $('.arrondissement-error').text('ce champ ne peut être vide');
                    result = false
                    $("#arrondissement").addClass("field-error")
                }
                if ($("#village").val().length < 3) {
                    $('.village-error').text('ce champ ne peut être vide');
                    result = false
                    $("#village").addClass("field-error")
                }
            }

            return result

        }
        
        if (validate())
        {
            console.log($("#alert_declaration").length)
            var step = $("#step").val()
            if (step == "1"){
 
                $.ajax({
                    type: "POST",
                    url: window.location.href,
                    data: donnee,
                    dataType: "JSON",
                    success: function (response) { 
                        $("#step").val(response["next-step"]) 
                        console.log(response)
    
                        //Add Class Active
                        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                        
                        //show the next fieldset
                        next_fs.show(); 
                        //hide the current fieldset with style
                        current_fs.animate({opacity: 0}, {
                            step: function(now) {
                                // for making fielset appear animation
                                opacity = 1 - now;
    
                                current_fs.css({
                                    'display': 'none',
                                    'position': 'relative'
                                });
                                next_fs.css({'opacity': opacity});
                            }, 
                            duration: 600
                        });
                    },
                    error: function(error){
                        console.log(error)
                        toastr.options = options
                        toastr["error"](error, "SNOIE ERROR")
                        
                    }
                });
            }

            else if(step == "2"){
                console.log("saving the second step")

                $.ajax({
                    type: "POST",
                    url: window.location.href,
                    data: donnee,
                    dataType: "JSON",
                    success: function (response) { 
                        $("#step").val(response["next-step"]) 
                        console.log(response)
    
                        //Add Class Active
                        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                        
                        //show the next fieldset
                        next_fs.show(); 
                        //hide the current fieldset with style
                        current_fs.animate({opacity: 0}, {
                            step: function(now) {
                                // for making fielset appear animation
                                opacity = 1 - now;
    
                                current_fs.css({
                                    'display': 'none',
                                    'position': 'relative'
                                });
                                next_fs.css({'opacity': opacity});
                            }, 
                            duration: 600
                        });
                    },
                    error: function(error){
                        console.log(error)
                        toastr.options = options
                        toastr["error"](error.responseText, "SNOIE ERROR")
                        
                    }
                });
            }
            
            else if(step == "3"){
                console.log(donnee)
                get_comment_template()

                $('body').on("click" ,"#get-comment" , function(){
                    donnee.push({"name":"comment" , "value": $("#comment").val()})
                    close_comment_modal()
                    $.ajax({
                        type: "POST",
                        url: window.location.href,
                        data: donnee,
                        dataType: "JSON",
                        success: function (response) { 
                            $("#step").val(response["next-step"]) 
                            console.log(response)
        
                            //Add Class Active
                            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                            
                            //show the next fieldset
                            next_fs.show(); 
                            //hide the current fieldset with style
                            current_fs.animate({opacity: 0}, {
                                step: function(now) {
                                    // for making fielset appear animation
                                    opacity = 1 - now;
        
                                    current_fs.css({
                                        'display': 'none',
                                        'position': 'relative'
                                    });
                                    next_fs.css({'opacity': opacity});
                                }, 
                                duration: 600
                            });
    
                            
                        },
                        error: function(error){
                            console.log(error)
                            toastr.options = options
                            toastr["error"](error.responseText, "SNOIE ERROR")
                            
                        }
                    });

                })

                $("body").on("click" , "#no-comment" , function(e){
                    e.preventDefault()
                    close_comment_modal()
                    $.ajax({
                        type: "POST",
                        url: window.location.href,
                        data: donnee,
                        dataType: "JSON",
                        success: function (response) { 
                            $("#step").val(response["next-step"]) 
                            console.log(response)
        
                            //Add Class Active
                            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                            
                            //show the next fieldset
                            next_fs.show(); 
                            //hide the current fieldset with style
                            current_fs.animate({opacity: 0}, {
                                step: function(now) {
                                    // for making fielset appear animation
                                    opacity = 1 - now;
        
                                    current_fs.css({
                                        'display': 'none',
                                        'position': 'relative'
                                    });
                                    next_fs.css({'opacity': opacity});
                                }, 
                                duration: 600
                            });
    
                            
                        },
                        error: function(error){
                            console.log(error)
                            toastr.options = options
                            toastr["error"](error.responseText, "SNOIE ERROR")
                            
                        }
                    });
                })



                
                
            }
            



            
        }
        
        
        
     
    });
    $(".previous").click(function(){
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();
        $(".invalid").text('');
        //Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
        var current_step = Number($("#step").val())
        $("#step").val(current_step-1)
        //show the previous fieldset
        previous_fs.show();

        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            }, 
            duration: 600
        });
        
    });


    $(".table-button.delete").on("click" , function(e){
        e.preventDefault();

        let id = $(this).attr("alert-id")
        console.log($(this))

        $("#deleteModal .delete-button").attr("alert-id"  , id)

        $("#deleteModal").modal('show')
    })


    $("#deleteModal .delete-button").on("click" , function(e){
        e.preventDefault();

        console.log($(this).attr("alert-id"))
        data = [{name:"alert_id" , value:$(this).attr("alert-id")} , {name:"csrfmiddlewaretoken" , value:$("input[name='csrfmiddlewaretoken']").val()}]
        $.ajax({
            type: "POST",
            url: $(this).attr("del-endpoint"),
            data: data,
            dataType: "JSON",
            success: function (response) { 
                window.location = window.location.href
            },
            error: function(error){
                console.log(error)
                toastr.options = options
                toastr["error"](error.responseText, "SNOIE ERROR")
                
            }
        });
        
    })

    $("#deleteModal .cancel").on("click" , function(e){
        e.preventDefault();

        $("#deleteModal").modal('hide')
        
    })

});


