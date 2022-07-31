window.mobileCheck = window.innerWidth <= 601;
$(document).ready(function () {
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
    $('.transcript').click(function(event){
        if ($(this).hasClass('open')) {
            $(this).removeClass('open')
        } else {
            $(this).addClass("open");
        }
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
        console.log("alou")
        console.log(sd)
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
        defaultDate: new Date(Date.parse(this.value)),
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
    jQuery('.datepicker').each(function () {
        var newDate = new Date(Date.parse(this.value));
        $(this).datepicker('setDate', newDate);
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