
$(function () {
    var today = new Date();
    var date = (today.getDate())+'-'+(today.getMonth()+1)+ '-'+ today.getFullYear();
     $("input[name='date_evaluation']").val(today.
              toLocaleString('fr-fr', {year: 'numeric', month: '2-digit', day: '2-digit'}).
              replace(/(\d+)\/(\d+)\/(\d+)/, '$1-$2-$3'))
    $("input[name='date_evaluation']").datetimepicker({
      format: 'd-m-Y'
    }
    );
  });
  $("input[name='date_evaluation']").val($("input[name='date_evaluation']").val().substring(0,10).replace('\/', '-').replace('\/', '-'))

  $(document).ready(function() {$(".textareaEmoji").emojioneArea({});});

  $('table tr td.classChecked').on("click", function(){
    if (!$(this).closest("tr").find("input[type=checkbox]").is(':checked')){
        $(this).closest("tr").find("input[type=checkbox]").prop('checked', true)
        $(this).closest("tr").find("input[type=checkbox]").parent().find("input").val(true)
    }
})
$("table").find("input[type=checkbox]").on("click", function(){
    if ($(this).is(':checked')){
        $(this).parent().find("input").val(true)
    }else{
        $(this).parent().find("input").val(false)
    }

})
$('.star').append('<i class="fas fa-star star0 fullStar" style="color:yellow"></i><i class="far fa-star star1" style="color:yellow"></i><i class="far fa-star star2" style="color:yellow"></i><i class="far fa-star star3" style="color:yellow"></i><i class="far fa-star star4" style="color:yellow"></i>')
$('.star').click(function() {                
    var $t = $(this)
    var t = event.target
    var j = true
    if ($(t).is("path")){
        t = $(t).parent()
    }
    if(! $(t).is('td')){
        starNumber = ""
        var svg_list = $(this).find("svg")
        $.each($(t).attr("class").split(/\s+/), function(index, value){
            switch (value){
                case 'star0':
                    starNumber = 0
                    if($t.find(".fullStar").length == 1){
                        j=false
                        $t.html("")
                        $t.append('<input type="hidden" name="star" value="0">')
                    }else{
                        $t.html("")
                    }
                    break;
                case 'star1':
                    starNumber = 1 
                    $t.html("")  
                    break; 
                case 'star2':
                    starNumber = 2  
                    $t.html("") 
                    break;
                case 'star3':
                    starNumber = 3  
                    $t.html("") 
                    break;
                case 'star4':
                    starNumber = 4  
                    $t.html("") 
                    break;
            }
        })
        $.each(svg_list, function(i, v){
            var intre = i + 1
            if(j){
                $t.append('<i class="fas fa-star fullStar star'+ i+'" style="color:yellow"></i>')
                if(i == starNumber){
                    $t.append('<input type="hidden" name="star" value="'+ intre +'">')
                    j = false
                }
            }else{
                    $t.append('<i class="far fa-star star'+ i+'" style="color:yellow"></i>')
            }
        })
    }
})

$("#enregister").on("click", function(){
    var form = $(this).closest("form");
                $.ajax({
                        url: window.location.href,
                        type:'post',
                        data: form.serialize(),
                        dataType: 'json',
                        success: function (data) {
                        //todo faire un message de validation
                        location.reload()
                        }
                })
})

$("form#profil_id :input").on("input", function(){
    $("button[name='modifier_profil']").removeClass('visually-hidden')
  })
  $("button[name='modifier_profil']").on("click", function(){
    var $this = $(this)
    $this.html('En cours de modification')
    var form = $(this).closest("form");
    $.ajax({
            url: window.location.href,
            type:'post',
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
            //todo faire un message de validation
                $this.html('Modifier')
            }
    })
  })

  const evaluations = JSON.parse(document.getElementById('evaluations').textContent);
  if (evaluations.length){
    $("#myDiv").removeClass('d-none')
  }
                    var dataChart = {}
                    $.each(evaluations, function(idx, x){
                        var crit = x.critere
                        var note=''
                        for (let i = 0; i < x.note; i++) {
                            note += "&#11088;";
                        }
                        if (x.note == 0){
                            x.note = 0.5
                            note='<span style="font-size:200%;color:yellow;">&#9734;</span>'

                        }
                        if (!dataChart.hasOwnProperty(crit)){
                            dataChart[crit]={
                                'x': ['Date: ' + x.date.slice(0, 10)],
                                'y': [x.note],
                                'commentaire':['<b>' +crit + ':</b> ' + note + '<br><b>Commentaire: </b>' + x.commentaire],
                                'hovertemplate':['<b>' +crit + ':</b> ' + note],
                                'text': [crit]
                            }                            
                        }else{
                            dataChart[crit]['x'].push('Date: ' + x.date.slice(0, 10))
                            dataChart[crit]['y'].push(x.note)
                            dataChart[crit]['commentaire'].push('<b>' + crit + ':</b> ' + note + '<br><b>Commentaire: </b>' + x.commentaire)
                            dataChart[crit]['hovertemplate'].push(crit + ': ' + note)
                            dataChart[crit]['text'].push(crit)
                        }
                    })
                    data=[]
                    for (var key in dataChart){
                        data.push(
                            {
                                x : dataChart[key]['x'],
                                y: dataChart[key]['y'],
                                type: 'bar',
                                name: key,
                                text: dataChart[key]['text'],
                                hovertemplate: dataChart[key]['hovertemplate'],
                                commentaire: dataChart[key]['commentaire'],
                                textangle: 90,
                                marker: {
                                        opacity: 0.7,
                                        line: {
                                        width: 1.5
                                        }
                                    }
                            }
                        )
                        
                    }
                    var layout = {
                    title: 'Evolution des évaluations',
                    xaxis: {
                        title:{
                            text: 'Date'
                        },
                        tickangle: -45
                    },
                    yaxis: {
                        title: {
                            text: '&#127775;'
                        }
                    },
                    barmode: 'group'
                    };
                    Plotly.newPlot('myDiv', data, layout);
                    var myPlot = document.getElementById('myDiv');
                    myPlot.on('plotly_hover', function(data){
                            var pts = '';
                        for(var i=0; i < data.points.length; i++){
                            pts = 'x = '+data.points[i].x +'\ny = '+
                                data.points[i].y.toPrecision(4) + '\n\n';
                            d = data.points[i].data.commentaire[0]
                            l= data.points[i].label
                        }
                        $("#commentaire").html(l + '<br>' + d)
                    });

