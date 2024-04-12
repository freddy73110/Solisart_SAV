/* Pour sélectionner que 2 fichiers csv max*/
$("#plage").find('input').on("click", function(){
    switch($("#plage").find('input:checked').length){
        case 0:
            $("#plage").find('input').prop("disabled", false)
            break        
        case 1:
            if($("#plage").find('input').first().is(':checked')){
                $("#plage").find('input:not(:checked)').prop("disabled", true)
                $("#plage").find('input:eq(0), input:eq(1)').prop("disabled", false)

            }else if($("#plage").find('input').last().is(':checked')){
                $("#plage").find('input:not(:checked)').prop("disabled", true)
                $("#plage").find('input:eq(-1), input:eq(-2)').prop("disabled", false)
            }else{
                $("#plage").find('input:not(:checked)').prop("disabled", true)
                $.each($("#plage").find('input'), function(i, v){
                    if($(v).is(':checked')){
                        $("#plage").find('input').eq(i).prop("disabled", false)
                        $("#plage").find('input').eq(i-1).prop("disabled", false)
                        $("#plage").find('input').eq(i+1).prop("disabled", false)
                    }
                })
            }
            break
        default:
            $("#plage").find('input:not(:checked)').prop("disabled", true)    
    }
})

$("#inputLinkData").on("change", function(e){
    var file = e.target.files[0]
    var reader = new FileReader();
   reader.readAsText(file,'UTF-8');

   // here we tell the reader what to do when it's done reading...
   reader.onload = readerEvent => {
      var csv = readerEvent.target.result; // this is the content!
      new generateChart(data).createDataSinceContent(csv)
   }
})

class generateChart { 

    dataEvolutionChart = {} 

    convertDataCSVToDataConfig = {
        'Tcapt':'t(1)',
        'TcaptF': 't(2)',
        'TbalS': 't(3)',
        'TbalA': 't(4)',
        'TalT': 't(5)',            
        'TpoeleB': 't(6)',        
        'TretC': 't(7)',       
        'TdepC': 't(8)',     
        'Text': 't(9)',    
        'Tcap2': 't(10)',
        'TZ1': 't(11)',
        'TZ2': 't(12)',           
        'TZ3': 't(13)',
        'TZ4': 't(14)',
        'T15': 't(15)',
        'T16': 't(16)',
        'Tcons1': 'Tcons(0)',
        'Tcons2': 'Tcons(1)',
        'Tcons3': 'Tcons(2)',
        'Tcons4': 'Tcons(3)',
        'TconsECS': 'Tcons(6)',
        'TconsPisc_dep': 'TconPisc_dep',
        'C1': 'tr(5)',
        'C2': 'tr(6)',
        'C3': 'tr(7)',
        'APP': 'tr(1)',
        'SOL': 'tr(2)',
        'BTC': 'tr(3)',
        'C7': 'tr(4)',
        'S10':'tr(10)',
        'S11':'tr(11)',
        'POSV3VSOL': 'v3v(0)',
        'POSV3VAPP': 'v3v(1)',
        'MD':'MD'
    }

    constructor(configInstantane) {
        this.configInstantane = configInstantane;
        this.label={
            'Tcapt':'T1 ' + this.configInstantane['tlbl(01)'],
            'TcaptF': 'T2 '+ this.configInstantane['tlbl(02)'],
            'TbalS': 'T3 '+ this.configInstantane['tlbl(03)'],
            'TbalA': 'T4 '+ this.configInstantane['tlbl(04)'],
            'TalT': 'T5 '+ this.configInstantane['tlbl(05)'],            
            'TpoeleB': 'T6 '+ this.configInstantane['tlbl(06)'],        
            'TretC': 'T7 '+ this.configInstantane['tlbl(07)'],       
            'TdepC': 'T8 '+ this.configInstantane['tlbl(08)'],     
            'Text': 'T9 '+ this.configInstantane['tlbl(09)'],    
            'Tcap2': 'T10 '+ this.configInstantane['tlbl(10)'],
            'TZ1': 'T11 '+ this.configInstantane['tlbl(11)'],
            'TZ2': 'T12 '+ this.configInstantane['tlbl(12)'],            
            'TZ3': 'T13 '+ this.configInstantane['tlbl(13)'],
            'TZ4': 'T14 '+ this.configInstantane['tlbl(14)'],
            'T15': 'T15 '+ this.configInstantane['tlbl(15)'],
            'T16': 'T16 '+ this.configInstantane['tlbl(16)'],
            'Tcons1': 'Consigne Zone 1',
            'Tcons2': 'Consigne Zone 2',
            'Tcons3': 'Consigne Zone 3',
            'Tcons4': 'Consigne Zone 4',
            'TconsECS': 'Consigne ECS',
            'TconsPisc_dep': 'Consigne piscine déportée',
            'C1': 'C1 ' + this.configInstantane['trilbl(05)'],
            'C2': 'C2 ' + this.configInstantane['trilbl(06)'],
            'C3': 'C3 ' + this.configInstantane['trilbl(07)'],
            'APP': 'C4 ' + this.configInstantane['trilbl(01)'],
            'SOL': 'C5 ' + this.configInstantane['trilbl(02)'],
            'BTC': 'C6 ' + this.configInstantane['trilbl(03)'],
            'C7': 'C7 ' + this.configInstantane['trilbl(04)'],
            'chdr1': APP1[parseInt(this.configInstantane['Type_Appoint(0)'])],
            'chdr2': APP2[parseInt(this.configInstantane['Type_Appoint(1)'])],
            'S10':"Opt1 " + this.configInstantane['trilbl(10)'],
            'S11':"Opt2 " + this.configInstantane['trilbl(11)']
        }
    }

