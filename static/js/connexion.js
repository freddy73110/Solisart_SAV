function afficheConnexion(configInstantane){
    $("#SN").val(configInstantane['serial'])
    $("#nomInstallation").val(configInstantane['srv_id'])
    $("#adresseMac").val(configInstantane['config_mac'])
    $("#adresseIP").val(configInstantane['ip(0)']+'.'+configInstantane['ip(1)']+'.'+configInstantane['ip(2)']+'.'+configInstantane['ip(3)'])
    $("#sousReseau").val(configInstantane['sub(0)']+'.'+configInstantane['sub(1)']+'.'+configInstantane['sub(2)']+'.'+configInstantane['sub(3)'])
    $("#Passerelle").val(configInstantane['gw(0)']+'.'+configInstantane['gw(1)']+'.'+configInstantane['gw(2)']+'.'+configInstantane['gw(3)'])
    $("#DNS1").val(configInstantane['pdn(0)']+'.'+configInstantane['pdn(1)']+'.'+configInstantane['pdn(2)']+'.'+configInstantane['pdn(3)'])
    $("#DNS2").val(configInstantane['sdn(0)']+'.'+configInstantane['sdn(1)']+'.'+configInstantane['sdn(2)']+'.'+configInstantane['sdn(3)'])
}

function Ajoututilisateur(){
    $("#Modal").find(".modal-title").html("Ajout d'un nouvel utilisateur")
    modalBody = '<div class="row">'
    +'<div class="col-12">'
    +'<div class="input-group mb-3">'
    +'<span class="input-group-text"><i class="fas fa-user"></i></span>'
    +'<div class="form-floating">'
    +'<input type="text" class="form-control">'
    +'<label>Nom</label>'
    +'</div>'
    +'<div class="form-floating">'
    +'<input type="text" class="form-control">'
    +'<label>Prénom</label>'
    +'</div>'
    +'</div>'
    +'</div>'
    +'<div class="col-12">'
    +'<div class="input-group mb-3">'
    +'<span class="input-group-text"><i class="fas fa-map-marker-alt"></i></span>'
    +'<div class="form-floating">'
    +'<input type="text" class="form-control">'
    +'<label>Adresse 1</label>'
    +'</div>'
    +'</div>'
    +'</div>'
    +'<div class="col-12">'
    +'<div class="input-group mb-3">'
    +'<span class="input-group-text"><i class="fas fa-map-marker-alt"></i></span>'
    +'<div class="form-floating">'
    +'<input type="text" class="form-control">'
    +'<label>Adresse 2</label>'
    +'</div>'
    +'</div>'
    +'</div>'
    +'<div class="col-12">'
    +'<div class="input-group mb-3">'
    +'<span class="input-group-text"><i class="fas fa-map"></i></span>'
    +'<div class="form-floating">'
    +'<input type="text" class="form-control">'
    +'<label>CP</label>'
    +'</div>'
    +'<div class="form-floating">'
    +'<input type="text" class="form-control">'
    +'<label>Ville</label>'
    +'</div>'
    +'</div>'
    +'</div>'
    +'<div class="col-6">'
    +'<div class="input-group mb-3">'
    +'<span class="input-group-text"><i class="fas fa-users"></i></span>'
    +'<div class="form-floating">'
    +'<select class="form-select">'
    /*Avec les option en fct du niveau du profil soit égal ou inférieur [admin, technicien, installateur, proprio, locataire] */
    +'<option>Propriétaire</option>'
    +'<option>Locataire Zone 1</option>'
    +'<option>Locataire Zone 2</option>'
    +'</select>'
    +'<label>Profil</label>'
    +'</div>'
    +'</div>'
    +'</div>'
    +'</div>'
    $("#Modal").find(".modal-body").html(modalBody)
    $("#Modal").find("button").last().html('<i class="fas fa-user-plus"></i> Ajouter')
}