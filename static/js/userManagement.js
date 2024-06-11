
$(document).ready(function () {

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

    $('input[name="email"]').on("focus" , function(e){
        $("input[name='email']").removeClass('error')
        $(".email").hide()
    })

    $('input[name="password"]').on("focus" , function(e){
        $("input[name='password']").removeClass('error')
        $("input[name='password2']").removeClass('error')
        $(".password").hide()
    })

    $("#create-user").on("click" , function(e){
        e.preventDefault()

        $("#addModal").modal('show')
    })

    $(".save-user").on("click" , function(e){
        e.preventDefault();

        current_fs = $(this).parent().parent();
        next_fs = current_fs.next();

        var data = current_fs.serializeArray()
        
        if (validate_user()){
            $.ajax({
                type: "POST",
                url: $("#create-form").attr('action'),
                data: data,
                dataType: "JSON",
                success: function (response) { 
                    console.log(response)
                    window.location = window.location.href
                },
                error: function(error){
                    console.log(error)
                    toastr.options = options
                    toastr["error"](error, "SNOIE ERROR")
                    
                }
            });
        }
        

        
    })



});





function validate_user(){
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let email = $('input[name="email"]').val()
    let password1 = $('input[name="password"]').val()
    let password2 = $('input[name="password2"]').val()
    let organisation = $('select[name="organisation"]').val()
    let role  = $('select[name="role"]').val()
    let name = $('input[name="lastName"]').val()

    console.log(organisation)
    console.log(role)
    console.log(name)

    if(name.length < 2){
        $("input[name='lastName']").addClass('error')
        $(".name").show()
        return false
    }

    if(organisation == 0){
        $('select[name="organisation"]').addClass('error')
        $(".no-empty").show()
        return false
    }

    if(role==0){
        $("select[name='role']").addClass('error')
        $(".no-empty").show()
        return false
    }

    if (!emailRegex.test(email)){
        $("input[name='email']").addClass('error')
        $(".email").show()
        return false
    }

    $.ajax({
        async: false,
        type: "GET",
        url: "/accounts/check-email?email=" + email,
        async: false,
        success: function (response) {
            exist = response.exist
            if(exist == true){
                $("input[name='email']").addClass('error')
                $(".email-exist").show()
                return false
            }
            console.log(response)
        },
        error: function (error) {
            console.log(error);
        }
    });


    if(password1 != password2 || password1.length < 6){
        $(".password").show()
        $("input[name='password']").addClass('error')
        $("input[name='password2']").addClass('error')
        return false
    }

    
    return true
}