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
        $(`.card[data-author="${event.currentTarget.textContent}"]`).each(function (i, chip) {
            chip.classList.toggle("hide");
        });
        event.currentTarget.classList.toggle("transparent");
    })

    $('.metasearch #sources .source').click(function(event) {
        var source = event.currentTarget.getAttribute('data-source');
        $(`.card[data-source="${source}"]`).each(function (i, chip) {
            chip.classList.toggle("hide");
        });
        event.currentTarget.classList.toggle("transparent");
    });

    $('.button').click(function(event) {
        var metamemos = []
        $('.metasearch #authors .author:not(.transparent)').each(function (i, chip) {
            metamemos.push(chip.getAttribute('data-author'));
        })
        
        var redes = []
        $('.metasearch #sources .source:not(.transparent)').each(function (i, chip) {
            redes.push(chip.getAttribute('data-source'));
        });
        var data = new Date($("#date-hidden")[0].value);
        
        var qs = $.param({"authors":metamemos.toString(), "sources":redes.toString()})
        
        window.location = `/search/${data.getUTCFullYear()}/${data.getUTCMonth()+1}/${data.getDate()}?${qs}`
    });

    //Datepicker
    var picker_date = new Date()
    picker_date.setDate(picker_date.getDate()-1);
    
    if ($("body").hasClass("search")) {
        picker_date = new Date($("#date-hidden")[0].value)
        picker_date.setMinutes(picker_date.getMinutes() + picker_date.getTimezoneOffset());
    }
    else {
        $("#date-hidden")[0].value = picker_date.toISOString();
    }
    
    $('.datepicker').datepicker({
        yearRange: [2008,2022],
        defaultDate: picker_date,
        setDefaultDate: true,
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
        },
        onSelect: function (d) {
            $("#date-hidden")[0].value = d.toISOString();
        }

    });



    //Carrega filtros
    if ($("body").hasClass("search")) {
        const queryString = window.location.search;
        var p = new URLSearchParams(queryString);
        var authors = p.get("authors").split(",");
        var redes = p.get("sources").split(",");

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
});