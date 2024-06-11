//Initialize Select2 Elements

$(document).ready(function () {
    $('.select2').select2()
    $('.signature').click(function (e) { 
        e.preventDefault();
        alert('hello')
    });
});
//select multiple dates
//$('#datePick').multiDatesPicker(); 
//Datemask2 mm/dd/yyyy
//$('#datemask').inputmask('dd/mm/yyyy', { 'placeholder': 'dd/mm/yyyy' })
//Datemask2 mm/dd/yyyy
//$('#datemask2').inputmask('mm/dd/yyyy', { 'placeholder': 'mm/dd/yyyy' })
//Money Euro
//$('[data-mask]').inputmask()

    
