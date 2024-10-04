//Icon Installation
const fontAwesomeIcon = L.divIcon({
    html: '<span class="fa-layers fa-fw fa-4x" style="vertical-align: top;"><i class="fas fa-map-marker text-primary" style="color:black"></i><i class="fas fa-solar-panel fa-inverse" data-fa-transform="shrink-10"></i></span>',
    iconSize: [60, 48],
    iconAnchor: [30, 48],
    popupAnchor:  [0, -48],
    className: 'myDivIcon'
});
//Icon installeur
const fontAwesomeIconInstallateur = L.divIcon({
    html: '<span class="fa-layers fa-fw fa-4x" style="vertical-align: top;"><i class="fas fa-map-marker text-danger" style="color:black"></i><i class="fas fa-tools fa-inverse" data-fa-transform="shrink-10"></i></span>',
    iconSize: [60, 48],
    iconAnchor: [30, 48],
    popupAnchor:  [0, -48],
    className: 'myDivIcon'
});
// Create map with backgroud googlemaps
const mymap = L.map('map').setView([45, 0],5);
L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}).addTo(mymap);

var markersClusterInstallateur = new L.MarkerClusterGroup();
var markersClusterInstallation = new L.MarkerClusterGroup();

//To display all deptment with color of salesman
function ajoutDepartement(value, color){
    myStyle={'color':color}
    L.geoJSON(value, {
        style:myStyle
    }).addTo(mymap)
}


function onEachFeature(feature, layer, myTag) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

//add maker on maps
function generate_marker(start, stop){
    $.ajax({
                url: window.location.href,
                type:'post',
                dataType: 'json',
                data: 'start=' + start + '&stop=' + stop,
                success: function (json) {
                        L.geoJSON(json, {
                            onEachFeature: function (feature, layer) { 
                                layer.myTag = "myGeoJSONINstallation";
                                if (feature.properties && feature.properties.popupContent) {
                                    layer.bindPopup(feature.properties.popupContent);
                                }
                            },
                            pointToLayer: function (feature, latlng) {
                                return L.marker(latlng, { icon: fontAwesomeIcon});
                            },
                            filter: function(feature, layer) {
                                return feature.properties.show_on_map;
                            }
                        }).addTo(markersClusterInstallation);
                    }
            })

    mymap.addLayer(markersClusterInstallation);

}

async function load() {
        
        let url = '/static/sav/geojson/geojsonFrance.json';
        let geojsonFrance = await (await fetch(url)).json();
        color=["blue", "gray", "green", "red", "orange", "pink", "cyan", "red", "orange"]
        const profils = JSON.parse(document.getElementById('profils').textContent);
        $.each(JSON.parse(profils), function(k, v){
            $("#list_profil").append('<li style="color:' + v.color + '">'+v.user+ ' '+ v.telephone1 + '</li>')
        })
        $.each( geojsonFrance.features, function( key, value ) {
          $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes(value.properties.code)){
                ajoutDepartement(value, v.color)
            }
          })
        });

        let url2 = '/static/sav/geojson/geojsonbelgique.json';
        let geojsonBelgique = await (await fetch(url2)).json();
            $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("100")){
                ajoutDepartement(geojsonBelgique, v.color)
            }
          })

         let url3 = '/static/sav/geojson/geojsonSuisse.json';
        let geojsonSuisse = await (await fetch(url3)).json();
            $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("200")){
                ajoutDepartement(geojsonSuisse, v.color)
            }
          })
        

}

window.onload = load();

class DisplayMarker{

    installation(){

        var install_total = parseInt(document.getElementById('install_total').textContent)
        var compter=0
        var start =0
        while(install_total>compter){
            compter=compter+100
            generate_marker(start, compter)
            start=compter
        }
        

    }

    installateur(){
        $.ajax({
                url: window.location.href,
                type:'post',
                dataType: 'json',
                data: 'show=installateur',
                success: function (json) {                    
                    L.geoJSON(json, {
                            onEachFeature: function (feature, layer) { 
                                layer.myTag = "myGeoJSONINstallateur";
                                if (feature.properties && feature.properties.popupContent) {
                                    layer.bindPopup(feature.properties.popupContent);
                                }
                            },
                            pointToLayer: function (feature, latlng) {
                                return L.marker(latlng, { icon: fontAwesomeIconInstallateur});
                            },
                            filter: function(feature, layer) {
                                return feature.properties.show_on_map;
                            }
                        }).addTo(markersClusterInstallateur);
                    }
            })

        mymap.addLayer(markersClusterInstallateur);
    }
}
const $DisplayMarker = new DisplayMarker()

function search(){
    var form = $('#adresse').closest("form");
          $.ajax({
            url: window.location.href,
            type:'post',
            data: form.serialize(),
            dataType: 'html',
            success: function (html) {
                data = JSON.parse(html)
                var lat = data[0].lat
                var lon = data[0].lon
                var geojson = data[0].geojson
                L.geoJSON(geojson).addTo(mymap)
                mymap.setView(new L.LatLng(lat, lon), 12);
                }
          })

}

$('#adresse').keypress(function (e) {
 var key = e.which;
 if(key == 13)  // the enter key code
  {
    search();
    return false;
  }
});

var removeMarkers = function(tag) {
        mymap.eachLayer( function(layer) {
          if ( layer.myTag &&  layer.myTag === tag) {
            mymap.removeLayer(layer)
              }

            });

    }

$("#inputInstallateur").on("change", function(){
    if($(this).is(":checked")){
        $DisplayMarker.installateur()
        
    }else{
        removeMarkers("myGeoJSONINstallateur")
        mymap.removeLayer(markersClusterInstallateur)
        markersClusterInstallateur = new L.MarkerClusterGroup()
    }

})
$("#inputInstallation").on("change", function(){
    if($(this).is(":checked")){        
        $DisplayMarker.installation()
    }else{
        removeMarkers("myGeoJSONINstallation")
        mymap.removeLayer(markersClusterInstallation)
        markersClusterInstallation = new L.MarkerClusterGroup()
    }
})