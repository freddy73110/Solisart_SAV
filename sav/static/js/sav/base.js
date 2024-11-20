//pass csrftoken for all ajax request for all pages
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({   headers: {  "X-CSRFToken": csrftoken  }  });

//No use
$(".alert-success").fadeTo(4000, 500).slideUp(500, function() {
    $(".alert-success").alert('close')
})

//to wait after click on icon link
$(".snipperclick").on('click', function(){
    $("#modal-progress").find(".modal-title").html("<h4>En cours de travail...</h4>")
    $("#modal-progress").find(".modal-body").css({ opacity: 0.5 })
    $("#modal-progress").find(".modal-body").addClass("text-center")
    $("#modal-progress").find(".modal-body").html("<i class='fas fa-spinner fa-pulse fa-10x text-primary'></i>")
    $("#modal-progress").modal('show')
})

//add it to bootstrap popover work
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
return new bootstrap.Popover(popoverTriggerEl)
})

if($('html').attr('data-bs-theme')=="dark"){
    $("button.btn").css({'color': '#BFB306 !important'});
    $("button.btn").hover({'color': 'black !important'})
}else{
    $("button.btn").css({'color': 'black'});
}
