$(document).ready(function(){
    $("#id_instal, #telephone, #prenom, #nom, #email, #id_code_postale_install, #id_ville_install, #id_BL, #id_CL, #id_Devis").on("keypress", function(e) {
         var key = e.which;         
         if(key == 13)  // the enter key code
          {
            var t = $(this)
            var inputSend = $(this).closest("form").find('input')
            $.each($('input[type=text]'), function(idx, elem){
                if (inputSend.index(elem)>-1) {                    
                }else{
                    $(elem).val("").removeClass('is-valid')
                }
            })
            send(t)
          }
    })

})
function send(t){
    if (t.val().length>2){
        $("#resultat").html('<h1 class="text-center m-3" style="font-size: 8em; color:yellow"><i class="fas fa-sun fa-spin" style="{color:yellow}"></i></h1>')
        $(".invalid-feedback").remove()
        t.addClass("is-valid").removeClass('is-invalid')
          var form = t.closest("form");
          $.ajax({
            url: window.location.href,
            type:'post',
            data: form.serialize(),
            dataType: 'html',
            success: function (html) {
                $("#resultat").html()
                $("#resultat").html(html)
                }
          })
    }else{
        t.addClass("is-invalid").removeClass('is-valid')
        t.after("<div class='invalid-feedback'>Ce champ doit comporté 2 caractères au minimum.</div>")
    }
}
$("input").hover(function(){
    $(this).closest(".input-group").toggleClass("shadow")
})