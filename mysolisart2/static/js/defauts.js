class defaults{

    listDef=[
        'Sonde poêle bouilleur tombée du doigt de gant',
        'T.Capteur supérieure 115°C',
        'T4 ou T3 supérieure Tmax autorisée',
        'Capteur inversé',
        'Blocage du multiplexeur',
        'défaut chaudière',
        'sonde Tcapt inférieure Tcapt froid',
        'Tcapt froid supérieur T7 en solaire',
        'Coupure de courant',
        'Clapet fuyard C1 à C4, C7 ou V3VAPP',
        'Calage V3V APP', 
        'Clapet fuyard C4', 
        'Clapet fuyard C5',
        'Loi d\'eau insuffisante',
        'Pas de débit sur C1 à C4', 
        'T6 supérieur Tmax chaudière bois'
    ]
    listVarCir=[
        'Consigne ECS trop élevée de 1°C',        
        'Consigne ECS trop élevée de 2°C',
        'Consigne ECS trop élevée de 3°C',
        'Consigne ECS trop élevée de 4°C',
        'Débit insuffisant dans les capteurs',
        'Débit insuffisant de la pompe de filtration piscine',
        'Blocage: Circulation capteur',
        'T1 très inférieure T8',
        'Circulation BTC',
        'Sonde T3 sortie de son doigt de gant',
        'Temps de marche des capteur supérieur 24h',
        'T1 ou T16 est passé en dessous de -40°C',
        'Clapet fuyard sur C6 ou V3V Tampon mal calée',
        'V3V Solaire mal calée',
        'Un circulateur tourne en permanence',
        'Appoint 1 tourne en permanence'
    ]
    listDtCapt=[
    'Manque débit circulateur C7',
    'T4 sortie de son doigt de gant',
    'T retour froid plancher > 50°C',
    'Clapet fuyard C7',
    'Circulateur SOLAIRE tourne en permanence',
    'Circulateur BTC tourne en permanence',
    'T8 inférieur à T7',
    'Température consigne Z1 non atteinte',
    'Température consigne Z2 non atteinte',
    'Température consigne Z3 non atteinte',
    'Température consigne Z4 non atteinte',
    'defaut clapet retour bouclage sanitaire',
    'T8 monte toute seule',
    'Ecart température trop important entre capteur et module',
    'Sonde comptage en défaut',
    'T1 mal placée']
    listIndex6=[
    'Manque débit circulateur SOL',
    'Manque débit circulateur APP',
    'Manque débit circulateur BTC',
    'Manque débit circulateur C1',
    'Manque débit circulateur C2',
    'Manque débit circulateur C3',
    'Manque débit circulateur C7',
    'Pas de débit circulateur SOL',
    'Pas de débit circulateur APP',
    'Pas de débit circulateur BTC',
    'Pas de débit circulateur C1',
    'Pas de débit circulateur C2',
    'Pas de débit circulateur C3',
    'Pas de débit circulateur C7',
    'Libre',
    'Entrée débitmètre 6 (manque de pression, ....)']


    convertirEnBooleens(nombreBinaire) {
        const resultat = [];
        const chaineBinaire = parseInt(nombreBinaire).toString(2);
        for (const chiffre of chaineBinaire) {
          resultat.push(chiffre === "1");
        }
        var lenresul = 16-resultat.length
        for(let i=0; i<lenresul; i++){
            resultat.unshift(false)
        }
        return resultat.reverse();
      }

    //
    defaultDef(){      
        return this.listDef.map((libelle, i) => {
            if (this.convertirEnBooleens(this.configInstantane['def'])[i]){
                return libelle
            }
        }).filter(x => x)
    }

    defaultVarCir(){
        return this.listVarCir.map((libelle, i) => {
            if (this.convertirEnBooleens(this.configInstantane['var_cir'])[i]){
                return libelle
            }
        }).filter(x => x)
    }

    defaultdtCapt(){
        return this.listDtCapt.map((libelle, i) => {
            if (this.convertirEnBooleens(this.configInstantane['dtcapt3mn'])[i]){
                return libelle
            }
        }).filter(x => x)
    }

    defaultIndex6(){
        return this.listIndex6.map((libelle, i) => {
            if (this.convertirEnBooleens(this.configInstantane['index6S'])[i]){
                return libelle
            }
        }).filter(x => x)
    }

    allDefaults(){
        return this.defaultDef().concat(this.defaultVarCir(),this.defaultdtCapt(), this.defaultIndex6())
    }

    AfficherMessageAllDefaults(configInstantane){
        this.configInstantane = configInstantane
        $("#message").find(".default").remove()
        if(this.allDefaults().length>0){
            var message='<div class="alert alert-warning default">'
            +'<div class="btn-group">'
            +'<a type="button" class="btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" style="color:black; text-decoration: none">'
            +'<b><i class="fa-solid fa-triangle-exclamation"></i> <span class="badge bg-danger rounded-pill">'+this.allDefaults().length+'</span> Défauts actuellement sur l\'installation'+ '</b>' 
            +'</a>'
            +'<ul class="dropdown-menu">'
            $.each(this.allDefaults(), function(index, value){
                message+='<li><a class="dropdown-item">'+ value +'</a></li>'
            })
            message+='</ul>'
            +'</div></div>'        
            $("#message").append(message)
        }

    }

    AfficherListAllDefault(dataEvolutionChart){
        this.dataEvolutionChart = dataEvolutionChart
        var totalDefault = 0
        $("#DiagTable").find('tbody').html()
        var laststate = Array(16).fill(false)
        var listdef = Array(16).fill([])
        this.dataEvolutionChart['def'].forEach((val, i) => {
            if(JSON.stringify(laststate) != JSON.stringify(this.convertirEnBooleens(val))){
                for (let j = 0; j <16; j++){
                    if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == true){
                        listdef[j].push([this.dataEvolutionChart['Date'][i]])
                    }else if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == false){
                        if(this.dataEvolutionChart['Date'][i] !="null"){
                            var end = this.dataEvolutionChart['Date'][i]
                        }else{
                            var end = this.dataEvolutionChart['Date'][i-1]
                        }
                        listdef[j].at(-1).push([])
                        $("#DiagTable").find('tbody').append("<tr>"
                        +'<td>'+ this.listDef[j] +'</td>'
                        +'<td>'+ listdef[j][0] +'</td>'
                        +'<td>'+ end +'</td>'
                        +'<td></td>'
                        +'</td>'
                        )
                        totalDefault+=1
                    }
                }
                laststate = this.convertirEnBooleens(val)
            }
        });
        var laststate = Array(16).fill(false)
        var listdef = Array(16).fill([])
        this.dataEvolutionChart['var_cir'].forEach((val, i) => {
            if(JSON.stringify(laststate) != JSON.stringify(this.convertirEnBooleens(val))){
                for (let j = 0; j <16; j++){
                    if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == true){
                        listdef[j].push([this.dataEvolutionChart['Date'][i]])
                    }else if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == false){
                        if(this.dataEvolutionChart['Date'][i] !="null"){
                            var end = this.dataEvolutionChart['Date'][i]
                        }else{
                            var end = this.dataEvolutionChart['Date'][i-1]
                        }
                        listdef[j].at(-1).push([])
                        $("#DiagTable").find('tbody').append("<tr>"
                        +'<td>'+ this.listVarCir[j] +'</td>'
                        +'<td>'+ listdef[j][0] +'</td>'
                        +'<td>'+ end +'</td>'
                        +'<td></td>'
                        +'</td>'
                        )
                        totalDefault+=1
                    }
                }
                laststate = this.convertirEnBooleens(val)
            }
        });
        var laststate = Array(16).fill(false)
        var listdef = Array(16).fill([])
        this.dataEvolutionChart['index6S'].forEach((val, i) => {
            if(JSON.stringify(laststate) != JSON.stringify(this.convertirEnBooleens(val))){
                for (let j = 0; j <16; j++){
                    if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == true){
                        listdef[j].push([this.dataEvolutionChart['Date'][i]])
                    }else if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == false){
                        if(this.dataEvolutionChart['Date'][i] !="null"){
                            var end = this.dataEvolutionChart['Date'][i]
                        }else{
                            var end = this.dataEvolutionChart['Date'][i-1]
                        }
                        listdef[j].at(-1).push([])
                        $("#DiagTable").find('tbody').append("<tr>"
                        +'<td>'+ this.listIndex6[j] +'</td>'
                        +'<td>'+ listdef[j][0] +'</td>'
                        +'<td>'+ end +'</td>'
                        +'<td></td>'
                        +'</td>'
                        )
                        totalDefault+=1
                    }
                }
                laststate = this.convertirEnBooleens(val)
            }
        });
        var laststate = Array(16).fill(false)
        var listdef = Array(16).fill([])
        this.dataEvolutionChart['dtcapt3mn'].forEach((val, i) => {
            if(JSON.stringify(laststate) != JSON.stringify(this.convertirEnBooleens(val))){
                for (let j = 0; j <16; j++){
                    if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == true){
                        listdef[j].push([this.dataEvolutionChart['Date'][i]])
                    }else if(this.convertirEnBooleens(val)[j] != laststate[j] && this.convertirEnBooleens(val)[j] == false){
                        if(this.dataEvolutionChart['Date'][i] !="null"){
                            var end = this.dataEvolutionChart['Date'][i]
                        }else{
                            var end = this.dataEvolutionChart['Date'][i-1]
                        }
                        listdef[j].at(-1).push([])
                        $("#DiagTable").find('tbody').append("<tr>"
                        +'<td>'+ this.listDtCapt[j] +'</td>'
                        +'<td>'+ listdef[j][0] +'</td>'
                        +'<td>'+ end +'</td>'
                        +'<td></td>'
                        +'</td>'
                        )
                        totalDefault+=1
                    }
                }
                laststate = this.convertirEnBooleens(val)
            }
        });
        $("#badgeTotalDefault").html(totalDefault)
    }

}