    generateSchemaAnime(){
        $("#schemaAnime").html($("#schema").html())
    }

    interactionChart(dataEvolutionChart){
        //Affichage bande bleu sur le graphique le circulateur sélectionné tourne seul
        $("#id_circulateur_seul").val("Aucun").on("change", function(){
            var TESTER = document.getElementById('evolutionChart')
            var shapes = []
            TESTER.layout.shapes.forEach(item => {
                if (item['type'] == 'line'){
                    shapes.push(item)
                }
            })  
            var listIndex=[]
            switch ($("#id_circulateur_seul").val()){
                case "C1":
                    listIndex = dataEvolutionChart['C1'].map((val, i) => (val != "0" 
                    && dataEvolutionChart['C2'][i] == "0" 
                    && dataEvolutionChart['C3'][i] == "0"
                    && dataEvolutionChart['APP'][i] == "0" 
                    && dataEvolutionChart['C7'][i] == "0" ) ? i : undefined).filter(x => x)                    
                    break
                case "C2":
                    listIndex = dataEvolutionChart['C2'].map((val, i) => (val != "0" 
                    && dataEvolutionChart['C1'][i] == "0" 
                    && dataEvolutionChart['C3'][i] == "0"
                    && dataEvolutionChart['APP'][i] == "0" 
                    && dataEvolutionChart['C7'][i] == "0" ) ? i : undefined).filter(x => x)                    
                    break
                case "C3":
                    listIndex = dataEvolutionChart['C3'].map((val, i) => (val != "0" 
                    && dataEvolutionChart['C1'][i] == "0" 
                    && dataEvolutionChart['C2'][i] == "0"
                    && dataEvolutionChart['APP'][i] == "0" 
                    && dataEvolutionChart['C7'][i] == "0" ) ? i : undefined).filter(x => x)                    
                    break
                case "C4":
                    listIndex = dataEvolutionChart['APP'].map((val, i) => (val != "0" 
                    && dataEvolutionChart['C1'][i] == "0" 
                    && dataEvolutionChart['C2'][i] == "0"
                    && dataEvolutionChart['C3'][i] == "0" 
                    && dataEvolutionChart['C7'][i] == "0" ) ? i : undefined).filter(x => x)                    
                    break
                case "C7":
                    listIndex = dataEvolutionChart['C7'].map((val, i) => (val != "0" 
                    && dataEvolutionChart['C1'][i] == "0" 
                    && dataEvolutionChart['C2'][i] == "0"
                    && dataEvolutionChart['C3'][i] == "0" 
                    && dataEvolutionChart['APP'][i] == "0" ) ? i : undefined).filter(x => x)                    
                    break
            }
            listIndex.forEach((val, i) => {
                if(i == 0){
                    shapes.push({
                        type: 'rect',                    
                        x0: dataEvolutionChart['Date'][val],
                        y0: 0,
                        x1: dataEvolutionChart['Date'][val],
                        y1: 100,
                        line: {
                          color: 'rgb(55, 128, 191)',
                          width: 3
                        },
                        fillcolor:"rgb(55, 128, 191)",
                        opacity:0.6
                    }
                    )

                }else if(i == listIndex.length-1){
                    shapes.at(-1)['x1']=dataEvolutionChart['Date'][val]
                }else if(val != listIndex[i+1]-1){
                    shapes.at(-1)['x1']=dataEvolutionChart['Date'][val]
                    shapes.push({
                        type: 'rect',                    
                        x0: dataEvolutionChart['Date'][listIndex[i+1]],
                        y0: 0,
                        x1: dataEvolutionChart['Date'][listIndex[i+1]],
                        y1: 100,
                        line: {
                          color: 'rgb(55, 128, 191)',
                          width: 3
                        },
                        fillcolor:"rgb(55, 128, 191)",
                        opacity:0.6
                    }
                    )
                }
            })
            Plotly.relayout(TESTER, {'shapes': shapes});
        })
        $("#id_demande").val("Aucun").on("change", function(){
            var TESTER = document.getElementById('evolutionChart')
            var shapes = []
            TESTER.layout.shapes.forEach(item => {
                if (item['type'] == 'line'){
                    shapes.push(item)
                }
            })  
            var listIndex=[]
            var Dem = ['1', '2', '3', '4']
            if($("#id_demande").val()=="DemECS"){
                Dem=['1', '2']
            }
            Dem.forEach((demande) => {
                switch ($("#id_demande").val()){
                    case "DemZ1":
                        listIndex = dataEvolutionChart['DemZ1'].map((val, i) => val == demande ? i : undefined).filter(x => x)
                        break
                    case "DemZ2":
                        listIndex = dataEvolutionChart['DemZ2'].map((val, i) => val == demande ? i : undefined).filter(x => x)
                        break
                    case "DemZ3":
                        listIndex = dataEvolutionChart['DemZ3'].map((val, i) => val == demande ? i : undefined).filter(x => x)
                        break
                    case "DemZ4":
                        listIndex = dataEvolutionChart['DemZ4'].map((val, i) => val == demande ? i : undefined).filter(x => x)
                        break
                } 
                var color = 'rgb(250, 0, 0)'
                if($("#id_demande").val()!="DemECS"){
                    switch (demande){
                        case "1":
                            color='rgb(255, 255, 0)'
                        case "2":
                            color='rgb(1, 5, 0)'
                        case "3":
                            color='rgb(55, 128, 191)'
                        case "4":
                            color='rgb(250, 0, 0)'
                    }
                }
                listIndex.forEach((val, i) => {
                    if(i == 0){
                        shapes.push({
                            type: 'rect',                    
                            x0: dataEvolutionChart['Date'][val],
                            y0: 0,
                            x1: dataEvolutionChart['Date'][val],
                            y1: 100,
                            line: {
                            color: color,
                            width: 3
                            },
                            fillcolor:color,
                            opacity:0.6
                        }
                        )

                    }else if(i == listIndex.length-1){
                        shapes.at(-1)['x1']=dataEvolutionChart['Date'][val]
                    }else if(val != listIndex[i+1]-1){
                        shapes.at(-1)['x1']=dataEvolutionChart['Date'][val]
                        shapes.push({
                            type: 'rect',                    
                            x0: dataEvolutionChart['Date'][listIndex[i+1]],
                            y0: 0,
                            x1: dataEvolutionChart['Date'][listIndex[i+1]],
                            y1: 100,
                            line: {
                            color: 'rgb(55, 128, 191)',
                            width: 3
                            },
                            fillcolor:"rgb(55, 128, 191)",
                            opacity:0.6
                        }
                        )
                    }
                })
            })
            Plotly.relayout(TESTER, {'shapes': shapes});
        })
    }

