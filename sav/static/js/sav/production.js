const group_user = JSON.parse(document.getElementById('group_user').textContent);
const pkCL = document.getElementById('pkCL').textContent.replaceAll('"', '');

var ClToDisplay =[]  
function afficherCLModal(CL){
    var $Modal=$("#ModalDiv")
                        $Modal.find(".modal-title").html()
                        $Modal.find(".modal-title").html("Détail de la commande " + CL)
                        $Modal.find(".modal-body").html()
                        $Modal.find(".modal-body").html('<h1><i class="fas fa-sun fa-spin" style="color:yellow"></i></h1>')
                        $Modal.modal('show')
                        $.ajax({
                            url: window.location.href,
                            type:'post',
                            data:{show: CL},
                            dataType: 'html',
                            success: function (html) {
                            //todo faire un message de validation
                                $Modal.find(".modal-body").html(html)
                                $("#enregistrer").attr('name', 'update')
                                $("#enregistrer").html('Mettre à jour')
                             }
                        })
}

function Dateformatter (value, row, index) {
    var v = value.slice(0, 10)
    return $("#step").val() != 'simple' ? '<input type="text" class="date_picker form-control" value=' + v + '>' : v
}

function operateFormatter(value, row, index) {
    var classlike = $("#step").val() == 'simple' ? "" : "like"

    return value == 100 ? '<a href="javascript:void(0)" class="'+classlike+'"><i class="far fa-check-circle text-success '+classlike+'"></i></a>' : '<a href="javascript:void(0)" class="'+classlike+'"><i class="far fa-circle text-danger '+classlike+'"></i></a>'
  }
function CLTabformatter(value, row, index) {
    return '<a href="javascript:void(0)" class="tabcl icon-link" onclick="afficherCLModal($(this).html())">' + value +'</a>'
}
window.operateEvents = {
    'click .like': function (e, value, row, index) {
      var v = $($(e.target).closest('a').find('svg')[0]).hasClass('text-success') ? `<a href="javascript:void(0)" class="like"><i class="far fa-circle text-danger like"></i></a>`: '<a href="javascript:void(0)" class="like"><i class="far fa-check-circle text-success like"></i></a>'
      if($($(e.target).closest('a').find('svg')[0]).hasClass('text-success')){
        $(e.target).closest('a').html('<i class="far fa-circle text-danger like"></i>')
         $.ajax({
                            url: window.location.href,
                            type:'post',
                            data: {'NotFinishedTask': JSON.stringify(row)},
                            dataType: 'json',
                            success: function (json) {
                                console.log(json)
                             }
                     })
      }else{
        $(e.target).closest('a').html('<i class="fas fa-check text-success like"></i>')
        $.ajax({
                            url: window.location.href,
                            type:'post',
                            data: {'finishTask': JSON.stringify(row)},
                            dataType: 'json',
                            success: function (json) {
                                showToast(row.name + ": terminée et sauvegardée")
                             }
                     })
      }

    }
}

if (group_user.includes('ADV')){
    $("#numCL").prop('disabled', false)
}


  $('#modalForm').submit(function(){
    $("#modalForm :disabled").removeAttr('disabled');
});
    function descriptionCL(){
        $Modalshow=new bootstrap.Modal(document.getElementById('ModalDiv'))
        var $Modal=$("#ModalDiv")
        $Modal.find(".modal-title").html()
        $Modal.find(".modal-title").html("Détail de la commande " + $("[name=numCL]").val())
        $Modal.find(".modal-body").html()
        $Modal.find(".modal-body").html('<h1><i class="fas fa-sun fa-spin" style="color:yellow"></i></h1>')
        $Modalshow.show()
        $.ajax({
            url: window.location.href,
            type:'post',
            data:{numCL:$("[name=numCL]").val()},
            dataType: 'html',
            success: function (html) {
            //todo faire un message de validation
                $Modal.find(".modal-body").html(html)
                $("#enregistrer").attr('name', 'add_CL')
                $("#enregistrer").html('Ajouter')
             }
        })
    }
