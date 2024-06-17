function get_alert_informations(url){
    var result 
    $.ajax({
        type: "GET",
        url: url,
        async: false,
        success: function (response) {
            
            result = response.html
        },
        error: function (error) {
            console.log(error);
        }
    });

    return result
}


function load_departments(region_id){
    var departments = []
    $.ajax({
        type: "GET",
        url: "/shared/get-departments",
        data: { region_id: region_id},
        async: false,
        success: function (response) {
            
            departments = response.departments
        },
        error: function (error) {
            console.log(error);
        }
    });

    return departments
}


function load_arrs(department_id){
    var arrs = []
    $.ajax({
        type: "GET",
        url: "/shared/get-arr",
        data: { department_id: department_id},
        async: false,
        success: function (response) {
            
            arrs = response.arrs
            console.log(response)
        },
        error: function (error) {
            console.log(error);
        }
    });

    return arrs
}


function get_alert_canals(){
    var canals ;

    $.ajax({
        type: "GET",
        url: "/shared/get-canal",
        async: false,
        success: function (response) {
            
            canals = response.canals
            console.log(response)
        },
        error: function (error) {
            console.log(error);
        }
    });

    return canals

}