    generateEvolutionChart() {
        var all_data=[]
        var label = this.label
        var dataEvolutionChart = this.dataEvolutionChart
        Object.keys(this.dataEvolutionChart).forEach(function(key) {
            if (['Tcapt', 'TcaptF', 'TbalS', 'TbalA', 'TalT', 'TpoeleB', 'TretC', 'TdepC','demPisc_D', 'Text', 'Tcap2', 'TZ1', 'TZ2',
             'TZ3', 'TZ4', 'T15', 'T16', 'Tcons1', 'Tcons2', 'Tcons3', 'Tcons4', 'TconsECS', 'tfmoy'].includes(key)){
                var unit=' °C'
            }else if(['C1', 'C2', 'C3', 'APP', 'SOL', 'BTC', 'C7', 'POSV3VSOL', 'POSV3VAPP', 'POSV3VOPT'].includes(key)){
                var unit=' %'
            }else{
                var unit=''
            }
            if (!['Date', 'DemZ1', 'DemZ2', 'DemZ3', 'DemZ4', 'DemECS', 'dtcapt3mn','demPisc_D', 'TconPisc_dep', 'var_cir', 'def_T', 'def', 'index6S'].includes(key)){
                all_data.push({
                    x: dataEvolutionChart['Date'],
                    y: dataEvolutionChart[key],
                    unit:unit,
                    yaxis: 'y1',
                    line: {shape: 'linear'},
                    type: 'scatter',
                    hovertemplate:'<b>Valeur:</b> %{y}'+unit,
                    visible: (unit == ' °C') ? true : "legendonly",
                    name: (label.hasOwnProperty(key)) ? label[key] : key
                    }
                )
            }
        })
        
        var selectorOptions = {
            buttons: [{
                step: 'day',
                stepmode: 'backward',
                count: 1,
                label: '1 jour'
            }, {
                step: 'day',
                stepmode: 'backward',
                count: 7,
                label: '1 semaine'
            }, {
                step: 'day',
                stepmode: 'backward',
                count: 14,
                label: '2 semaines'
            },{
                step: 'mouth',
                stepmode: 'backward',
                count: 1,
                label: '1 mois'
            },{
                step: 'all',
                label: 'Tout'
            }],
        };
        
        var layout={
                title:this.configInstantane['serial']+' ' + this.configInstantane['srv_id'],
                autosize: true,
                hovermode:"closest",
                plot_bgcolor: "#F4F4F4",
                paper_bgcolor: "#F4F4F4",
                xaxis:{
                    type: 'datetime',
                    autorange: true,
                    showspikes: true,
                    rangeselector: selectorOptions
                },
                yaxis: {
                    autorange: true,
                    showspikes: true,
                    spikemode: 'toaxis'
                    },
                shapes:[
                        {
                            type: 'line',                    
                            x0: dataEvolutionChart['Date'][0],
                            y0: 0,
                            x1: dataEvolutionChart['Date'][0],
                            y1: 100,
                            line: {
                              color: 'rgb(55, 128, 191)',
                              width: 3
                            }
                        }
                    ]
                // colorway: colorscale
            }
        var icon = {
          'width': 500,
          'path': 'M448 344v112a23.94 23.94 0 0 1-24 24H312c-21.39 0-32.09-25.9-17-41l36.2-36.2L224 295.6 116.77 402.9 153 439c15.09 15.1 4.39 41-17 41H24a23.94 23.94 0 0 1-24-24V344c0-21.4 25.89-32.1 41-17l36.19 36.2L184.46 256 77.18 148.7 41 185c-15.1 15.1-41 4.4-41-17V56a23.94 23.94 0 0 1 24-24h112c21.39 0 32.09 25.9 17 41l-36.2 36.2L224 216.4l107.23-107.3L295 73c-15.09-15.1-4.39-41 17-41h112a23.94 23.94 0 0 1 24 24v112c0 21.4-25.89 32.1-41 17l-36.19-36.2L263.54 256l107.28 107.3L407 327.1c15.1-15.2 41-4.5 41 16.9z',
        'ascent': 500,
        'descent': 0,
        };
        var listIcon={
            'width': 500,
            'path':"M464 480H48c-26.51 0-48-21.49-48-48V80c0-26.51 21.49-48 48-48h416c26.51 0 48 21.49 48 48v352c0 26.51-21.49 48-48 48zM128 120c-22.091 0-40 17.909-40 40s17.909 40 40 40 40-17.909 40-40-17.909-40-40-40zm0 96c-22.091 0-40 17.909-40 40s17.909 40 40 40 40-17.909 40-40-17.909-40-40-40zm0 96c-22.091 0-40 17.909-40 40s17.909 40 40 40 40-17.909 40-40-17.909-40-40-40zm288-136v-32c0-6.627-5.373-12-12-12H204c-6.627 0-12 5.373-12 12v32c0 6.627 5.373 12 12 12h200c6.627 0 12-5.373 12-12zm0 96v-32c0-6.627-5.373-12-12-12H204c-6.627 0-12 5.373-12 12v32c0 6.627 5.373 12 12 12h200c6.627 0 12-5.373 12-12zm0 96v-32c0-6.627-5.373-12-12-12H204c-6.627 0-12 5.373-12 12v32c0 6.627 5.373 12 12 12h200c6.627 0 12-5.373 12-12z",
            'ascent': 500,
            'descent': 0,
        }
        
        var config = {
            scrollZoom: true,
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
          modeBarButtonsToAdd: [
            {
              name: 'Toutes les étiquettes',
              icon: listIcon,
              direction: 'up',
              click: function(gd) {
                if($('#evolutionChart')[0].layout.hovermode == 'closest'){
                    var TESTER = document.getElementById('evolutionChart')
                    Plotly.relayout(
                        TESTER,
                        {
                            'hovermode': "x unified",
                            'yaxis':{'showspikes':false}
                        }
                    );
                }else{
                    var TESTER = document.getElementById('evolutionChart')
                    Plotly.relayout(
                        TESTER,
                        {
                            'hovermode': "closest",
                            'yaxis':{'showspikes':true}
        
                        }
                    );
                }
                }
            },
            {
              name: 'Plein écran',
              icon: icon,
              direction: 'up',
              click: function(gd) {
                if (document.fullscreenElement) {
            document.exitFullscreen();
          } else {
            $('#evolutionChart').get(0).requestFullscreen();
          }
            }}]
            }
        Plotly.newPlot('evolutionChart', all_data, layout, config);
        var TESTER = document.getElementById('evolutionChart')
        var convertdata = this.convertDataCSVToDataConfig
        var dataEvolutionChart = this.dataEvolutionChart
        var oldConfig = this.configInstantane
        
        TESTER.on('plotly_click', function(data){ 
            var x = data.points[0].x
            if(data.points[0].x.length == 16){
                x = x + ':30'
            }
            var idx=TESTER.data[0].x.indexOf(x)
            var shapes = []
            TESTER.layout.shapes.forEach(item => {
                if (item['type'] == 'rect'){
                    shapes.push(item)
                }
            })
            shapes.push(
                {
                    type: 'line',                    
                    x0: x,
                    y0: 0,
                    x1: x,
                    y1: 100,
                    line: {
                      color: 'rgb(55, 128, 191)',
                      width: 3
                    }
                }
            )
            Plotly.relayout(TESTER, {'shapes': shapes});
            for (const [key, value] of Object.entries(convertdata)) {                
                try {
                    if (['APP', 'SOL', 'BTC', 'C7', 'S10', 'S11', 'C1','C2', 'C3'].includes(key)){
                        oldConfig[value]=dataEvolutionChart[key][idx].toString() + 'pC'
                    }else if(['MD', 'POSV3VSOL', 'POSV3VAPP', 'Tcons1', 'Tcons2', 'Tcons3', 'Tcons4', 'TconsECS'].includes(key)){
                        oldConfig[value]=dataEvolutionChart[key][idx].toString()
                    }else{
                        oldConfig[value]=dataEvolutionChart[key][idx].toString() + ' dC'
                    }
                }catch{
                    oldConfig[value]="null"
                }                
            }            
            refresh(oldConfig, 'schemaAnime')

        }) 
        for (const [key, value] of Object.entries(convertdata)) {                
            try {
                if (['APP', 'SOL', 'BTC', 'C7', 'S10', 'S11', 'C1','C2', 'C3'].includes(key)){
                    oldConfig[value]=dataEvolutionChart[key][0].toString() + 'pC'
                }else if(['MD', 'POSV3VSOL', 'POSV3VAPP', 'Tcons1', 'Tcons2', 'Tcons3', 'Tcons4', 'TconsECS'].includes(key)){
                    oldConfig[value]=dataEvolutionChart[key][0].toString()
                }else{
                    oldConfig[value]=dataEvolutionChart[key][0].toString() + ' dC'
                }
            }catch{
                oldConfig[value]="null"
            }                
        }            
        refresh(oldConfig, 'schemaAnime')  
        this.interactionChart(dataEvolutionChart) 
        this.generateSchemaAnime()
        $("#schemaAnime").find(".fa-bounce").removeClass("fa-bounce")
        this.hoverlegend()
        this.performenceAppoint()
        this.performenceZone()
        $("body").toggleClass("wait")
    }

