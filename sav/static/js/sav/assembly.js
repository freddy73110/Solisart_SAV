$('[id ^=id_tracability][id $=-organ]').on("change", function(){
    var batchId = $(this)[0].id.replace("organ", "batch")
    var articlePk = $(this).val()
    $.ajax({
        url: window.location.href,
        type:'post',
        data: {articleChanged: articlePk},
        dataType: 'json',
        success: function (data) {
            var batches = data.batches
            $("#" + batchId).html("")
            if (batchId.includes('tracabilityMobal')){
                $.each(batches, function(i, v){
                    $("#" + batchId).append('<option value="'+v[0]+'">'+v[1]+'</option>')
                })
                batchId = batchId.replace("tracabilityMobal", "tracability")
            }else{
                $.each(batches, function(i, v){
                    $("#" + batchId).append('<option value="'+v[0]+'">'+v[1]+'</option>')
                })
                batchId = batchId.replace("tracability", "tracabilityMobal")
            }
            $.each(batches, function(i, v){
                $("#" + batchId).append('<option value="'+v[0]+'">'+v[1]+'</option>')
            })
        }
    })
    $('[id ^=id_tracability-]').on("blur", function(){
        var idToUpdate =this.id.replace("tracability", "tracabilityMobal")
        $("#"+idToUpdate).val($(this).val())
    })
    $('[id ^=id_tracabilityMobal-]').on("blur", function(){
        var idToUpdate =this.id.replace("tracabilityMobal", "tracability")
        $("#"+idToUpdate).val($(this).val())
    })
})

var $table = $($('#button').closest("fieldset").find("table")[0])
var $button = $('#button')
var $delete = $('#delete')
$(function() {
    $button.click(function () {
    var $t = $($('#button').closest("fieldset").find("table")[0]);
    var index = $t.find("tbody tr input").last()[0].id.split('-')[1]
    var nextIndex = parseInt(index) + 1
    var $row = $t.find("tbody tr").last();
    var ToAppend = $row.prop('outerHTML').replaceAll(index, nextIndex)
    $t.append(ToAppend)
    
    var $carouselItem = $("#ModalDiv").find(".carousel-item").last()
    var carouselItemToAppend = $carouselItem.prop('outerHTML').replaceAll(index, nextIndex)
    $(".carousel-inner").append(carouselItemToAppend)

    var $carouselItem = $("#ModalDiv").find(".carousel-indicators button").last()
    var carouselItemToAppend = $carouselItem.prop('outerHTML').replaceAll(index, nextIndex)
    $(".carousel-indicators").append(carouselItemToAppend)

    $("#id_tracability-" + nextIndex + "-organ").trigger( "change" )

    var v = document.getElementById("id_tracability-TOTAL_FORMS");
    v.value = parseInt(v.value) + 1;
    $('[id ^=id_tracability-][id $=-organ]').on("change", function(){
        var batchId = $(this)[0].id.replace("organ", "batch")
        var articlePk = $(this).val()
        $.ajax({
            url: window.location.href,
            type:'post',
            data: {articleChanged: articlePk},
            dataType: 'json',
            success: function (data) {
                var batches = data.batches
            $("#" + batchId).html("")
            if (batchId.includes('tracabilityMobal')){
                $.each(batches, function(i, v){
                    $("#" + batchId).append('<option value="'+v[0]+'">'+v[1]+'</option>')
                })
                batchId = batchId.replace("tracabilityMobal", "tracability")
            }else{
                $.each(batches, function(i, v){
                    $("#" + batchId).append('<option value="'+v[0]+'">'+v[1]+'</option>')
                })
                batchId = batchId.replace("tracability", "tracabilityMobal")
            }
            $.each(batches, function(i, v){
                $("#" + batchId).append('<option value="'+v[0]+'">'+v[1]+'</option>')
            })
            }
        })
    })
    $('[id ^=id_tracability-]').on("blur", function(){
        var idToUpdate =this.id.replace("tracability", "tracabilityMobal")
        $("#"+idToUpdate).val($(this).val())
    })
    $('[id ^=id_tracabilityMobal-]').on("blur", function(){
        var idToUpdate =this.id.replace("tracabilityMobal", "tracability")
        $("#"+idToUpdate).val($(this).val())
    })
  })
  
});
$(function() {
    var $button = $('#button')
    var $delete = $('#delete')
      $delete.click(function () {
        var $t = $($('#button').closest("fieldset").find("table")[0]);
        var $row = $t.find("tbody tr").last();
        var $carouselItem = $("#ModalDiv").find(".carousel-item").last()
        var $carouselItemButton = $("#ModalDiv").find(".carousel-indicators button").last()
        var rowLength = $t.find("tr").length;
        if (rowLength>2){
            $row.remove();
            console.log($carouselItem, $carouselItemButton)
            $carouselItem.remove();
            $carouselItemButton.remove()
            $("#carouselExampleDark").carousel()
            var v = document.getElementById("id_tracability-TOTAL_FORMS");
            v.value = parseInt(v.value) - 1;
        }else{
            $delete.prop("disabled",true)
        }
        })
});

      $(".buttonSave").on("click", function(){
        var form = $(this).closest("form")
        form.find('select').prop('disabled', false)
        $(this).prop('disabled', true)
        $.ajax({
            url: window.location.href,
            type:'post',
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
            //todo faire un message de validation
                window.location.reload();
            }
    })

    })
    $("input[id$='-icon']").on("click", function(){
        var id = $(this)[0].id.replace("icon", "date")
        if($(this).is(":checked")){
            var today = new Date();
            var date =  today.getFullYear() +'-'+(today.getMonth()+1)+'-'+today.getDate();
            $("#" + id).val(date)
        }else{
            $("#" + id).val('')
        }
    })

    function downloadSchema(Cl_id){
        $.ajax({
                    url: window.location.href,
                    type:'post',
                    data:{'downloadSchema': Cl_id},
                    xhrFields:{
                        responseType: 'blob'
                    },
                    success: function (response) {
                        var image = new Image();
                        image.src = URL.createObjectURL(response);
                        image.className="img-fluid rounded mx-auto d-block p-3"
                        $('#schema').html(image);
                    },
                    error: function(){
                        alert('error!');
                    }
                })
    }
    const CLid = document.getElementById('CLid').textContent
    downloadSchema(CLid)
function modify(t, row){
    var myModal = new bootstrap.Modal(document.getElementById('ModalDiv'), {
        keyboard: false
      })
      myModal.show()

}

$('[id ^=id_tracability-]').on("blur", function(){
    var idToUpdate =this.id.replace("tracability", "tracabilityMobal")
    $("#"+idToUpdate).val($(this).val())
})
$('[id ^=id_tracabilityMobal-]').on("blur", function(){
    var idToUpdate =this.id.replace("tracabilityMobal", "tracability")
    $("#"+idToUpdate).val($(this).val())
})