function Refreshdata(){
    $.ajax({
            url: window.location.href,
            type:'post',
            data:{calendar:"full"},
            dataType: 'json',
            async: false,
            success: function (json) {
                if(window.hasOwnProperty("data")){
                    delete data
                }
                data = json  
                ganttGenerator()          
                }
        })
        
        console.log("refresh fin  ")
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

function convertdate(date){

    date_datetime = new Date(date)
    delta = date_datetime.setDate(date_datetime.getDate() - 1)
    return formatDate(delta)
}

lastScroll=0

function ganttGenerator(pkCL=null){
    
    if($("#step").val() != "simple"){
        tasks=[]        
        console.log(Date.now(), data)
        $.each(data, function(index, value){
          if (ClToDisplay.includes(value['CL'])){
            if (value['CL'] == $("#VisuCL").val() || $("#VisuCL").val() == 'tout'){
                if (value['capteur'] != 'None' && ($("#step").val() == 'tout' || $("#step").val() == 'capteur')){
                    tasks.push(
                    {
                    start: convertdate((value['date_capteur']) ? (value['date_capteur']) : value['date_capteur_prevu']),
                    end: (value['date_capteur']) ? (value['date_capteur']) : value['date_capteur_prevu'],
                    name: (value['capteur_nbre'] < 2) ? value['CL'] + ' - ' + value['installateur'] +': '+ value['capteur_nbre'] + ' Capteur ' + value['capteur'] : value['CL'] + ' - ' + value['installateur'] + ': '+ value['capteur_nbre'] + ' Capteurs ' + value['capteur'],
                    id: "capteur-"+value['CL'],
                    CL: value['CL'],
                    progress: (value['date_capteur']) ? 100 : 0
                  })
                }
                if (value['ballon'] != 'None' && ($("#step").val() == 'tout' || $("#step").val() == 'ballon')){
                    tasks.push(
                    {
                    start: convertdate((value['date_ballon']) ? (value['date_ballon']) : value['date_ballon_prevu']),
                    end: (value['date_ballon']) ? (value['date_ballon']) : value['date_ballon_prevu'],
                    name: value['CL'] + ' - ' + value['installateur'] +': ' + value['ballon'],
                    id: "ballon-"+value['CL'],
                    CL: value['CL'],
                    progress: (value['date_ballon']) ? 100 : 0
                  })
                }
                if (($("#step").val() == 'tout' || $("#step").val() == 'montage') && value['module']!= "CESI"){
                    tasks.push(
                    {
                    start: convertdate((value['date_montage']) ? (value['date_montage']) : value['date_montage_prevu']),
                    end: (value['date_montage']) ? (value['date_montage']) : value['date_montage_prevu'],
                    name: value['CL'] + ' - ' + value['installateur'] + ': Montage',
                    button: (value['jsonfile']) ?'<a href = "/assembly/'+value['id']+'" class="btn btn-outline-primary">Accéder</a>' : "",
                    id: "montage-"+value['CL'],
                    CL: value['CL'],
                    progress: (value['date_montage']) ? 100 : 0
                  })
                }
                if (($("#step").val() == 'tout' || $("#step").val() == 'carte') && value['module']!= "CESI"){
                    tasks.push(
                    {
                    start: convertdate((value['date_prepa_carte']) ? (value['date_prepa_carte']) : value['date_prepa_carte_prevu']),
                    end: (value['date_prepa_carte']) ? (value['date_prepa_carte']) : value['date_prepa_carte_prevu'],
                    name: value['CL'] + ' - ' + value['installateur'] +': Création carte régulation ',
                    id: "carte-"+value['CL'],
                    CL: value['CL'],
                    progress: (value['date_prepa_carte']) ? 100 : 0,
                    dependencies: "montage-"+value['CL']
                  })
                }
                if ($("#step").val() == 'tout' || $("#step").val() == 'prepa'){
                    tasks.push(
                    {
                    start: convertdate((value['date_prepa']) ? (value['date_prepa']) : value['date_prepa_prevu']),
                    end: (value['date_prepa']) ? (value['date_prepa']) : value['date_prepa_prevu'],
                    name: value['CL'] + ' - ' + value['installateur'] + ': Préparation commande ',
                    button: (value['jsonfile']) ?'<a href = "/assembly/'+value['id']+'" class="btn btn-outline-primary">Accéder</a>' : "",
                    id: "prepa-"+value['CL'],
                    CL: value['CL'],
                    progress: (value['date_prepa']) ? 100 : 0,
                    dependencies: ["carte-"+value['CL'], "capteur-"+value['CL'], "ballon-"+value['CL']]
                  })
                }
                if ($("#step").val() == 'tout' || $("#step").val() == 'expe'){

                    tasks.push({
                    start: convertdate(value['date_livraison']),
                    end: value['date_livraison'],
                    name: (value['transporteur']) ? value['CL'] + ' - ' + value['installateur'] + ": Livraison par " + (value['transporteur']) : value['CL'] + ' - ' + value['installateur'] + ": Livraison par ?",
                    id: "livraison-"+value['CL'],
                    CL: value['CL'],
                    progress: (new Date(value['date_livraison']) < new Date()) ? 100 : 0,
                    dependencies: "prepa-"+value['CL']
                  })
                }
                if ($("#step").val() == 'tout' || $("#step").val() == 'livraison'){
                tasks.push(
                  {
                    start: convertdate(value['date_livraison_prevu']),
                    end: value['date_livraison_prevu'],
                    name: value['CL'] + ' - ' + value['installateur'] + ': Réception client',
                    id: "reception-"+value['CL'],
                    CL: value['CL'],
                    progress: (new Date(value['date_livraison_prevu']) < new Date()) ? 100 : 0,
                    dependencies: "livraison-"+value['CL']
                  })
                }
            }
          }  
        })

    }else{
        var tasks=[]
        $.each(data, function(index, dict){
          if (ClToDisplay.includes(dict['CL'])){
            if (dict['CL'] == $("#VisuCL").val() || $("#VisuCL").val() == 'tout'){
                var values = $.map(dict, function(v, key) {return v})
                var list_date = $.map(values, function(v, key){
                    return /[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/.test(v) ? v : null;
                }).sort()
                var prog =0
                
                if(dict['ballon'] == 'None' || dict['date_ballon'] != null){
                    var prog = 20
                    if(dict['capteur_nbre'] != 0 || dict['date_capteur'] != null){
                        var prog =30
                        if(dict['module'] != "CESI" && dict['date_prepa_carte'] != null){
                            var prog =50
                            if(dict['date_prepa_prevu'] != null){
                                var prog =90
                                if(new Date(dict['date_livraison']) < new Date()){
                                    var prog =95
                                    if(new Date(dict['date_livraison_prevu']) < new Date()){
                                        var prog =100
                                    }
                                }
                            }
                        }
                    }
                }
                tasks.push(
                      {
                        start: list_date[0],
                        end: list_date.pop(),
                        name: dict['CL'] + ' - ' + dict['installateur'],
                        id: "commande-"+dict['CL'],
                        CL: dict['CL'],
                        progress: prog
                      })
                }
            }
          }
            )
    }
    var tasks2=[]
        $.each(tasks, function(index, value){
            if($("#Todo").val() == 'todo' && value.progress != 100){
                tasks2.push(value)
            }
            if($("#Todo").val() == 'done' && value.progress == 100){
                tasks2.push(value)
            }
            if($("#Todo").val() == 'all'){
                tasks2.push(value)
            }
        })
    if (tasks2.length === 0){
        $("#ganttContainer").html("<h1>Pas de données avec ces critères</h1>")
    }else{
        $("#ganttContainer").addClass("gantt-container")
        $("#ganttContainer").html("")
        if (!$("#ganttVstableur").is(":checked")){
            myChart = new Gantt(".gantt-container", tasks2, {
              view_mode: $("#inputGroupSelect01").val(),
              header_height: 50,
              column_width: 50,
              step: 24,
              bar_height: 20,
              bar_corner_radius: 3,
              arrow_curve: 5,
              padding: 18,
              date_format: 'YYYY-MM-DD',
              language: 'fr',
              custom_popup_html: function(task) {
                // the task object will contain the updated
                // dates and progress value
                end = task.end.substring(0,10)
                if (task.button){
                wrapper = task.name + task.button
                }else{
                  wrapper = task.name
                }
                if(task.progress == 100){
                  
                     return `
                <div class="details-container h-100">
                  <h5>${wrapper}</h5>
                </div>
                `;
                }else{
                     return `
                <div class="details-container h-100">
                  <h5>${wrapper}</h5>
                </div>
                `;

                }

              },
              on_click: task => {
                if (group_user.includes('ADV')){
                    afficherCLModal(task.CL)
                }
              },
              on_date_change: (task, start, end) => {
                $('#ButtonSave').addClass('beatanimation')
              },
              on_progress_change: (task, progress) => {
                if(progress == 100){
                     $.ajax({
                            url: window.location.href,
                            type:'post',
                            data: {'finishTask': JSON.stringify(task)},
                            dataType: 'json',
                            success: function (json) {
                                showToast(task.name + ": terminée et sauvegardée")
                             }
                     })

                }else{
                    $.ajax({
                            url: window.location.href,
                            type:'post',
                            data: {'NotFinishedTask': JSON.stringify(task)},
                            dataType: 'json',
                            success: function (json) {
                                console.log(json)
                             }
                     })
                }

              }
            });
            DateTop= $(".date").offset().top
            $(".gantt-container:not(#ganttContainer)").doubleScroll()
            window.onscroll = function() {
                   if(window.pageYOffset > DateTop){
                        $('.lower-text').each(function(){
                            $(this).attr('y', parseFloat($(this).attr('y')) + window.pageYOffset - lastScroll)
                        })
                        $('.upper-text').each(function(){
                            $(this).attr('y', parseFloat($(this).attr('y')) + window.pageYOffset - lastScroll)
                        })
                        $(".date").css("background-color", "white")
                        lastScroll= window.pageYOffset
                   }else{
                        $('.lower-text').each(function(){
                            $(this).attr('y', 50)
                        })
                        $('.upper-text').each(function(){
                            $(this).attr('y', 25)
                        })
                        lastScroll= window.pageYOffset
                   }
            }
            $(".popup-wrapper").css('opacity', '0')
            
            //$(".gantt-container:not(#ganttContainer)").animate({scrollLeft: $('.today-highlight').position().left}, 1500);
          }else{
            $("#ganttContainer").removeClass("gantt-container")
            $("#ganttContainer").html('<table id="table" data-toggle="table" data-custom-sort="customSort" data-search="true" '+
            '><thead><tr>'+
            '<th data-field="CL"  data-halign="center" data-align="center" data-formatter="CLTabformatter" data-sortable="true">N° CL</th>'+
            '<th data-field="name"  data-halign="center" data-align="center" data-sortable="true">Installateur</th>'+
            '<th data-field="start"  data-halign="center" data-align="center" data-sortable="true" data-formatter="Dateformatter">Date prévu</th>'+
            '<th data-field="progress"  data-halign="center" data-align="center" data-formatter="operateFormatter" data-events="operateEvents" data-sortable="true">Etat</th>'+
            '</tr></thead></table>')

            var $table = $('#table')
            $(function() {
                $table.bootstrapTable({
                    data: tasks2,
                    onPostBody: function() {
                        $("input.date_picker").datetimepicker({
                                              format: 'Y-m-d'
                                            })
                        $("input.date_picker").on("change", function(){
                            $.ajax({
                                url: window.location.href,
                                type:'post',
                                data: {'updateDate': [{
                                    'CL': $(this).closest("tr").find("td:first-child a").html(),
                                    'new': $(this).val(),
                                    'task': $(this).closest("tr").find("td:nth-child(2)").html()
                                    }]},
                                dataType: 'json',
                                success: function (json) {
                                    showToast(task.name + ": terminée et sauvegardée")
                                }
                            })

                        })
                    }
                })
            })
        }
    }
    if (pkCL){
      $("#VisuCL").val(pkCL).change()
    }  
  }

function customSort(sortName, sortOrder, data) {
    var order = sortOrder === 'desc' ? -1 : 1
    data.sort(function (a, b) {
      var aa = +((a[sortName] + '').replace(/[^\d]/g, ''))
      var bb = +((b[sortName] + '').replace(/[^\d]/g, ''))
      if (aa < bb) {
        return order * -1
      }
      if (aa > bb) {
        return order
      }
      return 0
    })
  }

function save(){
        $('#ButtonSave').removeClass('beatanimation')
        var toUpdate=[]
        $.each(myChart.bars, function(index, value){
            var end= new Date(value.task.end)
            var _end= new Date(convertdate(value.task._end))
            if (end.getDate() != _end.getDate() || end.getMonth() != _end.getMonth() || end.getYear() != _end.getYear()){
                toUpdate.push({
                    old: end.toISOString().split('T')[0],
                    new: _end.toISOString().split('T')[0],
                    CL: value.task.CL,
                    task: value.task.id
                    })

            }
        })
        $.ajax({
                    url: window.location.href,
                    type:'post',
                    data: {'updateDate': JSON.stringify(toUpdate)},
                    dataType: 'json',
                    success: function (json) {
                        console.log("Update", json)
                     }
                })


    }

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

function searchByCustomer(){
 $.ajax({
                    url: window.location.href,
                    type:'post',
                    data: {'searchByCustomer': $("#client").val()},
                    dataType: 'json',
                    success: function (datal) {
                        $("#commercial").val("tout")
                        ClToDisplay = datal.map((x) => x.CL)
                        var html='<option value="tout" selected="">Visualiser tous les CL</option>'
                        $.each(datal, function(i, v){
                          html = html + "<option value='"+ v.CL+"'>"+ v.CL +" - " + v.installateur + "</option>"
                        })
                        $("#VisuCL").html(html)
                        ganttGenerator()
                     }
                })

}

function searchByCommercial(pkCL=null){
 $.ajax({
                    url: window.location.href,
                    type:'post',
                    data: {'searchByCommercial': $("#commercial").val()},
                    dataType: 'json',
                    success: function (datal) {
                        $("#client").val("tout")
                        ClToDisplay = datal.map((x) => x.CL)
                        var html='<option value="tout" selected="">Visualiser tous les CL</option>'
                        $.each(datal, function(i, v){
                          html = html + "<option value='"+ v.CL+"'>"+ v.CL +" - " + v.installateur + "</option>"
                        })
                        $("#VisuCL").html(html)
                        ganttGenerator(pkCL)
                     }
                })                
}

Refreshdata()
setTimeout(function () {
     searchByCommercial(pkCL)
,5000})



     const socket = new WebSocket('ws://'+window.location.host+'/ws/production/');
        socket.onmessage = (e) => {
            var d = JSON.parse(e.data)
            var d = d.message
            if (d.hasOwnProperty("message")) {
                var message = d.message;
                if(message == "Création d'une nouvelle commande"){
                  showToast(message)
                  $("#modal-progress").find(".modal-title").html("<h4>En cours de travail...</h4>")
                  $("#modal-progress").find(".modal-body").css({ opacity: 0.5 })
                  $("#modal-progress").find(".modal-body").addClass("text-center")
                  $("#modal-progress").find(".modal-body").html("<i class='fas fa-spinner fa-pulse fa-10x text-primary'></i>")
                  $("#modal-progress").modal('show')
                  window.location.reload();
                }else if (d.datereceptionclient){
                    if (data.result.length == 0){
                        message = message + '<br> Pas de date de livraison modifiée sur Héraklès'
                    }else{
                        message = message + "<br>Date de livraison modifiée:"
                        $.each(d.result, function(index, value){
                            message = message + '<li>' + value.Name + '</li>'
                        })
                    }
                }else{
                    message = message + "<br>Date modifié:"
                        $.each(d.result, function(index, value){
                            message = message + '<li>' + value + '</li>'
                        })
                }
                showToast(message)
                if ($("#ButtonSave").hasClass('beatanimation') && d.result.length != 0){
                    $('#alertMessageId').append(
                        '<div class="alert alert-warning alert-dismissible fade show" role="alert">' +
                          '<strong><i class="fas fa-exclamation-triangle"></i></strong> ' + message +
                          '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                        '</div>'
                    )
                }else{
                    console.log("refreshdata dans ws")
                    Refreshdata()
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
        
        $(function () {
            var today = new Date();
            var date = (today.getDate())+'-'+(today.getMonth()+1)+ '-'+ today.getFullYear()+ ' ' + today.getHours()+ ':' + today.getMinutes();
             $("input[name='date_information']").val(today.
                      toLocaleString('fr-fr', {year: 'numeric', month: '2-digit', day: '2-digit'}).
                      replace(/(\d+)\/(\d+)\/(\d+)/, '$1-$2-$3') + " " + today.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }))
            $("input[name='date_information']").datetimepicker({
              format: 'd-m-Y H:i'
            }
            );
          });
          $("input[name='date_information']").val($("input[name='date_information']").val().substring(0,16).replace('\/', '-').replace('\/', '-'))
          function CheckUpdateInformation(){
            $(".offcanvas-body").html('<h1><i class="fas fa-sun fa-spin" style="color:yellow"></i></h1>')
             $.ajax({
                url: window.location.href,
                type:'post',
                data:{date_information:$("#date_information").val()},
                dataType: 'html',
                success: function (html) {
                    $("#offcanvasRightLabel").html('Modifications de commentaire depuis le ' + $("#date_information").val())
                    $(".offcanvas-body").html(html)
                 }
            })

          }