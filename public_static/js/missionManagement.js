
$(document).ready(function () {


    $("#create-mission").on("click" , function(e){
        e.preventDefault()
        var data =get_mission_initial_data()
        console.log(data)

        $('#addMissionModal input[name="nom_mission"]').val(data['mission_name'])

        var select_fp = '<select name="fp" id="fp" class="form-control">'
        
        for(let i=0; i<data["fp"].length;  i++){
            select_fp += '<option value="'+data["fp"][i]["id"]+'">' + data["fp"][i]["ref"] + '</o[tion>'
        }
                            
        select_fp +='</select>'
        

        $("#addMissionModal #select-fp").append(select_fp)
        $("#addMissionModal").modal('show')
    })



});


function get_mission_initial_data(){
    var mission = []
    $.ajax({
        type: "GET",
        url: "/mission/create-mission",
        async: false,
        success: function (response) {
            
            mission = response
        },
        error: function (error) {
            console.log(error);
        }
    });

    return mission
}