function infoHeraklesfunction(id){
    $.ajax({
                 url: window.location.href,
                 data: {'herakles': ''},
                 dataType: 'html',
                 type: 'post',
                 success: function (data) {
                    $("#infoHerakles").html(data)
                 }
            })
}

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

console.log("mais pourquoi?")
//map

const fontAwesomeIcon = L.divIcon({
    html: '<span class="fa-layers fa-fw fa-4x" style="vertical-align: top;"><i class="fas fa-map-marker text-primary" style="color:black"></i><i class="fas fa-solar-panel fa-inverse" data-fa-transform="shrink-10"></i></span>',
    iconSize: [60, 48],
    iconAnchor: [30, 48],
    popupAnchor:  [0, -48],
    className: 'IconInstallation'
});
const fontAwesomeIconInstallateur = L.divIcon({
    html: '<span class="fa-layers fa-fw fa-4x" style="vertical-align: top;"><i class="fas fa-map-marker text-danger" style="color:black"></i><i class="fas fa-tools fa-inverse" data-fa-transform="shrink-10"></i></span>',
    iconSize: [60, 48],
    iconAnchor: [30, 48],
    popupAnchor:  [0, -48],
    className: 'IconInstallateur'
});
var onDrop = function (e) {
	var latlng = this.getLatLng();
    var t = this
    $.ajax({
        url: window.location.href,
        type:'post',
        data:{lat:latlng.lat, lng: latlng.lng},
        dataType: 'json',
        success: function () {
            t._popup.setContent("<b>"+ $("#ident").html()+ "</b>")
            t.openPopup()
        }
    })
};
const mymap = L.map('installation_carte',{
        center:[45, 0],
        zoom:6
        });
            L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}).addTo(mymap);
            const geo_instals = JSON.parse(document.getElementById('geo_instals').textContent)
            var arrayOfMarkers = []
            $.each(geo_instals, function(index, item){
                arrayOfMarkers.push(item.geolocalisation.split(',').map((x)=>Number(x)))
                L.marker(item.geolocalisation.split(','),{ icon: fontAwesomeIcon}).addTo(mymap)
                .bindPopup("<a href='/installation/"+ item.id +"' ><b>"+item.installation +" - "+ item.proprio +"</b></a>")
            })
            const geoUser = JSON.parse(document.getElementById('geo_user').textContent)
            const user = JSON.parse(document.getElementById('user').textContent)
            if (geoUser){
                arrayOfMarkers.push(geoUser)
                  L.marker(geoUser,{ icon: fontAwesomeIconInstallateur , draggable:true})
                  .addTo(mymap)
                  .on('dragend', onDrop)
                   .bindPopup("<b>"+ user +"</b>")
            }
                   
var bounds = new L.LatLngBounds(arrayOfMarkers);
mymap.fitBounds(bounds)

function localise(){
        $.ajax({
                            url: window.location.href,
                            type:'post',
                            data:{localise: ''},
                            dataType: 'json',
                            success: function (json) {
                                console.log(json)
                                //to remove all markers with installateur
                                for (const [key, value] of Object.entries(mymap._layers)) {
                                    if (value.options.icon == fontAwesomeIconInstallateur){
                                        mymap.removeLayer(value)
                                    }
                                }
                                if (json.localisation == 'village'){
                                    var precision= '<br> <i class="fas fa-exclamation-triangle text-danger"></i> Location imprécise'
                                }else{
                                    var precision= "<br> Location exacte"
                                }
                                var markerInstallateur = L.marker(
                                    [json.lat, json.lon],
                                    { icon: fontAwesomeIconInstallateur, draggable:true}
                                    )
                                    .addTo(mymap).bindPopup("<b>"+ $("#ident").html()+ precision +"</b>")
                                    .openPopup()
                                arrayOfMarkers.push([json.lat, json.lon])
                                var bounds = new L.LatLngBounds(arrayOfMarkers);
                                mymap.fitBounds(bounds);
                                markerInstallateur.on('dragend', onDrop)
                            }
        })
    }