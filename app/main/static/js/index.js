document.addEventListener('DOMContentLoaded', function() {    
    show_header();
    setInterval('show_header()', 5000);

    $('.ankor').on('click', function () {
        event.preventDefault();
        var id = $(this).attr('href'),
                top = $(id).offset().top - 55;
        $('body,html').animate({scrollTop: top}, 1000, 'linear');
    })   
}, false);   

function show_header()
{
    var cat_name_mass = [ "Недвижимость", "Авто", "Личные вещи", "Услуги", "Работа", "Запчасти и аксессуары", "Электроника", "Хобби и отдых"];
    var color_mass = ["#00aaff", "#97cf26", "#ff6163", "#a169f7", "#00aaff", "#97cf26", "#ff6163", "#a169f7"];
    var i = 0;
    var cat_name = document.getElementById('cat_name').innerHTML.trim();

    if (cat_name_mass[0] == cat_name) {
        i = 1;
    } else if (cat_name_mass[1] == cat_name) {
        i = 2;
    } else if (cat_name_mass[2] == cat_name) {
        i = 3;
    } else if (cat_name_mass[3] == cat_name) {
        i = 0;
    }
    document.getElementById('cat_name').innerHTML = cat_name_mass[i];
    document.getElementById('cat_name').setAttribute('style', 'color: ' + color_mass[i]);
}