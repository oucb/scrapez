function checkWidth(init)
{
    /*If browser resized, check width again */
    if ($(window).width() < 768) {
        $('#main-nav').addClass('nav-stacked');
    } else {
        if (!init) {
            $('#main-nav').removeClass('nav-stacked');
        }
    }
}

$(document).ready(function() {
    checkWidth(true);

    $(window).resize(function() {
        checkWidth(false);
    });
});
