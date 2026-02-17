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
// Create map 
const mymap = L.map('map',{
  attributionControl: false
}).setView([45, 0],5);
const googleMaps = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3'],
  crossOrigin: true})



// Fond OpenStreetMap
const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap',
  crossOrigin: true
});

// Fond satellite (Exemple Esri)
const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: '© Esri',
  crossOrigin: true
});

const CartoDB = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  crossOrigin: true})

// Sombre
const CartoDBDark =L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  crossOrigin: true})

const whiteTiles = L.tileLayer('', {
  attribution: '',
  minZoom: 0,
  maxZoom: 22,
  tileSize: 256
});

// Open map with CartoDB than background
CartoDB.addTo(mymap);

//Add all background map
L.control.layers({
  "OpenStreetMap": osm,
  "Satellite": satellite,
  "Google Maps": googleMaps,
  "CartoDB": CartoDB,
  "CartoDB Dark": CartoDBDark,
  "Fond blanc" :whiteTiles
}).addTo(mymap);

//Create Regroup markers
var markersClusterInstallateur = new L.MarkerClusterGroup();
var markersClusterInstallation = new L.MarkerClusterGroup();
let geoGroup = L.layerGroup().addTo(mymap)

function getColor(d) {
  return d > 95 ? '#a50f15' : // 100
         d > 90 ? '#de2d26' :
         d > 85 ? '#fb6a4a' :
         d > 80 ? '#fc9272' :
         d > 75 ? '#7f2704' :
         d > 70 ? '#a63603' :
         d > 65 ? '#d94801' :
         d > 60 ? '#f16913' :
         d > 55 ? '#fd8d3c' :
         d > 50 ? '#fdae6b' :
         d > 45 ? '#fdd0a2' :
         d > 40 ? '#08306b' :
         d > 35 ? '#08519c' :
         d > 30 ? '#2171b5' :
         d > 25 ? '#4292c6' :
         d > 20 ? '#6baed6' :
         d > 15 ? '#9ecae1' :
         d > 10 ? '#c6dbef' :
         d > 5  ? '#deebf7' :
                  '#f7fbff'; // très faible densité
}

//Pour générer le nuancier

  const colors = [
    '#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6',
    '#4292c6', '#2171b5', '#08519c', '#08306b', '#fdd0a2',
    '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603',
    '#7f2704', '#fc9272', '#fb6a4a', '#de2d26', '#a50f15'
  ];

  function GenerateNuancier(max, unit){

    const container = document.getElementById("nuancier");

    colors.forEach((color, i) => {
        const wrapper = document.createElement("div");
        wrapper.style.display = "flex";
        wrapper.style.flexDirection = "column";
        wrapper.style.alignItems = "center";

        const box = document.createElement("div");
        box.className = "nuance";
        box.style.backgroundColor = color;

        const label = document.createElement("div");
        label.className = "label";
        label.textContent = Math.round((i / (colors.length - 1)) * max);

        wrapper.appendChild(box);
        wrapper.appendChild(label);
        container.appendChild(wrapper);
    });

    $("#unite").html(unit)
}

function style(density,densityMax, color) {
  return {
    fillColor: getColor(parseFloat(density)/parseFloat(densityMax)*100),
    weight: 3,
    opacity: 1,
    color: color,
    fillOpacity: 1
  };
}