    convertFormatDate(strDate) {
        var partDate = strDate.split(" ")[0];
        var partTime = strDate.split(" ")[1];
        var year = '20' + partDate.split("/")[2];
        var month = partDate.split("/")[1];
        var day = partDate.split("/")[0];
        return year + '-' + month + '-' + day + ' ' + partTime;
    }

    hoverlegend(){
        $("#evolutionChart").find("g.traces")
            .mouseover( function(){
            var legendText = $(this).find("text.legendtext").html()            
            $.each($($("#evolutionChart"))[0].data, function(index, value){
                if(value.name == legendText){
                    var TESTER = document.getElementById('evolutionChart')
                    Plotly.restyle(TESTER, {
                    line:{width: 2}
                    });
                    Plotly.restyle(TESTER, {
                        line:{width: 4}
                        }, index);
                }
            })
            })
            .mouseout( function(){
            var legendText = $(this).find("text.legendtext").html()
            $.each($($("#evolutionChart"))[0].data, function(index, value){
                if(value.name == legendText){
                    var TESTER = document.getElementById('evolutionChart')
                    Plotly.restyle(TESTER, {
                        line:{width: 2, index}
                    });
                }
            })
            })
        }

    createDataSinceContent(csv){
        $("body").toggleClass("wait")
        const lines = csv.split("\n");
                var maxcolumns = '';

                // Cherche la ligne où de dénomination de colonnes où il y a le plus de champs
                lines.forEach(line => {
                    if (line.includes("Date") && line.length > maxcolumns.length) {
                        maxcolumns = line;
                    }
                });

                // Suppression de l'erreur si Date est écrit Date1
                var columns = maxcolumns.replace("Date1", "Date").split(";");
                

                columns.forEach(value => {
                    this.dataEvolutionChart[value] = [];
                });

                var lastDate = '';
                lines.forEach(line => {
                    if (!(line.includes("Date") || line.includes("SolisConfrt"))) {
                        var lineValues = line.replaceAll(' l mn', '').replaceAll('?', 'null').replaceAll('dsc', 'null').split(";");

                        columns.forEach((value, index) => {
                            //Pour mettre null si colonne vide
                            try {
                                if (index < lineValues.length-1) {
                                    if (value == "Date") {
                                        if (this.dataEvolutionChart['Date'].length == 0) {
                                            this.dataEvolutionChart[value].push(this.convertFormatDate(lineValues[index]) + ':30');
                                            lastDate = lineValues[index];
                                        } else if (lastDate == lineValues[index]) {
                                            this.dataEvolutionChart[value].push(this.convertFormatDate(lineValues[index]) + ':30');
                                            lastDate = lineValues[index];
                                        } else {
                                            this.dataEvolutionChart[value].push(this.convertFormatDate(lineValues[index]) + ':00');
                                            lastDate = lineValues[index];
                                        }
                                    } else {
                                        this.dataEvolutionChart[value].push(lineValues[index]);
                                    }
                                } else {
                                    this.dataEvolutionChart[value].push('null');
                                }
                            } catch (error) {
                                console.log(error);
                            }
                        });
                    }
                });
                this.generateEvolutionChart();
                const defdef = new defaults()
                defdef.AfficherListAllDefault(this.dataEvolutionChart)

    }

