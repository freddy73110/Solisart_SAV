$(function () {
    var today = new Date();
    today.setDate(today.getDate() - 30)
    var date = (today.getDate())+'-'+(today.getMonth()+1)+ '-'+ today.getFullYear()+ ' ' + today.getHours()+ ':' + today.getMinutes();
    $("input[name='date_start_BL']").val(today.
              toLocaleString('fr-fr', {year: 'numeric', month: '2-digit', day: '2-digit'}).
              replace(/(\d+)\/(\d+)\/(\d+)/, '$1-$2-$3') + " " + today.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }))
    $("input[name='date_start_BL']").datetimepicker({
      format: 'd-m-Y H:i'
    }
    );
  });
  $("input[name='date_start_BL']").val($("input[name='date_start_BL']").val().substring(0,16).replace('\/', '-').replace('\/', '-'))

  $(function () {
    var today = new Date();
    var date = (today.getDate())+'-'+(today.getMonth()+1)+ '-'+ today.getFullYear()+ ' ' + today.getHours()+ ':' + today.getMinutes();
     $("input[name='date_end_BL']").val(today.
              toLocaleString('fr-fr', {year: 'numeric', month: '2-digit', day: '2-digit'}).
              replace(/(\d+)\/(\d+)\/(\d+)/, '$1-$2-$3') + " " + today.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }))
    $("input[name='date_end_BL']").datetimepicker({
      format: 'd-m-Y H:i'
    }
    );
  });
  $("input[name='date_end_BL']").val($("input[name='date_end_BL']").val().substring(0,16).replace('\/', '-').replace('\/', '-'))

  var $table = $('#table')
  var data = JSON.parse(document.getElementById('data1').textContent);
    $table.bootstrapTable({data: data})
  function refreshBLStat(t){
    form = $("#form_BL")
    data =  form.serialize()
    $(t).html("Attente de résulat")
    $.ajax({
                        url: window.location.href,
                            type:'post',
                            data: data + "&refreshBL=refreshBL",
                            dataType: 'json',
                            success: function (data) {
                                    $(t).html("Visualiser")
                                    $('#table').bootstrapTable('load', data)
                            }
                    })

  }
  function codouvFooter() {
    return 'Total sous garantie'
  }
    function remiseFooter() {
    return '100 %'
  }
  function totalFooter(data) {
    var field = this.field
    var total = 0
    $.each(data, function(key, val){
        if(val.remisepct == 100){
            total = total + val.prixunitaire * val.qtet
        }
    })
    return  Math.round(total * 100) / 100 + " €"
  }

  function footerStyle(column) {
    return {
      codouv: {
        css: {'text-transform': 'uppercase'}
      }
    }[column.field]
  }

function priceFormatter(value) {
    var valuemonnaie = Math.round(value * 100) / 100
    return valuemonnaie + " €"
  }
function pctFormatter(value) {

    return value+ " %"
  }
   function rowStyle(row, index) {
    if (row.remisepct == 100) {
      return {
              css: {
                'font-weight': 'bold',
                'color': 'red'
              }
            }
    }else{
        return {
            classes: "text-center"
        }
    }

  }

  function ajaxRequest(params) {
    var url = 'api/NC'
    $.get(url).then(function (res) {
      params.success({                                  
        "rows": res,
        "total": res.lenght
    },null,{})
    })
  }
  function avoirFormat(value){
    if(value){
      return '<i class="fas fa-dollar-sign text-danger"></i>'
    }else{
      return ''
    }
  }
  function dateFormat(value){
    dd = new Date(value)
    return dd.toLocaleString()
  }


  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})
    function visualiser(t){
        var $t =$(t)
        $t.html('<i class="fas fa-spinner fa-pulse"></i> Visualiser')
        var form= $t.closest("form");
        data =  form.serialize()
        if(data.includes('field')){
            data=data+'&type=bar'
        }
        $.ajax({
        url: window.location.href,
            type:'post',
            data: data,
            dataType: 'html',
            success: function (html) {
                if (data.includes("pbcause")){
                    $("#sunburst2").html(html)
                    $("#button-form2").html("Visualiser")
                }else{
                    $("#tickets_chart").html(html)
                    $.ajax({
                        url: window.location.href,
                            type:'post',
                            data: form.serialize() + "&type=sunburst",
                            dataType: 'html',
                            success: function (html) {
                                    $("#sunburst").html(html)
                            }
                    })
                    $("#button-form").html("Visualiser")
                }
            }
    })
}

function genetableau(t){
        var $t =$(t)
        $t.html('<i class="fas fa-spinner fa-pulse"></i> <i class="fas fa-table"></i> Tableau')
        var form= $t.closest("form");
        data =  form.serialize() + '&tableau=True'
        $("#sunburst2").html()
        $.ajax({
        url: window.location.href,
            type:'post',
            data: data,
            dataType: 'html',
            success: function (html) {
                $("#sunburst2").html(html).attr("tabindex",-1).focus()
                $("#buttongeneretableau").html('<i class="fas fa-table"></i> Tableau')
            }
    })
    }
    function Actionbouton_problem(t){
    if($(t).html()== 'Tout sélectionner'){
        $("input[name=probleme]").prop('checked', true)
        $(t).html('Tout déselectionner')
    }else{
        $("input[name=probleme]").prop('checked', false)
        $(t).html('Tout sélectionner')
    }
    }
        function Actionbouton_cause(t){
    if($(t).html()== 'Tout sélectionner'){
        $("input[name=cause]").prop('checked', true)
        $(t).html('Tout déselectionner')
    }else{
        $("input[name=cause]").prop('checked', false)
        $(t).html('Tout sélectionner')
    }
    }
function Actionbouton_BL(t){
    if($(t).html()== 'Tout sélectionner'){
        $("input[name=article_BL]").prop('checked', true)
        $(t).html('Tout déselectionner')
    }else{
        $("input[name=article_BL]").prop('checked', false)
        $(t).html('Tout sélectionner')
    }
    }
