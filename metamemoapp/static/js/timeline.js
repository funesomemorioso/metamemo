$(document).ready(function () {
    var origin   = window.location.origin;
    $.when($.getJSON(origin+"/timeline/api/v1/fact/?limit=100000"),$.getJSON( origin+"/timeline/api/v1/session/?limit=100000")).then(function(data,data_sessions){
        //formatação das datas 
        const option = {
            year: 'numeric',
            month: ('long' || 'short' || 'numeric'),
            day: 'numeric',
        }
        const locale = 'pt-br'

        
        all_timelines = data[0]["objects"].map(function(A) {return A["timeline"];});
        timelines = all_timelines.filter((value, index, self) =>
            index === self.findIndex((t) => (
                t.place === value.place && t.name === value.name
            ))
        );
        timeline_selectors = [];
        facts = []
        sessions = []
        facts_timelines = []
        selectors_width = 100/timelines.length
        $("#timeline_style").text(`@media (min-width: 600px) {.timeline-seletor .ovo.m3{width:${selectors_width}%;}}`);
        $.each( timelines, function( key, val ) {            
            nome_id = val["name"].split(' ').join('-');
            timeline_selectors.push(`
                <div class="ovo col offset-s3 s6 m3 padding-top50 center-align">
                    <a id="${nome_id}" class="white-text">
                        <img src="${val["image"]}" alt="" width="100%" class="miniature circle darken-filter">
                        <br>${val["name"]}
                    </a>
                </div>
            `);
            facts.push({timeline: val["id"],name:val["name"],facts:data[0]["objects"].filter(obj => {
                return obj["timeline"]["id"] === val["id"]
            })});
            sessions.push({timeline: val["id"],sessions:data_sessions[0]["objects"].filter(obj => {
                return obj["timeline"]["id"] === val["id"]
            })});
        });
        $( ".timeline-seletor" ).html(timeline_selectors.join( "" ));
        
        $.each(facts, function(this_tl_key,this_tl_facts){
            //sort this timeline's facts
            this_tl_facts["facts"].sort(function(a,b){
                return new Date(a.date) - new Date(b.date);
            });
            this_tl_sessions = sessions[this_tl_key]
            //sort this timeline's sessions
            this_tl_sessions["sessions"].sort(function(a,b){
                return new Date(a.start) - new Date(b.start);
            });
            console.log("oooooooo")
            console.log(this_tl_sessions)
            
            //this timeline's header
            
            tl = [] // this_timeline's list of session objects with facts categorized by date inside 
            //session colors list to loop over
            session_cores = ["metablue","metagreen","metaroxo","metagold","metared"]
            $.each(this_tl_sessions["sessions"],function(session_key,session){
                //loop over colors
                cor_atual = session_cores[session_key % session_cores.length]
                //add session to TL 
                tl.push({session:session["title"],text:session["text"],start:session["start"],end:session["end"],color:cor_atual,years:{}}) 
            });
            $.each(this_tl_facts["facts"],function(fact_key,fact){
                let data_t = new Date(fact["date"])
                function isAround(object){//checks if session encompases this date
                    return data_t > new Date(object["start"]) && data_t <  new Date(object["end"]);
                }      
                sess_id = tl.findIndex(isAround);//finds the first session that encompasses this date
                dia = data_t.getDate() 
                mes = data_t.toLocaleString("pt-BR", { month: "long" });
                mesin = data_t.toLocaleString("pt-BR", { month: "short" });
                ano = data_t.getFullYear()
                //console.log(`${dia} de ${mes} - ${ano}`)
                if(sess_id == -1){

                }else{
                    if(tl[sess_id]["years"][ano]===undefined){
                        tl[sess_id]["years"][ano]={};
                    }
                    if(tl[sess_id]["years"][ano][mesin]===undefined){
                        tl[sess_id]["years"][ano][mesin]=[];
                    }
                    tl[sess_id]["years"][ano][mesin].push(fact)
                }
            });
            console.log("end_tl")
            console.log(tl)
            
            $( "#ovo" ).after(`<section id="timeline-${this_tl_facts["name"].split(' ').join('-')}" class="timeline-body"></section>`)
            var sessions_list = []
            $.each( tl, function( sesh_key, this_sesh ) {
                let ts_key = this_sesh["session"].replace(/^[^a-z]+|[^\w:.-]+/gi, "");
                var sessio = `<div class="row timeline-board ${this_sesh["color"]}">
                    <div><b>${this_sesh["session"]}</b></div>
                    ${this_sesh["text"]}
                    <small>${new Date(this_sesh["start"]).getFullYear()}-${new Date(this_sesh["end"]).getFullYear()}</small>
                    </div>`;
                var sessio_years = []
                var sessio_modals = []
                $.each( this_sesh["years"], function( y_key, this_year ) {
                    ano_ini = `<div class="row">
                    <span class="bubble ${this_sesh["color"]}">${y_key}</span>`
                    ano_fim = `</div>` 
                    this_year_months = []
                    $.each(this_year,function( m_key, this_month ) {
                        mesio = `
                        <div class="row">
                            <span data-target="modal-${(m_key.split('.').join(""))+"-"+y_key+"-"+ts_key}" class="bubble mini ${this_sesh["color"]} modal-trigger">${m_key.split('.').join("").toUpperCase()}</span>
                        </div>
                        `
                        month_modal = [`
                        <div id="modal-${(m_key.split('.').join(""))+"-"+y_key+"-"+ts_key}" class="modal timeline-modal" tabindex="0" style="z-index: 1003; display: none; opacity: 0; top: 4%; transform: scaleX(0.8) scaleY(0.8);">
                            <div class="modal-content">
                        `]
                        $.each(this_month,function( f_key, this_fact ) {
                            const option = {
                                year: 'numeric',
                                month: ('long' || 'short' || 'numeric'),
                                day: 'numeric',
                            }
                            const locale = 'pt-br'
                            data_str = new Date(this_fact["date"]).toLocaleDateString( locale, option)
                            factio = `
                            <p class="radius8 metapink white-text" title="source: ${this_fact["source"]} (${this_fact["resource_uri"]})"><b>${data_str}</b> - ${this_fact["text"]}</p>
                            `
                            month_modal.push(factio)
                            if(this_fact["image"] != null){
                                imagio =`<img src="${this_fact["image"]}" alt="" class="z-depth-3">`
                                month_modal.push(imagio)
                            }
                        });
                        month_modal.push(`</div>
                        </div>`)
                        this_year_months.push(mesio)
                        sessio_modals.push(month_modal.join( "" ))
                    })
                    anio=(ano_ini+this_year_months.join( "" )+ano_fim)
                    sessio_years.push(anio)
                });
                sessions_list.push(sessio+sessio_years.join( "" ))
                $("section.no-padding-bottom").after(sessio_modals.join( "" ))
            });
            console.log("ovo")
            console.log(this_tl_facts)
            this_tl_destaque_image = ""
            if(this_tl_facts["facts"][0]["image"]!= null){
                this_tl_destaque_image = `<span class="bubble large metapink">${new Date(this_tl_facts["facts"][0]["date"]).getFullYear()}</span><img src="${this_tl_facts["facts"][0]["image"]}" alt="" class="z-depth-3"/>`
            }
            $(`#timeline-${this_tl_facts["name"].split(' ').join('-')}`).append(`
            <div class="center-align">
                <img src="${this_tl_facts["facts"][0]["timeline"]["image"]}" alt="" class="circle">
            </div>
            <div class="center-align metagreen-text font35 font26-s fontBold">
                ${this_tl_facts["name"].toUpperCase()}
            </div>
            <div class="start container center-align">
                ${this_tl_destaque_image}
                <p class="radius8 grey lighten-3"><b>${new Date(this_tl_facts["facts"][0]["date"]).toLocaleDateString( locale, option)}</b> - ${this_tl_facts["facts"][0]["text"]}</p>
            </div>
            <div class="timeline-content">
                ${sessions_list.join( "" )}
            </div>
            `);
            
        })  
        $('.timeline-seletor a').each(function(index, el) {
            $(this).click(function(event) {
                $('.timeline-body').removeClass('active');
                $(`#timeline-${this.id}`).addClass('active');
            });
        });
        $('.timeline-content > .row').each(function(index, el) {
            var row = this;
            $(row).find('> .bubble').click(function(event) {
                $(row).toggleClass('active');
            });
        });
        $('.modal').modal();
    });
});