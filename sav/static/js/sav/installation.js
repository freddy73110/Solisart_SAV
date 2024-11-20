//
const CL0 = document.getElementById('CL0').textContent.replaceAll('"', '');
$("#enregister").on("click", function(){
    hh = $(this).closest("form")[0]
  
     var d = new FormData(hh)
    if($("#InputNoncompliance").is(':checked')){
        d.append('Noncompliance', '0')
    } 
      var form = $(this).closest("form");
        $.ajax({
          url: window.location.href,
          data: d,
          dataType: 'json',
          type: 'Post',
          processData: false,
          contentType: false,
          success: function (data) {
            $("#ModalEvenement").hide()
            if (data.hasOwnProperty('evaluation')){
              location.reload()
            }
            if (data.hasOwnProperty('probleme')){
              $("#add_evenement_modal").show()
              $("[name='sous_categorie']").val("")
              $('#id_probleme').append($('<option>', {
                  value: data.probleme.id,
                  text: 'data.probleme.title'
              }));
              $('#id_probleme').val(data.probleme.id)
            }

             if (data.hasOwnProperty('mes')&&data.mes=="ok"){
              location.reload()
            }else{
              $("#ModalEvenement").show()
              $(".is-invalid").removeClass("is-invalid")
              $("small").remove()
              $.each(data.error, function(index, value){
                  $("[name="+index+"]").addClass("is-invalid").removeClass("is-valid").after("<small class='text-danger'>"+value+"</small>")
              })
            }
            if (data.hasOwnProperty('ticket')&&data.ticket=="ok"){
              location.reload()
            }else{
              $("#ModalEvenement").show()
              $(".is-invalid").removeClass("is-invalid")
              $("small").remove()
              $.each(data.error, function(index, value){
                  $("[name="+index+"]").addClass("is-invalid").removeClass("is-valid").after("<small class='text-danger'>"+value+"</small>")
              })
            }
            if(data.hasOwnProperty('deleted')){
                  location.reload()
            }
            if(data.hasOwnProperty('renamed')){
                  location.reload()
            }
            if(data.hasOwnProperty('update_ticket')){
                  location.reload()
            }
          }
        });
  })

//Update quickly details fields of ticket
function Updatedata(t){
    console.log(t)
                $.ajax({
                      url: window.location.href,
                      data: {"details": $(t).val(), "id": $(t).attr('id')},
                      dataType: 'json',
                      type: 'Post',
                      success: function (data) {
                          console.log(data)
                      }
                })

  }