//To display all deptment with color of salesman
function ajoutDepartement(value, color, varCode, density){
    var code = varCode != 0 ? varCode : value.properties.code
    switch (density){
        case undefined :
            myStyle={'color':color}
            geo = L.geoJSON(value, {
                style:myStyle
            }).addTo(geoGroup)
            var center = geo.getBounds().getCenter(); // Centre approximatif

            // Création d'un divIcon pour afficher juste du texte
            var label = L.divIcon({
            className: 'dep-label',
            html: `<div style="color: ${color}" class="dep-text">${code}</div>`, // ou code_insee selon ton fichier
            iconAnchor: [7, 7],
            iconSize: null, // Important pour ne pas réserver de place inutile
            code : code
            });

            // Ajout de l’étiquette sur la carte
            let marker
            switch (varCode){
                case 0 :
                    marker = L.marker(center, { icon: label }).addTo(mymap).bindPopup('<b>Département ' + value.properties.nom +  ' (' + code +') :</b>');
                    tableData.data.push(
                        {
                            dept:value.properties.nom, 
                            code:value.properties.code,
                            surface: (turf.area(value)/1000000).toFixed(2)
                        }
                    )
                    break;
                case 100 :
                    marker = L.marker(center, { icon: label }).addTo(mymap).bindPopup('<b>Belgique (' + code +') :</b>');
                                tableData.data.push(
                        {
                            dept:"Belgique", 
                            code: 100,
                            surface: 30688
                        }
                    )
                    break;
                case 200 :
                    marker = L.marker(center, { icon: label }).addTo(mymap).bindPopup('<b>Suisse (' + code +') :</b>');
                    tableData.data.push(
                        {
                            dept:"Suisse", 
                            code: 200,
                            surface: 41285
                        }
                    )
                    break;
                case 300 :
                    marker = L.marker(center, { icon: label }).addTo(mymap).bindPopup('<b>Luxembourg (' + code +') :</b>');
                    tableData.data.push(
                        {
                            dept:"Luxembourg", 
                            code: 300,
                            surface: 2586
                        }
                    )
                    break;
                case 1000:
                    break
            }

            geo.on("mouseout", function (e) {
            geo.closePopup();
            });
            geo.on("click", function (e) {
            marker.openPopup();
            });
            break
        case "installationDensity":
            L.geoJSON(value, {
                style:style(value.properties.installationDensity, DensityInstallationMax, color)
            }).addTo(geoGroup)
            break
        case "installateurDensity":
            L.geoJSON(value, {
                style:style(value.properties.installateurDensity, DensityInstallateurMax, color)
            }).addTo(geoGroup)
            break
        case "rapport":
            L.geoJSON(value, {
                style:style(value.properties.rapport, rapportMax, color)
            }).addTo(geoGroup)
            break
    }

}


function onEachFeature(feature, layer, myTag) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

//add maker on maps
function generate_marker(start, stop) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: window.location.href,
            type: 'post',
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
                        return L.marker(latlng, { icon: fontAwesomeIcon });
                    },
                    filter: function(feature, layer) {
                        return feature.properties.show_on_map;
                    }
                }).addTo(markersClusterInstallation);

                mymap.addLayer(markersClusterInstallation);

                resolve(); // ✅ la promesse est terminée
            },
            error: function (xhr, status, error) {
                reject(error); // ⚠️ important pour gérer les erreurs
            }
        });
    });
}
var profils //list texte des commerciaux à convertir en json
var DensityInstallationMax = 0
var DensityInstallateurMax = 0
var rapportMax = 0
async function load() {
        
        let url = '/static/sav/geojson/geojsonFrance.json';
        geojsonFrance = await (await fetch(url)).json();
        profils = JSON.parse(document.getElementById('profils').textContent);
        $.each(JSON.parse(profils), function(k, v){
            $("#list_profil").append('<li style="color:' + v.color + '">'+v.user+ ' '+ v.telephone1 + '</li>')
        })
        $.each(geojsonFrance.features, function( key, value ) {
          $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes(value.properties.code)){
                ajoutDepartement(value, v.color, 0)
            }
          })
        });

        let url2 = '/static/sav/geojson/geojsonbelgique.json';
        geojsonBelgique = await (await fetch(url2)).json();
            $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("100")){
                ajoutDepartement(geojsonBelgique, v.color, 100)
            }
          })

         let url3 = '/static/sav/geojson/geojsonSuisse.json';
        geojsonSuisse = await (await fetch(url3)).json();
            $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("200")){
                ajoutDepartement(geojsonSuisse, v.color, 200)
            }
          })
          let url4 = '/static/sav/geojson/geojsonLuxembourg.json';
        geojsonLuxembourg = await (await fetch(url4)).json();
            $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("300")){
                ajoutDepartement(geojsonLuxembourg, v.color, 300)
            }
          })
        $('#table').bootstrapTable(tableData)
        

}

window.onload = load();

class DisplayMarker{

