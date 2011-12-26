/* Royal Street Flash */

MapBox = function () {

    this.init = function (b, c, d, e) {
        var a = this;
        this.mapBlock = b; // inner container for map
        this.mapLayer = c; // where paint the map
        this.mapList = d; // array with address in attr title
        this.mapListLen = this.mapList.children().length;
        this.mapListChilds = this.mapList.children();
        this.mapLinkOppener = e;
        this.mapStartIndicator = 0;


        // координаты для начальной карты
        if(a.mapListLen >=1) {
            this.coord = (a.mapListChilds[0].getAttribute("title").split(","));
        }
        // проверка на несколько адресов
        if (a.mapListLen > 1) {
            var coord2 = [];
            for (var i=0; i <= (a.mapListLen-1); i++) {
                coord2[i] = {
                    "lat" : a.mapListChilds[i].getAttribute("title").split(",")[0],
                    "lng" : a.mapListChilds[i].getAttribute("title").split(",")[1]
                };
            }
            this.coord2 = coord2;
        } else {
            this.coord2 = a.coord;
        }


        // EVENTS & ACTIVATORS
        this.mapLinkOppener.click(function (i){
            if (a.mapStartIndicator == 0){
                mapBox.mapShow2();
            }
            a.mapStartIndicator = 1;

            var dis = a.mapLayer.css('display');
            if (dis == 'none') {
                a.mapLayer.show();
            } else {
                a.mapLayer.hide();
            }
            return false;
        });

        // штука для смены стиля ((((
        this.mapLinkOppener.mouseover(function(e) {
            $(this).parent().removeClass('shopsMapLink-off');
            $(this).parent().addClass('shopsMapLink-on');
        });
        this.mapLinkOppener.mouseout(function(e) {
            $(this).parent().removeClass('shopsMapLink-on');
            $(this).parent().addClass('shopsMapLink-off');
        });



    };



// FUNCTIONS

    /*
        отображение карты
        у ф-ции нет передаваемых параметров, они берутся из инита
    */
    this.mapShow2 = function () {
        // стартуем новую карту
        var latlng = new google.maps.LatLng(this.coord[0], this.coord[1]);

        // параметры
        var myOptions = {
            navigationControl: true,
            mapTypeControl: true,
            mapTypeControlOptions: {
                style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
                position: google.maps.ControlPosition.TOP_RIGHT},
            navigationControlOptions: {
                style: google.maps.NavigationControlStyle.SMALL},
            scaleControl: true,
            zoom: 15,
//            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        // цикл для множественных точек и поиска границ
        if (this.mapListLen > 1 ){
            // создаём пустые границы
            var bounds = new google.maps.LatLngBounds();
            // перебор координат
            for (var index in this.coord2) {
                var lat = this.coord2[index].lat;
                var lng = this.coord2[index].lng;
                latlng = new google.maps.LatLng(lat, lng);
                bounds.extend(latlng);
            }
            // отрисовка карты
            map = new google.maps.Map(document.getElementById("mapBoxContainer"), myOptions);
            // раздвигание границ ;)
            map.fitBounds(bounds);
        } else {
            var lat = this.coord2[0];
            var lng = this.coord2[1];
            latlng = new google.maps.LatLng(lat, lng);
            myOptions['center'] = latlng;
            map = new google.maps.Map(document.getElementById("mapBoxContainer"), myOptions);
        }

        // отрисовывание маркеров
        if (this.mapListLen > 1 ){ // если адресов несколько
            for (index in this.coord2) {
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(this.coord2[index].lat, this.coord2[index].lng),
                    map: map,
                    title:"Hello World!"
                });
            }
        } else { // если один
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(this.coord2[0], this.coord2[1]),
                map: map,
                title:"Hello World!"
            });
        }
    };


};



// START ON DOM READY
// inits for all stuff
$(document).ready(function () {
    mapBox = new MapBox();
    mapBox.init($("#mapBox"), $("#mapBoxContainer"), $("#addressMap"), $("#shopsMapLink a"));

});