function modaldisplay(t){

    $.ajax({
        url: "/api/tickets/" + t.id.split("_")[1],
            type:'get',
            success: function (json) {
                console.log(json)
                $("#ModalLabel").html("Modifier sur le ticket de l'installation: " + json.instal)
            }
})
    var id=$(t)[0].id.replace('ticket_', '')
    text = $($($(t).closest('tr').find('td')[0]).find('a')[0]).html()
    $("#ModalLabel").html("Modifier sur le ticket de l'installation: " + text)
    $.ajax({
        url: window.location.href,
            type:'post',
            data: {'nature_form': 'update_ticket_init', 'id':id},
            dataType: 'html',
            success: function (html) {
                $("#ticket_form").html(html)
            }
})
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