    async installation(){

        var install_total = parseInt(document.getElementById('install_total').textContent)
        var compter=0
        var start =0
        var json = []
        let promises = [];
        //To display marker by group 
        while(install_total>compter){
            compter=compter+100
            promises.push(generate_marker(start, compter))
            start=compter
        }

        //wait all marker display
        await Promise.all(promises);
        
        tableData.columns.push(
                        {
                field: 'installation',
                title: "Nombre d'installation",
                sortable: true,
                align: 'center'
            },{
                field: 'densInstallation',
                title: "Densité d'installation<br>(installation/1 000km²)",
                sortable: true,
                align: 'center'
            }
        )
        if("installateurDensity" in geojsonFrance.features[0].properties){
            tableData.columns.push(
                        {
                field: 'rapport',
                title: "rapport<br>(installation/installateur)",
                sortable: true,
                align: 'center'
            })
        }
        var density
        //count installation by french's departments
        $.each( window.geojsonFrance.features, function( key, value ) {
                                    const polygon = value

                                    let count = 0;                                    
                                    
                                    markersClusterInstallation.getLayers().forEach(marker => {
                                        if (marker.myTag
                                        && marker.myTag == "myGeoJSONINstallation"){
                                            const point = turf.point(marker.feature.geometry.coordinates);
                                            if (turf.booleanPointInPolygon(point, polygon)) {
                                                count++;
                                            }
                                    }
                                    });
                                    tableData.data.forEach(o => {
                                        if (o.code === value.properties.code) {
                                            o.installation = count;
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallation = density
                                            if("installateurDensity" in value.properties){
                                                o.rapport = value.properties.installateurDensity != 0 ? (density/value.properties.installateurDensity).toFixed(2) : 0
                                            }                                            
                                        }
                                        }); 
                                    value.properties.installationDensity = density
                                    if("installateurDensity" in value.properties){
                                        value.properties.rapport = value.properties.installateurDensity != 0 ? (density/value.properties.installateurDensity).toFixed(2) : 0
                                        rapportMax = parseFloat(value.properties.rapport) > parseFloat(rapportMax) ? parseFloat(value.properties.rapport) : parseFloat(rapportMax)
                                    }
                                    if(parseFloat(density) > parseFloat(DensityInstallationMax)){
                                        DensityInstallationMax = parseFloat(density)
                                    }
                                    
                                    
                                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == value.properties.code;
                                    });

                                    filtered.forEach(marker => {
                                        if (!marker._popup._content.includes("installation")){
                                            if (count > 1){
                                            marker.setPopupContent(marker._popup._content + '<li>'+ count +' installations ('+  density+' installation/1 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installation ('+  density+' installation/1 000km²)</li>');
                                            }
                                        }
                                    });
                                    });
                                    
                    

                                 
                    // Pour compter le nombre d'installation pour la Belgique    
                    let count = 0;
                    $.each( window.geojsonBelgique.features, function( key, value ) {
                                    const polygon = value
                                    markersClusterInstallation.getLayers().forEach(marker => {
                                        if (marker.myTag
                                        && marker.myTag == "myGeoJSONINstallation"){
                                            const point = turf.point(marker.feature.geometry.coordinates);
                                            if (turf.booleanPointInPolygon(point, polygon)) {
                                                count++;
                                            }
                                    }
                                    });                                   
                    }); 
                    tableData.data.forEach(o => {
                                        if (o.code === 100) {
                                            o.installation = count;
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallation = density
                                        }
                                        }); 
                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == 100;
                                    });

                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (!marker._popup._content.includes("installation")){
                                            if (count > 1){
                                            marker.setPopupContent(marker._popup._content + '<li>'+ count +' installations ('+  density+' installation/1 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installation ('+  density+' installation/1 000km²)</li>');
                                            }
                                        }
                                    });
                        
                    //Pour compter le nombre d'installation pour la Suisse
                    count = 0;
                    $.each( window.geojsonSuisse.features, function( key, value ) {
                                    const polygon = value
                                    
                                    markersClusterInstallation.getLayers().forEach(marker => {
                                        if (marker.myTag
                                        && marker.myTag == "myGeoJSONINstallation"){
                                            const point = turf.point(marker.feature.geometry.coordinates);
                                            if (turf.booleanPointInPolygon(point, polygon)) {
                                                count++;
                                            }
                                    }
                                    });                                  
                    }); 
                    tableData.data.forEach(o => {
                                        if (o.code === 200) {
                                            o.installation = count;
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallation = density
                                        }
                                        });  
                    
                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == 200;
                                    });

                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (count > 1){
                                            marker.setPopupContent(marker._popup._content + '<li>'+ count +' installations ('+  density+' installation/1 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installation ('+  density+' installation/1 000km²)</li>');
                                            }
                                    });   
                    //Pour compter le nombre d'installation pour le Luxembourg
                    count = 0;
                    $.each( window.geojsonLuxembourg.features, function( key, value ) {
                                    const polygon = value
                                    
                                    markersClusterInstallation.getLayers().forEach(marker => {
                                        if (marker.myTag
                                        && marker.myTag == "myGeoJSONINstallation"){
                                            const point = turf.point(marker.feature.geometry.coordinates);
                                            if (turf.booleanPointInPolygon(point, polygon)) {
                                                count++;
                                            }
                                    }
                                    });                                  
                    }); 
                    tableData.data.forEach(o => {
                                        if (o.code === 300) {
                                            o.installation = count;
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallation = density
                                        }
                                        });  
                    
                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == 300;
                                    });

                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (count > 1){
                                            marker.setPopupContent(marker._popup._content + '<li>'+ count +' installations ('+  density+' installation/1 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installation ('+  density+' installation/1 000km²)</li>');
                                            }
                                    });
                    $('#table').bootstrapTable('destroy')                  
                    $('#table').bootstrapTable(tableData)
                    $("#DensityInstallation").prop('disabled', false); 
                    if("installateurDensity" in geojsonFrance.features[0].properties){
                        $("#rapport").prop('disabled', false);
                    }
                                   

    }

    installateur(){
        tableData.columns.push(
                        {
                field: 'installateur',
                title: "Nombre d'installateur",
                sortable: true,
                align: 'center'
            },{
                field: 'densInstallateur',
                title: "Densité d'installateur<br>(installateur/10 000km²)",
                sortable: true,
                align: 'center'
            }
        )
        if("installationDensity" in geojsonFrance.features[0].properties){
            tableData.columns.push(
                        {
                field: 'rapport',
                title: "rapport<br>(installation/installateur)",
                sortable: true,
                align: 'center'
            })
        }
        var density
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
                    //Pour compter le nombre de marker par département français                    

                    $.each( window.geojsonFrance.features, function( key, value ) {
                                    const polygon = value

                                    let count = 0;
                                    json.forEach(marker => {
                                        const point = turf.point(marker.geometry.coordinates);
                                        if (turf.booleanPointInPolygon(point, polygon)) {
                                            count++;
                                        }
                                    });


                                    tableData.data.forEach(o => {
                                        if (o.code === value.properties.code) {
                                            o.installateur = count;
                                            density = (count/o.surface*1000).toFixed(2) 
                                            o.densInstallateur = density
                                            if("installationDensity" in geojsonFrance.features[0].properties){
                                                o.rapport = density != 0 ? (value.properties.installationDensity/density).toFixed(2) : 0
                                            } 
                                        }
                                    });
                                    value.properties.installateurDensity = density
                                    if("installationDensity" in value.properties){
                                        value.properties.rapport = density != 0 ? (value.properties.installationDensity/density).toFixed(2) : 0
                                        rapportMax = parseFloat(value.properties.rapport) > parseFloat(rapportMax) ? parseFloat(value.properties.rapport) : parseFloat(rapportMax)
                                    }
                                    DensityInstallateurMax = parseFloat(density) > parseFloat(DensityInstallateurMax) ? parseFloat(density) : parseFloat(DensityInstallateurMax)
                                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == polygon.properties.code;
                                    });


                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (!marker._popup._content.includes("installateur")){
                                            if (count > 1){
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateurs ('+  density+' installateur/10 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateur ('+  density+' installateur/10 000km²)</li>');
                                            }
                                        }
                                    });
                                    
                })    
                    // Pour compter le nombre d'installateur pour la Belgique    
                    let count = 0;
                    $.each( window.geojsonBelgique.features, function( key, value ) {
                                    const polygon = value
                                    
                                    json.forEach(marker => {
                                        const point = turf.point(marker.geometry.coordinates);
                                        if (turf.booleanPointInPolygon(point, polygon)) {
                                            count++;
                                        }
                                    });                                    
                    }); 
                    
                    tableData.data.forEach(o => {
                                        if (o.code === 100) {
                                            o.installateur = count;
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallateur = density
                                        }
                                        }); 
                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == 100;
                                    });

                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (!marker._popup._content.includes("installateur")){
                                            if (count > 1){
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateurs ('+  density+' installateur/10 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateur ('+  density+' installateur/10 000km²)</li>');
                                            }
                                        }
                                    });
                    
                    //Pour compter le nombre d'installateur pour la Suisse
                    count = 0;
                    $.each( window.geojsonSuisse.features, function( key, value ) {
                                    const polygon = value
                                    
                                    json.forEach(marker => {
                                        const point = turf.point(marker.geometry.coordinates);
                                        if (turf.booleanPointInPolygon(point, polygon)) {
                                            count++;
                                        }
                                    });                                    
                    }); 
                     
                    tableData.data.forEach(o => {
                                        if (o.code === 200) {
                                            o.installateur = count;                                            
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallateur = density
                                        }
                                        });
                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == 200;
                                    });

                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (count > 1){
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateurs ('+  density+' installateur/10 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateur ('+  density+' installateur/10 000km²)</li>');
                                            }
                                    });
                    //Pour compter le nombre d'installateur pour le luxembourg
                    count = 0;
                    $.each( window.geojsonLuxembourg.features, function( key, value ) {
                                    const polygon = value
                                    
                                    json.forEach(marker => {
                                        const point = turf.point(marker.geometry.coordinates);
                                        if (turf.booleanPointInPolygon(point, polygon)) {
                                            count++;
                                        }
                                    });                                    
                    }); 
                     
                    tableData.data.forEach(o => {
                                        if (o.code === 300) {
                                            o.installateur = count;                                            
                                            density = (count/o.surface*1000).toFixed(2)
                                            o.densInstallateur = density
                                        }
                                        });
                    var filtered = Object.values(mymap._layers).filter(lay => {
                                    return lay instanceof L.Marker 
                                        && lay.options.icon 
                                        && lay.options.icon.options.code == 300;
                                    });

                                    // Exemple : modifier le popup de tous
                                    filtered.forEach(marker => {
                                        if (count > 1){
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateurs ('+  density+' installateur/10 000km²)</li>');
                                            }else{
                                                marker.setPopupContent(marker._popup._content + '<li>'+ count +' installateur ('+  density+' installateur/10 000km²)</li>');
                                            }
                                    });

                    $('#table').bootstrapTable('destroy')                  
                    $('#table').bootstrapTable(tableData)
                    $("#DensityInstallateur").prop('disabled', false);
                    if("installationDensity" in geojsonFrance.features[0].properties){
                        $("#rapport").prop('disabled', false);
                    }

                    }    
            })

        mymap.addLayer(markersClusterInstallateur);                    
    }
}
const $DisplayMarker = new DisplayMarker()