    createData(url) {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.onload = () => {
            if (xhr.status === 200) {
                var csv = xhr.responseText;
                this.createDataSinceContent(csv)
            } else {
                console.error('Erreur lors du chargement du fichier CSV');
            }
        };
        xhr.send();
    }

    performenceAppoint(){
        $("#performanceAppoint").html()
        var PerfAppointData = []
        var annotations = []
        //-1 pour ne pas compter la dernière ligne qui fait null, null; null; ...
        if(this.configInstantane['Type_Appoint(0)'] != '0'){
            $("table[id=TableAppoint] thead th:eq(1)").html(APP1[this.configInstantane['Type_Appoint(0)']])
            PerfAppointData.push(
                {
                    values: [this.dataEvolutionChart['chdr1'].filter((item) => item == '0').length, this.dataEvolutionChart['chdr1'].filter((item) => item != '0').length],
                    labels: ['Arrêt', 'En Demande' ],
                    domain: {column: 0},
                    name: APP1[this.configInstantane['Type_Appoint(0)']],
                    hoverinfo: 'label+percent+name',
                    hole: .4,
                    type: 'pie'
                  }
            )
            var demarrage = -1
            var lastStart = this.dataEvolutionChart['Date'][0]
            this.dataEvolutionChart['chdr1'].forEach((val, i) => {
                if(i<this.dataEvolutionChart['chdr1'].length-1){
                    if(this.dataEvolutionChart['chdr1'][i] == '0' && this.dataEvolutionChart['chdr1'][i+1] != '0'){
                        demarrage += 1
                        lastStart = this.dataEvolutionChart['Date'][i]
                    }
                }            
            });
            //Afficher nbre de démarrage
            $("table[id=TableAppoint] tbody tr:eq(1) td:eq(1)").html(demarrage)
            //Afficher dernier démarrage
            $("table[id=TableAppoint] tbody tr:eq(0) td:eq(1)").html(lastStart)
            //Afficher la durée moyenne de démarrage
            if(demarrage != 0){
                var dureemoy = this.dataEvolutionChart['chdr1'].filter((item) => item != '0').length*30/60/demarrage
                $("table[id=TableAppoint] tbody tr:eq(2) td:eq(1)").html(parseInt(dureemoy) + 'min')
            }else{
                $("table[id=TableAppoint] tbody tr:eq(2) td:eq(1)").html('-')
            }
            if(this.configInstantane['Type_Appoint(1)'] != '0'){
                    annotations.push(
                        {
                            font: {
                            size: 20
                            },
                            showarrow: false,
                            text: APP1[this.configInstantane['Type_Appoint(0)']],
                            x: 0.17,
                            y: 0.5
                        }
                    )
                }else{
                    annotations.push(
                        {
                            font: {
                            size: 20
                            },
                            showarrow: false,
                            text: APP1[this.configInstantane['Type_Appoint(0)']],
                            x: 0.5,
                            y: 0.5
                        }
                    )
                }
        }
        if(this.configInstantane['Type_Appoint(1)'] != '0'){            
            $("table[id=TableAppoint] thead th:eq(2)").html(APP2[this.configInstantane['Type_Appoint(1)']])
            PerfAppointData.push(
                {
                    values: [this.dataEvolutionChart['chdr2'].filter((item) => item == '0').length, this.dataEvolutionChart['chdr2'].filter((item) => item != '0').length],
                    labels: ['Arrêt', 'En Demande' ],
                    domain: {column: this.configInstantane['Type_Appoint(0)'] != '0'},
                    name: APP2[this.configInstantane['Type_Appoint(1)']],
                    hoverinfo: 'label+percent+name',
                    hole: .4,
                    type: 'pie'
                  }
            )
            var demarrage = -1
            var lastStart = this.dataEvolutionChart['Date'][0]
            this.dataEvolutionChart['chdr2'].forEach((val, i) => {
                if(i<this.dataEvolutionChart['chdr2'].length-1){
                    if(this.dataEvolutionChart['chdr2'][i] == '0' && this.dataEvolutionChart['chdr2'][i+1] != '0'){
                        demarrage += 1
                        lastStart = this.dataEvolutionChart['Date'][i]
                    }
                }            
            });
            $("table[id=TableAppoint] tbody tr:eq(1) td:eq(2)").html(demarrage)
            $("table[id=TableAppoint] tbody tr:eq(0) td:eq(2)").html(lastStart)
            if(this.configInstantane['Type_Appoint(1)'] != '0'){
                annotations.push(
                    {
                        font: {
                        size: 20
                        },
                        showarrow: false,
                        text: APP2[this.configInstantane['Type_Appoint(1)']],
                        x: 0.83,
                        y: 0.5
                    }
                )
            }else{
                annotations.push(
                    {
                        font: {
                        size: 20
                        },
                        showarrow: false,
                        text: APP2[this.configInstantane['Type_Appoint(1)']],
                        x: 0.5,
                        y: 0.5
                    }
                )
            }
        }
          
          var layout = {
            title: 'Répartition des demandes Chaudière',
            annotations: annotations,
            height: 400,
            showlegend: false,
            grid: {rows: 1, columns: this.configInstantane['Type_Appoint(0)'] != '0' + this.configInstantane['Type_Appoint(1)'] != '0'}
          };
          
          var config={responsive: true}

          Plotly.newPlot('performanceAppoint', PerfAppointData, layout, config);
    }

