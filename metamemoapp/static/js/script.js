window.mobileCheck  = window.innerWidth <= 601;
$(document).ready(function(){
    $('.parallax').parallax();
    $('.resultado-slider .slider').slider({
        indicators: false,
        height : window.mobileCheck ? 400 : 340,
        duration : 0
    });
    setTimeout(function (){
        $('.resultado-slider .slider').slider('pause');
    },3000)
    if (!window.mobileCheck) {
        $('.blog .carousel').carousel({
            indicators: true,
            fullWidth : true,
            duration : 300,
            numVisible :  1,
            dist: 0,
            padding: 0,
            noWrap: true,
        });
    }
    
    $('.nav-arrow.nav-right').click(function(event) {
        $('.slider').slider('next');
        $('.slider').slider('pause');
    });
    $('.nav-arrow.nav-left').click(function(event) {
        $('.slider').slider('prev');
        $('.slider').slider('pause');
    });
    
    $('.materialboxed').materialbox();

    
    //Form de busca
    $('.metasearch #authors .author').click(function(event) {
        $(`.card[data-author="${event.currentTarget.textContent}"]`).parent().each(function (i, chip) {
            chip.classList.toggle("hide-author");
        });
        event.currentTarget.classList.toggle("transparent");
    })

    $('.metasearch #sources .source').click(function(event) {
        var source = event.currentTarget.getAttribute('data-source');
        $(`.card[data-source="${source}"]`).parent().each(function (i, chip) {
            chip.classList.toggle("hide-source");
        });
        event.currentTarget.classList.toggle("transparent");
    });

    $('.button').click(function(event) {
        var authors = [];
        
        $('.metasearch #authors .author:not(.transparent)').each(function (i, chip) {
            authors.push(chip.getAttribute('data-author'));
        })
        
        var sources = [];
        $('.metasearch #sources .source:not(.transparent)').each(function (i, chip) {
            sources.push(chip.getAttribute('data-source'));
        });
        
        var qs = {
            'author' : authors,
            'source' : sources,
            'content' : $("#id_content").val()
        }

        var sd =  new Date(M.Datepicker.getInstance($("#start_date")).date);
        var ed = new Date(M.Datepicker.getInstance($("#end_date")).date);

        if (sd) {
            qs['start_date'] = `${sd.getUTCFullYear()}-${sd.getUTCMonth()+1}-${sd.getDate()}`
        }
        if (ed) {
            qs['end_date'] = `${ed.getUTCFullYear()}-${ed.getUTCMonth()+1}-${ed.getDate()}`
        }
        qs = $.param(qs, true);
        
        window.location = `/lista/?${qs}`
    });

    //Datepicker
    $('.datepicker').datepicker({
        yearRange: [2008,2022],
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
        const queryString = window.location.search;
        var p = new URLSearchParams(queryString);
        var authors = p.getAll("author");
        var redes = p.getAll("source");

        $("#id_content").val(p.get("content"));
        //set date
        var start_date = M.Datepicker.getInstance($(".metasearch #start_date"))
        var end_date = M.Datepicker.getInstance($(".metasearch #end_date"))
        
        start_date.setDate(p.get("start_date"));
        start_date._finishSelection();

        end_date.setDate(p.get("end_date"));
        end_date._finishSelection();

        $('.metasearch #sources .source').each(function (i, rede) {
            var source = rede.getAttribute('data-source');
            if (redes.includes(source)) {
                rede.click();
            }
        });
        

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


});