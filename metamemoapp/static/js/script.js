window.mobileCheck = window.innerWidth <= 601;
$(document).ready(function () {
    $.when($.getJSON("http://127.0.0.1:8000/timeline/api/v1/fact/?limit=100000"),$.getJSON( "http://127.0.0.1:8000/timeline/api/v1/session/?limit=100000")).then(function(data,data_sessions){
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
        $.each( timelines, function( key, val ) {            
            nome_id = val["name"].split(' ').join('-');
            timeline_selectors.push(`
                <div class="col offset-s3 s6 m3 padding-top50 center-align">
                    <a id="${nome_id}" class="white-text">
                        <img src="https://picsum.photos/130" alt="" width="100%" class="circle darken-filter">
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
                <img src="https://picsum.photos/282" alt="" class="circle">
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
/*         $( "#ovo" ).after(`<section id="timeline-jair_bolsonaro" class="timeline-body active">
        <div class="center-align">
            <img src="https://picsum.photos/282" alt="" class="circle">
        </div>
        <div class="center-align metagreen-text font35 font26-s fontBold">
            JAIR MESSIAS BOLSONARO
        </div>
        <div class="start container center-align">
            <span class="bubble large metapink">1888</span>
            <img src="https://picsum.photos/670/375" alt="" class="z-depth-3">
            <p class="radius8 grey lighten-3"><b>Abril de 1888</b> - Vittorio 
    Bolsonaro emigra de Anguillara, na região do Vêneto, nordeste da Itália,
     para o Brasil. Aos dez anos, viaja com o pai, a mãe e dois irmãos. 
    Desembarcaram em Santos. Angelo, seu filho, casou com uma brasileira 
    descendente de alemães e teve Percy Geraldo, pai de Jair Messias 
    Bolsonaro em 1927.</p>
        </div>
        <div class="timeline-content">
            <div class="row timeline-board metagreen">
                <div><b>PARTE 1</b></div>
                Jair, infância e adolescência 
                <small>1955-1972</small>
            </div>
            <div class="row">
                <span class="bubble metagreen">1955</span>
                <div class="row">
                    <span data-target="modal1" class="bubble mini metagreen modal-trigger">JAN</span>
                </div>
                <div class="row">
                    <span data-target="modal1" class="bubble mini metagreen modal-trigger">FEV</span>
                </div>
            </div>
            <div class="row"><span class="bubble metagreen">1955</span></div>
            <div class="row"><span class="bubble metagreen">1955</span></div>
    
            <div class="row timeline-board metagold">
                <div><b>PARTE 2</b></div>
                Jair, de cadete à capitão
                <small>1973-1988</small>
            </div>
            <div class="row"><span class="bubble metagold">1955</span></div>
            <div class="row"><span class="bubble metagold">1955</span></div>
            <div class="row"><span class="bubble metagold">1955</span></div>
    
            <div class="row timeline-board metablue"> 
                <div><b>PARTE 3</b></div>
                Jair, de vereador a deputado polêmico 
                <small>1988- 2015</small>
            </div>
            <div class="row"><span class="bubble metablue">1955</span></div>
            <div class="row"><span class="bubble metablue">1955</span></div>
            <div class="row"><span class="bubble metablue">1955</span></div>
    
            <div class="row timeline-board metared">
                <div><b>PARTE 4</b></div>
                Jair, de vereador a deputado polêmico
                <small>1988- 2015</small> 
            </div>
            <div class="row"><span class="bubble metared">1955</span></div>
            <div class="row"><span class="bubble metared">1955</span></div>
            <div class="row"><span class="bubble metared">1955</span></div>
        </div>
    </section>`); */
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
    
/*     
    $.getJSON( "http://127.0.0.1:8000/timeline/api/v1/fact/?limit=100000", function( data ) {

    }); */
    $('.parallax').parallax();
    $('.resultado-slider .slider').slider({
        indicators: false,
        height: window.mobileCheck ? 400 : 340,
        duration: 0
    });
    setTimeout(function () {
        $('.resultado-slider .slider').slider('pause');
    }, 3000)
    if (!window.mobileCheck) {
        $('.blog .carousel').carousel({
            indicators: true,
            fullWidth: true,
            duration: 300,
            numVisible: 1,
            dist: 0,
            padding: 0,
            noWrap: true,
        });
    }

    $('.nav-arrow.nav-right').click(function (event) {
        $('.slider').slider('next');
        $('.slider').slider('pause');
    });
    $('.nav-arrow.nav-left').click(function (event) {
        $('.slider').slider('prev');
        $('.slider').slider('pause');
    });

    $('.materialboxed').materialbox();


    //Form de busca
    $('.metasearch #authors .author').click(function (event) {
        $(`.card[data-author="${event.currentTarget.textContent}"]`).parent().each(function (i, chip) {
            chip.classList.toggle("hide-author");
        });
        event.currentTarget.classList.toggle("transparent");
    })

    $('.metasearch #sources .source').click(function (event) {
        var source = event.currentTarget.getAttribute('data-source');
        $(`.card[data-source="${source}"]`).parent().each(function (i, chip) {
            chip.classList.toggle("hide-source");
        });
        event.currentTarget.classList.toggle("transparent");
    });

    $('.button').click(function (event) {
        var authors = $('.metasearch #authors .author:not(.transparent)')
            .map(function (i, chip) {
                return chip.getAttribute('data-author');
            }).get()

        var sources = $('.metasearch #sources .source:not(.transparent)')
            .map(function (i, chip) {
                return chip.getAttribute('data-source');
            }).get();

        var qs = {
            'author': authors,
            'source': sources,
            'content': $("#id_content").val()
        }

        var sd = M.Datepicker.getInstance($("#start_date")).date;
        var ed = M.Datepicker.getInstance($("#end_date")).date;

        if (sd) {
            let date = new Date(sd);
            qs['start_date'] = `${date.getUTCFullYear()}-${date.getUTCMonth() + 1}-${date.getDate()}`
        }
        if (ed) {
            let date = new Date(ed);
            qs['end_date'] = `${date.getUTCFullYear()}-${date.getUTCMonth() + 1}-${date.getDate()}`
        }
        qs = $.param(qs, true);

        window.location = `/lista/?${qs}`
    });

    //Datepicker
    $('.datepicker').datepicker({
        yearRange: [2008, 2022],
        i18n: {
            today: 'Hoje',
            clear: 'Limpar',
            done: 'Ok',
            nextMonth: 'Próximo mês',
            previousMonth: 'Mês anterior',
            weekdaysAbbrev: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S'],
            weekdaysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
            weekdays: ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado'],
            monthsShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        }
    });



    //Carrega filtros
    if ($("body").hasClass("search")) {
        var p = new URLSearchParams(window.location.search);

        // what does this do?
        $("#id_content").val(p.get("content"));

        //set date
        var start_date = M.Datepicker.getInstance($(".metasearch #start_date"))
        var end_date = M.Datepicker.getInstance($(".metasearch #end_date"))

        if (p.get('start_date')) {
            start_date.setDate(p.get("start_date"));
            start_date._finishSelection();
        }
        if (p.get('end_date')) {
            end_date.setDate(p.get("end_date"));
            end_date._finishSelection();
        }


        var redes = p.getAll("source");
        $('.metasearch #sources .source').each(function (i, rede) {
            var source = rede.getAttribute('data-source');
            if (redes.includes(source)) {
                rede.click();
            }
        });


        var authors = p.getAll("author");
        $('.metasearch #authors .author').each(function (i, chip) {
            var source = chip.getAttribute('data-author');
            if (authors.includes(source)) {
                chip.click();
            }
        });

    }

    //Baixa midia
    $("#get_media").click(function (event) {
        var url = event.currentTarget.getAttribute('href');
        $.ajax(url);
        $("#get_media").parent()[0].textContent = 'baixando...'
    });

    /*timeline*/

});