//
$("button[data-bs-target='#ModalEvenement']").on("click", function(){
    $(".modal-body").find("div").hide()
    $("#add_evenement_modal").show()
    $("#add_evenement_modal").find('div').show()
    $("[name='sous_categorie']").val("")
    $("#ModalEvenementLabel").html($(this).text())
    $("#enregister").html('Enregister')
    if($(this).attr('data-bs-whatever') == 'ticket'){
        $("input[name='nature_form']").val('ticket')
        $("#ticket_modal").show("show")
        $("#ticket_modal").find('div').show("show")
    }else if($(this).attr('data-bs-whatever') == 'MES'){
        $("input[name='nature_form']").val('MES')
        $("#MES_modal").show("show")
        $("#update_ticket").show("show")
        $("#MES_modal").find('div').show("show")
    }
})
function initticketform(me){
$(".modal-body").find("div").hide()
$("#update_ticket").html()
$("#update_ticket").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
$.ajax({
url: window.location.href,
type:'post',
data: {'nature_form': 'update_ticket_init', 'id':0},
dataType: 'html',
success: function (html) {
$("#update_ticket").html(html)
$("input[name='nature_form']").val('ticket')
$("#add_evenement_modal").show("slow")
$("#update_ticket").show("slow")
$("#ModalEvenementLabel").html('Enregister un ticket')
$("#enregister").html('Enregister')
}
})
}
function deletefile(me){
$(".modal-body").find("div").hide()
$("input[name='nature_form']").val('delete_file')
$("#ModalEvenementLabel").html('Supprimer définitivement le fichier "' + $(me).attr('file_name') + '"')
$("#delete_file_input").val($(me)[0].id)
$("div[name='modal_form']").hide()
$("#delete_file_modal").show("slow" )
$("#enregister").html('Supprimer')
}
function renamefile(me){
$(".modal-body").find("div").hide()
$("input[name='nature_form']").val('rename_file')
$("#ModalEvenementLabel").html('Renommer le fichier "' + $(me).attr('file_name')+'"')
$("#rename_file_input").val($(me)[0].id)
$("#new_name").val($(me).attr('file_name'))
$("#rename_file_modal").show("slow")
$("#rename_file_modal").find('div').show("slow")
$("#enregister").html('Renommer')
}
function submit_ticket(){
var d = new FormData($("#ticket_form")[0])
if($("#InputNoncompliance").is(':checked')){
d.append('Noncompliance', '0')
}
$.ajax({
url: window.location.href,
data: d,
type: 'Post',
processData: false,
contentType: false,
success: function (data) {
if(data.even == "ok" && data.ticket=="ok"){
if(data.ticketChanged.etat == 3){
$("#ticket_" + data.ticketChanged.id).closest('tr').remove()
}
var myModal = bootstrap.Modal.getOrCreateInstance(document.getElementById('Modal'));
myModal.hide();
if ("ticketChanged" in data){
if (data['ticketChanged'] == 3){
location.reload()
}
}        
}else{
$.each(data.ticket.error, function(index, value){
              $("[name="+index+"]").addClass("is-invalid").removeClass("is-valid").after("<small class='text-danger'>"+value+"</small>")
          })
$.each(data.even.error, function(index, value){
              $("[name="+index+"]").addClass("is-invalid").removeClass("is-valid").after("<small class='text-danger'>"+value+"</small>")
          })
$.each(data.NC.error, function(index, value){
              $("[name="+index+"]").addClass("is-invalid").removeClass("is-valid").after("<small class='text-danger'>"+value+"</small>")
          })                                
}
}
})
}
function updateTicket(id){
$(".modal-body").find("div").hide()
$("#update_ticket").html()
$("#update_ticket").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
$.ajax({
url: window.location.href,
type:'post',
data: {'nature_form': 'update_ticket_init', 'id':id},
dataType: 'html',
success: function (html) {

//todo faire un message de validation
$("#update_ticket").html(html)
$("input[name='nature_form']").val('update-ticket')
$("#add_evenement_modal").show("slow" )
$("#update_ticket").show("slow" )
$("#ModalEvenementLabel").html('Mettre à jour le ticket')
$("#enregister").html('Mettre à jour')
}
})
}
function modifierGPS(){
var form = $('#GPSValider').closest("form");
$.ajax({
url: window.location.href,
type:'post',
data: form.serialize(),
dataType: 'json',
success: function (data) {
//todo faire un message de validation
console.log(data)
$('#GPS').addClass("is-valid")
}
})
}
$(document).ready(function() {
$('#GPSValider').on('click', function(){
var form = $(this).closest("form");
$.ajax({
url: window.location.href,
type:'post',
data: form.serialize(),
dataType: 'json',
success: function (data) {
//todo faire un message de validation
console.log(data)
}
})
});
});
//
$(document).on('dragover', function (e) {
    e.preventDefault();
    $('.upload-zone').on('dragover', function(event){
    if(!$(this).find('.todelete').length){
            $(this).find('p').first().after('<div class="well text-muted text-center todelete" style="padding-top: 4rem; padding-bottom: 4rem;"><i class="fa fa-arrow-down fa-4x" aria-hidden="true"></i><h3>Déposer vos fichiers ici</h3></div>')
        }
    });
    if (!$(event.target).closest('.upload-zone').length){
        $('.todelete').remove()
    }
});
$('.upload-zone').each(function () {
    var DropZone = $(this);
    var DropZone_id = DropZone[0].id.split('_')[1];
    DropZone.find('input:first').fileupload({
            dropZone: DropZone,
            dataType: 'json',
            sequentialUploads: true,

            start: function (e) {
              $("#modal-progress").modal("show");
            },

            stop: function (e) {
              $("#modal-progress").modal("hide");
            },

            progressall: function (e, data) {
              
              var progress = parseInt(data.loaded / data.total * 100, 10);
              var strProgress = progress + "%";
              $(".progress-bar").css({"width": strProgress});
              $(".progress-bar").text(strProgress);
              if (progress == 100){
                setTimeout(function(){
                    $("#modal-progress").modal("hide");
                    location.reload()
                }, 1500);
              }
            },
            done: function (e, data) {
              $('.todelete').remove()
              console.log(e, data)
              if (data.is_valid == false){

              }else{

              }

            }
    });
});
//
function alldownload(ticket_id){
    var data = "ticket_id=" + ticket_id + "&alldownload=all"
    $("#buttonAllDownload" + ticket_id).html("<i class='fas fa-sun fa-spin'></i> En téléchargement")
    $.ajax({
            url: window.location.href,
            type:'post',
            data: data,
            xhrFields:{
                responseType: 'blob'
            },
            success: function (response) {
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(response)
                    link.download = 'Ticket.zip';
                    document.body.appendChild(link);
                    link.click();
                    $("#buttonAllDownload" + ticket_id).html("<i class='fas fa-cloud-download-alt'></i> Tout télécharger")
            }

    })
}

