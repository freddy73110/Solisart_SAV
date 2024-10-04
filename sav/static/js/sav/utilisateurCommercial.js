var t_json=[]
$("#button-ticket_commercial").on("click", function(){
    var form = $(this).closest("form");
    $.ajax({
        url: window.location.href,
        type:'post',
        data: form.serialize(),
        dataType: 'html',
        success: function (data) {
             t_json= JSON.parse(data)
             var ticket_commercial_count = t_json.length
             $("#bagde-ticket_commercial").html(ticket_commercial_count )
              $('#table').bootstrapTable('load',  t_json )
                $(function() {
    $('#table').bootstrapTable()
  })
        }
    })
})
$("#button-ticket_commercial").click()