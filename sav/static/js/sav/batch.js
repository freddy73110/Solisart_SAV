function UpdateModalBatch(pk, elem){
    $("#modalBody").html('<h1 class="m-auto"><i class="fas fa-sun fa-spin m-auto" style="color:yellow"></i></h1>')
    $.ajax({
        url: window.location.href,
        type:'post',
        data: {updateModal: pk},
        dataType: 'html',
        success: function (html) {
            $("#modalBody").html(html)
            var bat = $(elem).closest('tr').find('img').attr('alt')
            $("#ModalEvenementLabel").html('Mettre à jour du lot ' + bat)                
            $("#enregistrer").html('Mettre à jour')
            $("#enregistrer").attr('name', "update")
            $("#enregistrer").show()
        }
    })
}
function AddBashModal(){
    $("#modalBody").html('<h1 class="m-auto"><i class="fas fa-sun fa-spin m-auto" style="color:yellow"></i></h1>')
    $.ajax({
        url: window.location.href,
        type:'post',
        data: {AddBashModal: ""},
        dataType: 'html',
        success: function (html) {
            $("#modalBody").html(html)
            $("#ModalEvenementLabel").html('Créer un nouveau lot')                
            $("#enregistrer").html('Ajouter')
            $("#enregistrer").attr('name', "add")
            $("#enregistrer").show()

        }
    })

}
function AddArticleBashModal(){
    $("#modalBody").html('<h1 class="m-auto"><i class="fas fa-sun fa-spin m-auto" style="color:yellow"></i></h1>')
    $.ajax({
        url: window.location.href,
        type:'post',
        data: {AddArticleBashModal: ""},
        dataType: 'html',
        success: function (html) {
            $("#modalBody").html(html)
            $("#ModalEvenementLabel").html('Ajouter un article à gérer par lot')                
            $("#enregistrer").html('Ajouter')
            $("#enregistrer").attr('name', "addArticle")
            $("#enregistrer").show()

        }
    })

}
function link(pk, elem){
    var pk = pk
    $("#modalBody").html('<h1 class="m-auto"><i class="fas fa-sun fa-spin m-auto" style="color:yellow"></i></h1>')
    $.ajax({
        url: window.location.href,
        type:'post',
        data: {link: pk},
        dataType: 'html',
        success: function (html) {
            $("#modalBody").html(html)
            var bat = $(elem).closest('tr').find('img').attr('alt')
            $("#ModalEvenementLabel").html('Liste des installations en lien avec le lot ' + bat)                
            $("#enregistrer").html('Don t touch')
            $("#enregistrer").attr('name', "")
            $("#enregistrer").hide()
        }
    })
}

function printModal(pk, elem){
    var pk = pk
    var bat = $(elem).closest('tr').find('img').attr('alt')
    $("#ModalEvenementLabel").html('Nombre d etiquette pour ' + bat) 
    $("#enregistrer").html('Imprimer')
    $("#enregistrer").attr('name', "print")
    $("#enregistrer").show()
    $("#modalBody").html('<h1 class="m-auto"><i class="fas fa-sun fa-spin m-auto" style="color:yellow"></i></h1>')
    $.ajax({
        url: window.location.href,
        type:'post',
        data: {printModal: pk},
        dataType: 'html',
        success: function (html) {
            $("#modalBody").html(html)

        }
    })

    // $.ajax({
    //     url: window.location.href,
    //     type:'post',
    //     data: {print: pk},
    //     dataType: 'html',
    //     success: function (html) {
    //         $("#modalBody").html(html)
                          
    //         $("#enregistrer").html('Don t touch')
    //         $("#enregistrer").attr('name', "")
    //         $("#enregistrer").hide()
    //     }
    // })
}