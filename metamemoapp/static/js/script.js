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
});