$(document).ready(function () { 


    var context = $(".table-text")
    for(let i=0; i<context.length; i++){
        console.log(context[i])
        $(context[i]).html($(context[i]).html().substring(0,100)+"...")
    }
    
    

    $(".create-pertinence-sheet").on("click" , function(){

        var fiches = get_fiches_info()
        console.log(fiches)

        var html = ''

        for (let i = 0; i<fiches.length; i++ ){
            html += '<option value="' + fiches[i].id + '" >' + fiches[i].ref + '</option>'
        }

        $("#modal-add-fp #id_fi").html(html)

        $("#modal-add-fp").modal('show')
    })

    $("#modal-add-fp .creer").on("click" , function(){

        var id = $("#modal-add-fp #id_fi").val()

        console.log(id)

        window.location = "/fr/fiches-management/create-fiche-pertinence/" + id
    })



})

function get_fiches_info(){
    var fiches = []
    $.ajax({
        type: "GET",
        url: "/fiches-management/get-fiches-info",
        async: false,
        success: function (response) {
            
            fiches = response.fiches
        },
        error: function (error) {
            console.log(error);
        }
    });

    return fiches
}