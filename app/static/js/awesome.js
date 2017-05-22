$(function() {
    var active = location.pathname.substr(0, 4) === '/uk/' ? 'uk-active' : 'active';
    if (location.pathname.indexOf('manage') !== -1) {
        $('#navbar-left>li:eq(1)').addClass(active);
    }
    else {
        $('#navbar-left>li:first').addClass(active);
    }
    $(window).scroll(function() {
        if($(this).scrollTop() >= $(this).height()) {
            $("#go-top").fadeIn();
        }
        else {
            $("#go-top").fadeOut();
        }
    });
    $("#go-top").click(function() {
        $("body").animate({scrollTop: 0}, 800, "swing");
    });
});