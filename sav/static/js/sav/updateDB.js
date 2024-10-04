//To display and downloads file since json file
$(".api").on("click", function(){
    var importedFile = $("#json_file")[0].files[0];
    var typeOutput=this.id
    var reader = new FileReader();
    reader.onload = function() {
        var fileContent = JSON.stringify(JSON.parse(reader.result));            
        $.ajax({
            url: window.location.href,
            type:'post',
            data: {'typeOutput':typeOutput,"jsonfile":fileContent},
            xhrFields:{
                responseType: 'blob'
            },
            success: function(response) {
                if(response.size != '0'){
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(response)
                    if(typeOutput == "exe"){
                        link.download = $("#json_file")[0].files[0].name.replace('.json', '.png');
                        var image = new Image();
                        image.src = URL.createObjectURL(response);
                        image.className="img-fluid rounded mx-auto d-block"
                        $("#imageResult").html(image);
                    }else if (typeOutput == "hydro"){
                        link.download = $("#json_file")[0].files[0].name.replace('.json', '.png');
                        var image = new Image();
                        image.src = URL.createObjectURL(response);
                        image.className="img-fluid rounded mx-auto d-block"
                        $("#imageResult").html(image);
                    }else if (typeOutput == "ficheProg"){
                        link.download = $("#json_file")[0].files[0].name.replace('.json', '.png');
                        var image = new Image();
                        image.src = URL.createObjectURL(response);
                        image.className="img-fluid rounded mx-auto d-block"
                        $("#imageResult").html(image);
                    }else if (typeOutput == "config"){
                        link.download = $("#json_file")[0].files[0].name.replace('.json', '.csv');
                    }
                    document.body.appendChild(link);
                    link.click();
                }else{
                    showToast("<li class='text-danger'><b> Le fichier n'est pas formaté comme il faut</b></li>")
                }
            }
        });
    };
    reader.readAsText(importedFile)
})

//to Export price to sender site
function exportprix(){
    $("#resulexport").html('<h1><i class="fas fa-sun fa-spin" style="color:yellow"></i></h1>')
    $.ajax({
                        url: window.location.href,
                            type:'post',
                            data: "exportprix=exportprix",
                            dataType: 'html',
                            success: function (html) {
                                    $("#resulexport").html(html)
                                    $("h3.m-3").html("Dernière mise à jour: A l'instant")
                            }
                    })
}
//to display toast message
function showToast(Toastbody){
    var d = new Date();
    var n = d.toLocaleTimeString();
    $("#toastSmall").html(n)
    $(".toast-body").html(Toastbody)
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
      var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl)
      })
      toastList.forEach(toast => toast.show())
}

//to open websocket
const socket = new WebSocket('ws://'+window.location.host+'/ws/updateDB/');
        socket.onmessage = (e) => {
            var d = JSON.parse(e.data)
            $("#inputGroup").prop('disabled', true)
            if(!$("#modal-progress").hasClass("show")){
                $("#modal-progress").modal("show")
                $(".modal-title").html("Mise à jour des " + d.total +" " + d.nature)
            }
            var progress = parseInt(d.index / d.total * 100, 10);
                  var strProgress = progress + "%";
                  $(".progress-bar").css({"width": strProgress});
                  $(".progress-bar").text(strProgress);
            if (d.hasOwnProperty("message")) {
                if(d.message.includes("Importation finie:")){
                    $("#modal-progress").modal("hide")
                    window.location.href=window.location.href
                }
            }
        }
        socket.onclose = (e) => {
            console.log("Socket closed!");
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
            showToast("<li class='text-danger'><b>"+time+":WebSocket déconnectée. Veuillez réactualiser la page</b></li>")
        }