var onDrop = function (e) {
	var latlng = this.getLatLng();
    var t = this
    $.ajax({
        url: window.location.href,
        type:'post',
        data:{lat:latlng.lat, lng: latlng.lng},
        dataType: 'html',
        success: function (json) {
            data = JSON.parse(json)
            var lat = data.lat
            var lon = data.lon
            var txt = ""
            if ("adresse" in data){
                txt = "<b>Adresse: </b>" + data['adresse'] + '<br>'
            }
            txt+='<b>Coordonnées GPS: </b>' + parseFloat(lat).toFixed(6) + ',' + parseFloat(lon).toFixed(6) + '<br>'
            txt += "<b>Altitude: </b>" + data.alt + " m"
            if ("zone" in data){
                if (data.zone.length == 2){
                    txt += "<br> Vérifié la température de base entre les zones " + data.zone[0] + ' et ' +  data.zone[1] + " sur ce site:" +
                    "<a href='https://www.izi-by-edf-renov.fr/blog/temperature-exterieure-de-base'>ici</a>"
                }else{
                    txt += "<br><b>Zone: </b>" + data['zone']
                }    
            }
            if ("TempDeBase" in data){
                txt += "<br><b>Température de Base: </b>" + data['TempDeBase'] + '°C'
            }
            if ("commercial" in data){
                txt += "<br><b>Commercial de la zone: </b>" + data['commercial']
            }
            t._popup.setContent(txt)
            t.openPopup()
        }
    })
};
var marker
function search(){
    var form = $('#adresse').closest("form");
          $.ajax({
            url: window.location.href,
            type:'post',
            data: form.serialize(),
            dataType: 'html',
            success: function (json) {
                if (marker){
                    mymap.removeLayer(marker)
                }
                data = JSON.parse(json)
                var lat = data.lat
                var lon = data.lon
                var txt =""
                if ("adresse" in data){
                    txt = "<b>Adresse: </b>" + data['adresse'] + '<br>'
                }
                txt+='<b>Coordonnées GPS: </b>' + parseFloat(lat).toFixed(6) + ',' + parseFloat(lon).toFixed(6) + '<br>'
                txt += "<b>Altitude: </b>" + data.alt + " m"
                if ("zone" in data){
                    if (data.zone.length == 2){
                        txt += "<br> Vérifié la température de base entre les zones " + data.zone[0] + ' et ' +  data.zone[1] + " sur ce site:" +
                        "<a href='https://www.izi-by-edf-renov.fr/blog/temperature-exterieure-de-base' target='_blank'>ici</a>"
                    }else{
                        txt += "<br><b>Zone: </b>" + data['zone']
                    }    
                }
                if ("TempDeBase" in data){
                    txt += "<br><b>Température de Base: </b>" + data['TempDeBase'] + '°C'
                }
                if ("commercial" in data){
                    txt += "<br><b>Commercial de la zone: </b>" + data['commercial']
                }
                mymap.setView(new L.LatLng(lat, lon), 12);
                marker = L.marker([lat, lon],{ draggable:true}).addTo(mymap)
                .bindPopup(txt)
                .openPopup()
                .on('dragend', onDrop)
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


// Pour que les numéro des département augmente quand on zoome
const zoomBase = mymap.getZoom();

mymap.on("zoomend", () => {
  const currentZoom = mymap.getZoom();
  const scale = 1 + (currentZoom - zoomBase) * 0.3; // règle l’effet

  document.querySelectorAll(".dep-text").forEach(el => {
    el.style.transform = `scale(${scale})`;
    el.style.transformOrigin = "center center";
  });
});

//Création du tableau
let tableData = {
  columns: [{
    field: 'dept',
    title: 'Département',
    align: 'center'
  }, {
    field: 'code',
    title: 'Code',
    sortable: true,
    align: 'center'
  }, {
    field: 'surface',
    title: 'Surface<br>(km²)',
    sortable: true,
    align: 'center'
  }],
  data: [],
  sortName: 'code',     // colonne utilisée pour trier
  sortOrder: 'asc',     // ou 'desc'
  search: true,
  pagination: true

}

$('[name="repartition"]').change(async function() {
  var repartition = $(this).filter(':checked').val();
  $("#nuancier").html("")
  $("#unite").html("")
  geoGroup.clearLayers()
  switch (repartition){
    case "repartitionCommercial":        
        $.each(geojsonFrance.features, function( key, value ) {
          $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes(value.properties.code)){
                ajoutDepartement(value, v.color, 1000)
            }
          })
        });
        $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("100")){
                ajoutDepartement(geojsonBelgique, v.color, 100)
            }
          })
          $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("200")){
                ajoutDepartement(geojsonSuisse, v.color, 200)
            }
          })
        $.each(JSON.parse(profils), function(k, v){
            if(v.departement.includes("300")){
                ajoutDepartement(geojsonLuxembourg, v.color, 200)
            }
          })
        
        break
    case "installation":

        $.each(geojsonFrance.features, function( key, value ) {
            $.each(JSON.parse(profils), function(k, v){
                if(v.departement.includes(value.properties.code)){
                    ajoutDepartement(value, v.color, 0, "installationDensity")
                }
            })
        });
        GenerateNuancier(DensityInstallationMax, " installation/1000km²")
        break
    case "installateur":
        $.each(geojsonFrance.features, function( key, value ) {
            $.each(JSON.parse(profils), function(k, v){
                if(v.departement.includes(value.properties.code)){
                    ajoutDepartement(value, v.color, 0, "installateurDensity")
                }
            })
        });
        GenerateNuancier(DensityInstallateurMax, " installateur/10 000km²")
        break
    case "rapport":
        $.each(geojsonFrance.features, function( key, value ) {
            $.each(JSON.parse(profils), function(k, v){
                if(v.departement.includes(value.properties.code)){
                    ajoutDepartement(value, v.color, 0, "rapport")
                }
            })
        });
        GenerateNuancier(rapportMax, " installations par installateur")
        break
  }
});

//Pour agrandir la fenêtre de la carte

const colMap = document.getElementById("col-map");
  const mapDiv = document.getElementById("map");
  const resizer = document.getElementById("resizer");

  let isResizing = false;

  resizer.addEventListener("mousedown", function(e) {
    isResizing = true;
    document.body.style.userSelect = "none";
  });

  document.addEventListener("mousemove", function(e) {
    if (!isResizing) return;

    const minWidth = 300;
    const minHeight = 600;

    // Largeur: distance entre le bord gauche de la row et la souris
    const newWidth = Math.max(minWidth, e.clientX - colMap.parentElement.offsetLeft);

    // Hauteur: distance entre le haut du conteneur et la souris
    const newHeight = Math.max(minHeight, e.clientY - mapDiv.getBoundingClientRect().top);

    // on fixe la largeur de la colonne gauche
    colMap.style.flex = "0 0 " + newWidth + "px";

    // on fixe la hauteur de la carte
    mapDiv.style.height = newHeight + "px";

    mymap.invalidateSize();
  });

  document.addEventListener("mouseup", function() {
    isResizing = false;
    document.body.style.userSelect = "auto";
  });
