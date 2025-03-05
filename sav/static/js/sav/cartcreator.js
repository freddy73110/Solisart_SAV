function getISOWeekNumber(date) {
    const target = new Date(date.valueOf());
    const dayNumber = (date.getDay() + 6) % 7; // Ajuste pour que lundi = 0, dimanche = 6
    target.setDate(target.getDate() - dayNumber + 3); // Se place au jeudi de la semaine actuelle
    const firstThursday = new Date(target.getFullYear(), 0, 4);
    const weekNumber = Math.ceil(((target - firstThursday) / 86400000 + firstThursday.getDay() + 1) / 7);
    return weekNumber;
}

$("#typeInstallation").on('change', function(){
    var years = new Date().getFullYear()
    // currentDate = new Date();
    // currentDate.setDate(currentDate.getDate() + 2 )
    // console.log("coucou", currentDate)
    // startDate = new Date(currentDate.getFullYear(), 0, 1);
    // var days = Math.floor((currentDate - startDate) /
    //     (24 * 60 * 60 * 1000));            
    var weekNumber = ("0" + getISOWeekNumber(new Date()) ).slice(-2);
    data = {"installExiste": years.toString() + weekNumber.toString()}
    $.ajax({
         url: window.location.href,
         data: data,
         dataType: 'json',
         type: 'post',
         success: function (json) {
            $("[name=new_installation]").val($("#typeInstallation").val()+ json['SN'])
         },
    })            
})
$("#typeInstallation").change()
$("#option").on('change', function(){
if($("#option").val() == "json"){
    const jsonInCl = document.getElementById('jsonInCl').textContent
    if (jsonInCl == 'true'){
        const CL = document.getElementById('CL').textContent
        $("#divInstallation").addClass('d-none')
        $("#divFile").removeClass('d-none')
        $("#divFile").append("<span>La carte sera créée avec le fichier json de la commande "+ CL +" </span>")
        $("#divFile").find(".mb-3:first").addClass('d-none')                
        $("#submit").prop("disabled",false);
    }else{
        $("#divInstallation").addClass('d-none')
        $("#divFile").removeClass('d-none')
        $("label[for='formFile']").html("Sélectionner le json généré par la schématèque")
        $('#formFile').attr("accept", "." + "json")
        $("#submit").prop("disabled",false);
    }
}else if($("#option").val() == "csv"){
    $("#divInstallation").addClass('d-none')
    $("#divFile").removeClass('d-none')
    $("label[for='formFile']").html("Sélectionner le fichier csv de configuration de l'installation")
    $('#formFile').attr("accept", "." + "csv")
    $("#submit").prop("disabled",false);
}else if($("#option").val() == "installation"){
    $("#divFile").addClass('d-none')
    $("#divInstallation").removeClass("d-none")
    $("#submit").prop("disabled",false);
}else{
    $("#submit").prop("disabled",true);
}
})
$("#option").change()
$("#submit").on('click', function(e){
    e.preventDefault();
    var data = new FormData($('form').get(0))
    $("#results").parent().removeClass('d-none')
    $("#formFile").prop("disabled",true);
    $("#divInstallation").prop("disabled",true);
    $("#option").prop("disabled",true);
    $.ajax({
         url: window.location.href,
         data: data,
         dataType: 'json',
         type: 'post',
         success: function (json) {
            console.log(json)
         },
         cache: false,
        contentType: false,
        processData: false
    })
})

var processing = false
    var json = false
    var png = false
    var client = false
        const socket = new WebSocket('ws://'+window.location.host+'/ws/cartcreator/');
        socket.onmessage = (e) => {
            data = JSON.parse(e.data)
            if (data.hasOwnProperty("processing")) {
                processing = data.processing
                if (processing == true){
                    $("#submit").prop("disabled",true);
                    $("#stop").removeClass("d-none")
                    $("#submit").html('<i class="fas fa-sun fa-spin" style="color:yellow"></i> Processus en cours')
                }else{
                    $("#submit").prop("disabled",false);
                    $("#submit").html('Lancer')
                    $("#stop").addClass("d-none")
                }
            }
            if(data.hasOwnProperty("download")){
                download_config()
            }
            if (data.hasOwnProperty("message")) {
                var dt = new Date();
                var min, sec
                if(dt.getMinutes() < 10){
                    min = "0" + dt.getMinutes()
                }else{
                    min = dt.getMinutes()
                }
                if(dt.getSeconds() < 10){
                    sec = "0" + dt.getSeconds()
                }else{
                    sec = dt.getSeconds()
                }
                var time = dt.getHours() + ":" + min + ":" + sec;
                result = data.message;
                $('#results li:last-child').remove();
                $("#results").append("<li><b>"+ time + ":</b> "+ result + "</li>");
                if(processing == true){
                    $("#results").append('<li><i class="fas fa-sun fa-spin" style="color:yellow"></i></li>');
                }
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("li:last").offset().top
                }, 2000);
            }
        }
        socket.onclose = (e) => {
            var dt = new Date();
            var min, sec
            if(dt.getMinutes() < 10){
                min = "0" + dt.getMinutes()
            }else{
                min = dt.getMinutes()
            }
            if(dt.getSeconds() < 10){
                sec = "0" + dt.getSeconds()
            }else{
                sec = dt.getSeconds()
            }
            var time = dt.getHours() + ":" + min + ":" + sec;
            $('#results li:last-child').remove();
            $("#results").append(
                "<li class='text-danger'><b>"+time+":WebSocket déconnectée. Attenter quelques minutes avant de vérifier l'état de la carte.</b></li>");
        }


$("#stop").on("click", function(){
    socket.send(JSON.stringify({
        stop: "stop"
    }))
})


$("#formFile").on('change', function(event) {
  var reader = new FileReader();

  reader.onload = function(event) {
    var jsonObj = JSON.parse(event.target.result);
    console.log(jsonObj);
  }

  reader.readAsText(event.target.files[0]);
});
function download_config(){
    var form=$(form)
    $.ajax({
        url: window.location.href,
        data: form.serialize() + '&download=-',
        type: 'post',
        xhrFields:{
            responseType: 'blob'
        },
        success: function(response){
            if($("#option").val() == "json"){
                var fileName= 'config_' + $("input[name=new_installation]").val() + '.csv'
            }
            if($("#option").val() == "installation"){
                var fileName= 'config_' + $("#installation").val() + '.csv'
            }
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(response)
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
        }
    })
}