function ShowModalImage(id, photo_id, type){
    var data = type + "_id=" + id + "&photoid=" + photo_id
    $.ajax({
            url: window.location.href,
            type:'post',
            data: data,
            dataType: 'html',
            success: function (html) {
            //todo faire un message de validation
                $(".modal-body").find("div").hide()
                $("#ModalEvenementLabel").html("<h2>Photos</h2>")
                $("#photos").html(html)
                $("#photos").show("show")
            }
    })

}

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})
//
$(document).ready(function() {
    $('textarea.textarea_update').emojioneArea({
      attributes: {
        spellcheck : true,
        autocomplete   : "on",
      },
      events: {
        change: function(editor, event) {
          txt=editor.html()
          id = $(editor).parent().parent().find('textarea')[0].id
          $($(editor).parent().parent().find('textarea')[0]).html(txt)
          Updatedata($(editor).parent().parent().find('textarea')[0])
        },
        keyup: function(editor, event) {
          txt=editor.html()
          id = $(editor).parent().parent().find('textarea')[0].id
          $($(editor).parent().parent().find('textarea')[0]).html(txt)
          Updatedata($(editor).parent().parent().find('textarea')[0])
        },
        picker_click: function(editor, event) {
          txt=editor.html()
          id = $(editor).parent().parent().find('textarea')[0].id
          $($(editor).parent().parent().find('textarea')[0]).html(txt)
          Updatedata($(editor).parent().parent().find('textarea')[0])
        }
      }
    });
  });
  var $popover = $(".BL, .devis, .CL")
  if ($popover.length){
    var popover = new bootstrap.Popover($popover)
  }
  
  $(".CL").on('click', function(){
          var CL = $(this)
          $("#offcanvasRightLabel").html("Détail du " + CL.attr('cl') + ":")
          $(".offcanvas-body").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
              $.ajax({
                   url: window.location.href,
                   data: {'CL_popover': CL.attr('cl')},
                   dataType: 'html',
                   type: 'post',
                   success: function (data) {
                      $(".offcanvas-body").html(data)
                   }
              })
  })
  
  $(".BL").on('click', function(){
          var BL = $(this)
          $("#offcanvasRightLabel").html("Détail du " + BL.attr('BL') + ":")
          $(".offcanvas-body").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
              $.ajax({
                   url: window.location.href,
                   data: {'BL_popover': BL.attr('BL')},
                   dataType: 'html',
                   type: 'post',
                   success: function (data) {
                      $(".offcanvas-body").html(data)
                   }
              })
  })
  
  $(".devis").on('click', function(){
          var devis = $(this)
          $("#offcanvasRightLabel").html("Détail du " + devis.attr('devis') + ":")
          $(".offcanvas-body").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
              $.ajax({
                   url: window.location.href,
                   data: {'devis_popover': devis.attr('devis')},
                   dataType: 'html',
                   type: 'post',
                   success: function (data) {
                      $(".offcanvas-body").html(data)
                   }
              })
  })
  
  function evalutionForm(userID){
    $.ajax({
      url: window.location.href,
      data: {'evalutionForm': userID},
      dataType: 'html',
      type: 'post',
      success: function (html) {
        $(".modal-body").find("div").hide()
        $("#ModalEvenementLabel").html("<h2>Evaluation</h2>")
        $("#enregister").html('Enregistrer')
        $("#evalutionFormDiv").html(html).fadeIn(500)      
      }
    })
  
  }
  
  function afficherCLModal(){
    $(".modal-body").find("div").hide()
    var $Modal=$("#ModalEvenement")
    $Modal.modal('show')
                        $Modal.find(".modal-title").html()
                        $Modal.find(".modal-title").html("Détail de la commande " + CL0)
                        $Modal.find("#divCL").html()
                        $Modal.find(".divCL").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
                        $Modal.modal('show')
                        $.ajax({
                            url: "/production",
                            type:'post',
                            data:{show: CL0},
                            dataType: 'html',
                            success: function (html) {
  
                            //todo faire un message de validation
                                $("#divCL").html(html)
                                $("#divCL").show()
                                $("#enregistrer").attr('name', 'update')
                                $("#enregistrer").html('Mettre à jour')
                             }
                        })
  }
  function downloadSchema(Cl_id){
    $.ajax({
                url: "/production",
                type:'post',
                data:{'downloadSchema': Cl_id},
                xhrFields:{
                    responseType: 'blob'
                },
                success: function (data) {
                    var file = new Blob([data], { type: 'application/pdf' });
                    var fileURL = URL.createObjectURL(file);
                    window.open(fileURL);
                },
                error: function(){
                    alert('error!');
                }
            })
  }
//Display bootstrap toast 
var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
      return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show())

function SeachInstallateur(pk){
  $("#installateursMap").html('<h1><i class="fas fa-sun fa-spin" style="color:black"></i></h1>')
  $.ajax({
    url: window.location.href,
    type:'post',
    data:{'searchInstallateur': pk},
    dataType: 'html',
    success: function (html) {
        $("#installateursMap").html(html)
    },
    error: function(){
        alert('error!');
    }
})

}