    performenceZone(){
        $("#performanceZone").html()
        var PerfDataDemZone =[]
        var PerfDataZoneConsigne =[]
        var dems = ['DemZ1', 'DemZ2', 'DemZ3', 'DemZ4']
        var decompteZone = 1
        //pour ECS
        PerfDataDemZone.push(
            {
                values: [this.dataEvolutionChart['DemECS'].length/2/60,
                 this.dataEvolutionChart['DemECS'].filter((item) => item == '0').length/2/60, 
                    (this.dataEvolutionChart['DemECS'].filter((item) => item == '1').length + this.dataEvolutionChart['DemECS'].filter((item) => item == '2').length)/2/60,
                    this.dataEvolutionChart['DemECS'].filter((item) => item == '100').length/2/60
                ],
                labels:['ECS', 'Non', 'En Demande', 'A arrêt'],
                parents: ['', 'ECS', 'ECS', 'ECS'],
                domain: {column: 0},
                name: "Eau chaude Sanitaire",
                hovertemplate: '<b>%{label}:<br>Durée total: %{value:.2f} heures<br>soit %{percentRoot:.2%} du temps total et %{percentParent:.2%} du temps "%{parent}"</b>',                    
                leaf: {opacity: 0.4},
                marker: {line: {width: 2}},
                type: 'sunburst',
                leaf: {"opacity": 0.4},
                branchvalues: 'total',
            }
        )
        var ecartConsigne = []
        this.dataEvolutionChart['TconsECS'].forEach((value, i) => {
            try{
                ecartConsigne.push(
                    parseFloat(value) - parseFloat(this.dataEvolutionChart['TbalA'])
                 )
            }catch{
                ecartConsigne.push("null") 
            }                })
        PerfDataZoneConsigne.push(                    
                    {
                        y: this.dataEvolutionChart['TconsECS'].concat(ecartConsigne),
                        x: Array(this.dataEvolutionChart['TconsECS'].length).fill("Température").concat(
                            Array(ecartConsigne.length).fill("Ecart à la consigne")
                            ), 
                        name:"Eau chaude Sanitaire",
                        type: 'box'
                      }
                )
        //Pour les zones
        dems.forEach((DemZ, index) => {
            if(this.configInstantane['Type_Emetteur('+ index +')'] != '0'){
                PerfDataDemZone.push(
                    {
                        values: [
                            this.dataEvolutionChart[DemZ].length/2/60,
                            (this.dataEvolutionChart[DemZ].length - this.dataEvolutionChart[DemZ].filter((item) => item != '0').length)/2/60,
                            (this.dataEvolutionChart[DemZ].length - this.dataEvolutionChart[DemZ].filter((item) => item == '0').length)/2/60,                            
                            this.dataEvolutionChart[DemZ].filter((item) => item == '1').length/2/60,
                            this.dataEvolutionChart[DemZ].filter((item) => item == '2').length/2/60,
                            this.dataEvolutionChart[DemZ].filter((item) => item == '3').length/2/60,
                            this.dataEvolutionChart[DemZ].filter((item) => item == '4').length/2/60
                        ],
                        labels: [this.configInstantane['tlbl(1'+ DemZ.replace("DemZ", "") +')'], 
                            'Sans Demande',
                            'En demande',                        
                            'Solaire',
                            'Ballon tampon',
                            'Ballon Sanitaire',
                            'Appoint'],
                        parents:[
                            '',
                             this.configInstantane['tlbl(1'+ DemZ.replace("DemZ", "") +')'],
                             this.configInstantane['tlbl(1'+ DemZ.replace("DemZ", "") +')'],
                             'En demande',
                             'En demande',
                             'En demande',
                             'En demande'],
                        domain: {column: decompteZone},
                        hovertemplate: '<b>%{label}:<br>Durée total: %{value:.2f} heures<br>soit %{percentRoot:.2%} du temps total et %{percentParent:.2%} du temps "%{parent}"</b>',                    
                        name: this.configInstantane['tlbl(1'+ DemZ.replace("DemZ", "") +')'],
                        type: 'sunburst',
                        leaf: {"opacity": 0.4},
                        branchvalues: 'total',
                    }
                )
                var ecartConsigne = []
                this.dataEvolutionChart['Tcons'+ DemZ.replace("DemZ", "")].forEach((value, i) => {
                    try{
                        ecartConsigne.push(
                            parseFloat(value) - parseFloat(this.dataEvolutionChart['TZ'+ DemZ.replace("DemZ", "")][i])
                        )
                    }catch{
                        ecartConsigne.push("null") 
                    }                })
                PerfDataZoneConsigne.push(                    
                    {
                        y: this.dataEvolutionChart['TZ'+ DemZ.replace("DemZ", "")].concat(ecartConsigne),
                        x: Array(this.dataEvolutionChart['TZ'+ DemZ.replace("DemZ", "")].length).fill("Température").concat(
                            Array(ecartConsigne.length).fill("Ecart à la consigne")
                            ), 
                        name:this.configInstantane['tlbl(1'+ DemZ.replace("DemZ", "") +')'],
                        type: 'box'
                      }
                )
                decompteZone += 1
                }
        })       
        var layout = {
            title: 'Répartition des temps de demandes',
            autosize: true,
            yaxis:{autorange:true},
            xaxis:{autorange:true},
            showlegend: false,
            grid: {rows: 1, columns: decompteZone}
        };          
        var config={responsive: true}
        Plotly.newPlot('performanceZoneDem', PerfDataDemZone, layout, config);
        var layout = {
            title:"Température et écart à la consigne",
            yaxis: {
              title: 'Température °C',
              autorange: true,
              zeroline: false
            },
            xaxis:{autorange:true},
            boxmode: 'group'
          };
          Plotly.newPlot('performanceZoneConsigne', PerfDataZoneConsigne, layout, config);      
    }

}
function ResizePerformChart(){
    var P = document.getElementById('performanceAppoint')
    Plotly.relayout(P, {'xaxis.autorange': true,'yaxis.autorange': true})
}





