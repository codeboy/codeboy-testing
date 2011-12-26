/* Royal Street Flash */

QBasket = function () {

    this.init = function (b, c, d, e, f, g) {
        var a = this;
        this.baskDataContainer = b; // where search
        this.baskAddButton = c; // button for add
        this.baskDelButton = d; // button for delete
        this.baskBlockContainer = e; // контейнер для миникорзины
        this.baskButtonPlus = f;
        this.baskButtonMinus = g;

        this.flagRegister = 0;


        // EVENTS & ACTIVATORS
        //----------------------------------------------------
        this.baskAddButton.click(function(e) {
            var ggg = $('#mmm');
            if (ggg.size() >= 1){
                alert(ggg)
            }
            var tParents = $(this).parent().parent()        // выбераем родителей
            var tNumber = tParents.find('.cCountInput input').attr('value')     // берём кол-во
            var tName = tParents.find('.cDescription').text()     // берём кол-во
            var tPrice = tParents.find('.cPrice').text()     // берём кол-во

            var tString = $(this).parent().find('.js-informer').text()          // находим строку с данными
            var tStringSplit = tString.split(';')                               // мэджик

            var message = '';

            // проверка на авторизацию
            if (tStringSplit[4] == 'False'){
                qPopBox.boxShow(
                    'Для добавления в корзину <a href="/registration/">зарегистрируйтесь</a> или <a href="/login/"> войдите',
                    3500
                );
            // если зарегистрирован
            } else {

                // делаем запрос
                $.post("/basket-add", {
                    item_id: tStringSplit[0],
                    brand_name : tStringSplit[1],
                    warehouse_id : tStringSplit[2],
                    value : tNumber
                },

                // отрабатываем возвращённое значение
                function(data) {
                    if (data == 'upd'){
                        message = 'Товар обновлён';
                        qBasket.basketBlockAddItem(tStringSplit[0], tStringSplit[1], tPrice, tNumber, tName)
                    } else if (data == 'add') {
                        message = 'Товар добавлен в корзину';
                        qBasket.basketBlockAddItem(tStringSplit[0], tStringSplit[1], tPrice, tNumber, tName)
                    } else if (data == 'error') {
                        message = 'Что-то пошло не так!'
                    }
                    qPopBox.boxShow(message);
                });
            }
            return false;
        });


        // ДОБАВЛЕНИЕ ОДНОГО ТОВАРА В КОРЗИНУ
        this.baskButtonPlus.click(function(e){
            var tParents = $(this).parent().parent()        // выбераем родителей
            var tNumber = tParents.find('.cCountInput').text()     // берём кол-во
            var tName = tParents.find('.cDescription').text()     // берём кол-во
            var tPrice = tParents.parent().find('.cPrice').text()     // берём кол-во

            var tString = $(this).parent().find('.js-informer').text()          // находим строку с данными
            var tStringSplit = tString.split(';')                               // мэджик

            var message = '';

            // проверка на авторизацию
            if (tStringSplit[4] == 'False'){
                qPopBox.boxShow(
                    'Для добавления в корзину <a href="/registration/">зарегистрируйтесь</a> или <a href="/login/"> войдите',
                    3500
                );
            // если зарегистрирован
            } else {
                var ggg = function () {
                    $(location).delay(1000).attr('href', '/basket/')
                }

                // делаем запрос
                $.post("/basket-add", {
                    item_id: tStringSplit[0],
                    brand_name : tStringSplit[1],
                    warehouse_id : tStringSplit[2],
                    value : 1
                },

                // отрабатываем возвращённое значение
                function(data) {
                    if (data == 'upd'){
                        message = 'Товар обновлён';
                        qBasket.basketBlockAddItem(tStringSplit[0], tStringSplit[1], tPrice, 1, tName)
                    } else if (data == 'add') {
                        message = 'Товар добавлен в корзину';
                        qBasket.basketBlockAddItem(tStringSplit[0], tStringSplit[1], tPrice, tNumber, tName)
                    } else if (data == 'error') {
                        message = 'Что-то пошло не так!'
                    }
                    qPopBox.boxModalShow(message, ggg   )
//                    $(location).delay(3000).attr('href', '/')
//                    setTimeout($(location).attr('href', '/'), 50000);
                });
            }
            return false;
        });


        this.baskDelButton.click(function(e) {
            var tParents = $(this).parent().parent()
            var tNumber = tParents.find('.cCountInput input').attr('value')

            var tString = $(this).parent().find('.js-informer').text()
            var tStringSplit = tString.split(';')

            $.post("/basket-del", {
                item_id: tStringSplit[0],
                brand_name : tStringSplit[1],
                warehouse_id : tStringSplit[2],
                price_id : tStringSplit[3],
                value : tNumber
            },
            function(data) {
                if (data == 'error'){
                    qPopBox.boxShow(data);
                } else {
                    var url = "/basket/";
                    $(location).attr('href',url);
                }
            });
            return false;
        });

    };



// FUNCTIONS
//----------------------------------------------------

    this.basketBlockAddItem = function(prod_id, brand, price, value, name){
        price = parseInt(price)
        value = parseInt(value)

        var iContainer = this.baskBlockContainer.find('.'+brand+'-'+prod_id);
        var iSummContainer = this.baskBlockContainer.find('#js-basketTotalPrice')
        var iSumm = parseFloat(iSummContainer.text())
        if (iContainer.size() >= 1){
            var iNumberContainer = iContainer.find('.js-itemNumber');
            var iNumberText = parseInt(iNumberContainer.text());
            var iPriceContainer = iContainer.find('.js-itemPrice')
            var iPriceText = parseInt(iPriceContainer.text())

            iNumberContainer.text(iNumberText+(value));
            iPriceContainer.text(iPriceText+(price*value))

            iSummContainer.text(iSumm + (price * value) )

        } else {
            var zzz = this.baskBlockContainer.find('ul')
            zzz.append('<li class="'+brand+'-'+prod_id+'"><a href="/">'+name+'<span>(<span class="js-itemNumber">'+
                value+'</span> шт)</span></a><abbr><span  class="js-itemPrice">'+(value * price)+
                '</span> р</abbr><div class="clear"></div></li>'
            )

            var dfdf = (price * value)
            var gtgt = (iSumm+dfdf)
            iSummContainer.text(iSumm + dfdf)
        }

    }
};
//#####   END   ############################################################################




/* Popup window
==========================================================================================*/
QPopBox = function () {
    this.init = function () {
        var a = this;
        this.boxContainer = $('body'); // where append
        this.boxKey = $(document.documentElement); //
        this.boxStartFlag = 0;
        this.boxOpenFlag = 0;

        this.boxStart()
        this.boxContentBlock = $('#js-boxPopContainer')


        // EVENTS & ACTIVATORS
    };



// FUNCTIONS

    this.boxStart = function () {
        this.boxContainer.append('<div id="js-boxPopContainer"></div>');
        qPopBox.boxPopId = $('#js-boxPopContainer');

        var iContainer = qPopBox.boxPopId;
        var windowHeight = $(window).height();
        var windowWidth = $(window).width();

        iContainer.css('left', (windowWidth/2)-200).css('top', ((windowHeight/2)-150));
//        qPopBox.boxStartFlag = 1
    };

    this.boxOpen = function(subj, width, height) {
//        if (qPopBox.boxStartFlag === 0) {qPopBox.boxStart()}

        subj = typeof(subj) != 'undefined' ? subj : 'KeKeKe';
        width = typeof(width) != 'undefined' ? width : 250;
        height = typeof(height) != 'undefined' ? height : 80;

        this.boxPopId.css('width', width)
        this.boxPopId.css('height', height)

        this.boxContentBlock.html(subj);
        this.boxContentBlock.fadeIn();
        this.boxOpenFlag = 1;
    };

    this.boxClose = function (time){
        time = typeof(time) != 'undefined' ? time: 300;
        this.boxContentBlock.delay(time).fadeOut()
        this.boxOpenFlag = 0;
    };

    this.boxChange = function(subj, width, height) {
        subj = typeof(subj) != 'undefined' ? subj : 'KeKeKe';
        width = typeof(width) != 'undefined' ? width : 250;
        height = typeof(height) != 'undefined' ? height : 80;

        this.boxPopId.css('width', width),
        this.boxPopId.css('height', height);

        var iContainer = this.boxPopId;
        var windowHeight = $(window).height();
        var windowWidth = $(window).width();

        iContainer.css('left', (windowWidth/2)-width).css('top', ((windowHeight/2)-height));

        this.boxContentBlock.html(subj);
    };


    this.boxShow = function (subj, time, cbFunction) {
        subj = typeof(subj) != 'undefined' ? subj : 'KeKeKe';
        time = typeof(time) != 'undefined' ? time : 1100;
        cbFunction = typeof(cbFunction) != 'undefined' ? cbFunction : false;

        if (cbFunction != false){
            this.boxOpen(subj),this.boxClose(time);
//            this.cbFunctions
        } else {
            this.boxOpen(subj),this.boxClose(time);
        }

    };


    this.boxModalShow = function(subj, cbFunction, time, width, height){
        subj = typeof(subj) != 'undefined' ? subj : 'KeKeKe';
        time = typeof(time) != 'undefined' ? time : 0;
        width = typeof(width) != 'undefined' ? width : 400;
        height = typeof(height) != 'undefined' ? height : 300;

        var subjData = '<div class="js-boxModalContent">'+subj+'</div>'+
            '<div class="js-boxModalButtons">' +
            '<button name="jsBoxClose" id="js-boxClose">отмена</button>' +
            '<button name="jsBoxSend" id="js-boxSend">сохранить</button>'

//        this.boxOpen(subjData, time, width, height);
        this.boxOpen(subjData, width, height);
        $('#js-boxSend').click(cbFunction)
        $('#js-boxClose').click(function(){
            qPopBox.boxClose(time);
        })
    }
};
//#####   END   ############################################################################




QOpener = function(){
    this.init = function (b, c) {
        var a = this;
        this.openerTriggerList = b;
        this.openerContent = c;
        this.openerFlag = 0;

        // EVENTS & ACTIVATORS
        this.openerTriggerList.live('click', function() {
            if (a.openerFlag == 1){
                qOpener.openerClose();
            }
            else {
                qOpener.openerOpen();
            }
        });
    };

    // FUNCTIONS
    this.openerOpen = function(){
        this.openerContent.show();
        this.openerFlag = 1;
    };
    this.openerClose = function(){
        this.openerContent.hide();
        this.openerFlag = 0;
    };
    return false;
};
//#####   END   ############################################################################



/*
*********************************************************************/
QAddress = function() {
    this.init = function(b, c, d){
        var a = this;
        this.adAddButton = b;
        this.adEditButton = c;
        this.adDelButton = d;

        this.adAddButton.click(function(){

            var adData = '<h1>Добавить адрес</h1><form name="addrForm" id="addrForm" method="post" action="/delivery-address-add"> ' +
    '<div><label for="id_item_index">Индекс</label><input type="text" name="item_index" id="id_item_index" /></div>'+
    '<div><label for="id_city">Город</label><input id="id_city" type="text" name="city" value="Санкт-Петербург" maxlength="25" /></div>'+
    '<div><label for="id_street_type">Тип улицы</label><select name="street_type" id="id_street_type">' +
        '<option value="">---------</option>' +
        '<option value="UL" selected="selected">ул</option>' +
        '<option value="PR">просп</option>' +
        '<option value="PE">пер</option>' +
        '<option value="NA">наб</option>' +
        '<option value="AL">аллея</option>' +
        '<option value="HW">шоссе</option>' +
        '<option value="PZ">проезд</option>' +
        '<option value="LI">линия</option>' +
        '<option value="LU">луч</option>' +
        '<option value="SP">спуск</option>' +
        '<option value="SE">съезд</option>' +
    '</select></div>'+
    '<div><label for="id_street_name">Название улицы</label><input id="id_street_name" type="text" name="street_name" maxlength="35" /></div>'+
    '<div><label for="id_house">Дом</label><input type="text" name="house" id="id_house" /></div>'+
    '<div><label for="id_corpus">Корпус</label><input type="text" name="corpus" id="id_corpus" /></div>'+
    '<div><label for="id_appartment">Офис / Квартира</label><input id="id_appartment" type="text" name="appartment" maxlength="10" /></div>' +
    '</form>'

            qPopBox.boxModalShow(adData, function(){
                $('#addrForm').ajaxSubmit();
                var url = "";
                qPopBox.boxChange('Адрес добавлен', 100, 30),qPopBox.boxClose(10800).$(location).attr('href',url);
                return false;
            });
        return false;
        });


        this.adEditButton.click(function(){
            var iContainer = $(this).parent()
            var iVarIndex = iContainer.find('.js-delIndex').text()
            var delCity = iContainer.find('.js-delCity').text()
            var delStrType = iContainer.find('.js-delStrType').text()
            var delStrName = iContainer.find('.js-delStrName').text()
            var delHouse = iContainer.find('.js-delHouse').text()
            var delCorpus = iContainer.find('.js-delCorpus').text()
            var delApp = iContainer.find('.js-delApp').text()
            var delID = iContainer.find('.js-delID').text()

            var adData = '<h1>Редактировать адрес</h1><form name="addrForm" id="addrForm" method="post" action="/delivery-address-add"> ' +
    '<div><label for="id_item_index">Индекс</label><input type="text" name="item_index" id="id_item_index" value="'+iVarIndex+'" /></div>'+
    '<div><label for="id_city">Город</label><input id="id_city" type="text" name="city" value="'+delCity+'" maxlength="25" /></div>'+
    '<div><label for="id_street_type">Тип улицы</label><select name="street_type" id="id_street_type">' +
        '<option value="">---------</option>' +
        '<option value="UL"'
        if (delStrType == "UL" || delStrType ===""){adData = adData +' selected="selected" '}
        adData = adData +' >ул</option><option value="PR" '
        if (delStrType == 'PR'){adData = adData +' selected="selected" '}
        adData = adData +'>просп</option><option value="PE" '
        if (delStrType == 'PE'){adData = adData +' selected="selected" '}
        adData = adData +'>пер</option><option value="NA" '
        if (delStrType == 'NA'){adData = adData +' selected="selected" '}
        adData = adData +'>наб</option><option value="AL" '
        if (delStrType == 'AL'){adData = adData +' selected="selected"'}
        adData = adData +'>аллея</option>' +
        '<option value="HW">шоссе</option>' +
        '<option value="PZ">проезд</option>' +
        '<option value="LI">линия</option>' +
        '<option value="LU">луч</option>' +
        '<option value="SP">спуск</option>' +
        '<option value="SE">съезд</option>' +
    '</select></div>'+
    '<div><label for="id_street_name">Название улицы</label><input id="id_street_name" type="text" name="street_name" maxlength="35" value="'+delStrName+'" /></div>'+
    '<div><label for="id_house">Дом</label><input type="text" name="house" id="id_house" value="'+delHouse+'" /></div>'+
    '<div><label for="id_corpus">Корпус</label><input type="text" name="corpus" id="id_corpus" value="'+delCorpus+'" /></div>'+
    '<div><label for="id_appartment">Офис / Квартира</label><input id="id_appartment" type="text" name="appartment" value="'+delApp+'" maxlength="10" /></div>' +
    '<div><input id="delID" type="hidden" name="delID" value="'+delID+'" /></div>' +
    '</form>'


            qPopBox.boxModalShow(adData, function(){
                $('#addrForm').ajaxSubmit();
                qPopBox.boxChange('Адрес изменён', 100, 30),qPopBox.boxClose(800);
                var url = "";
                $(location).attr('href',url);
                return false;
            });
        return false;
        });


        this.adDelButton.click(function(){
            var delID = $(this).parent().find('.js-delID').text()

            $.post("/delivery-address-del", {
                delID: delID
            },
            function(data) {
                if (data == 'error'){
                    qPopBox.boxShow(data);
                } else {
                    var url = "";
                    $(location).attr('href',url);
                }
            });

        return false;
        });


    return false;
    };

    this.adSendAjax = function(){
//        qAddress.adMakeVars()
//
//        $.post("/delivery-address-add", {
//            adrApp: qAddress.adVarApp
//        }, function(data) {
//            qPopBox.boxShow(data);
//        });


    };

    this.adStartModal = function() {
    };

    this.adMakeVars = function(){
        var adVarContainer = $('#js-boxModalContent');
        qAddress.adVarIndex = $('#js-adrIndex').val()
        qAddress.adVarCity = $('#js-adrCity').val()
        qAddress.adVarStrType = $('#js-adrStrType').val()
        qAddress.adVarStrName = $('#js-adrStrName').val()
        qAddress.adVarHouse = $('#js-adrHouse').val()
        qAddress.adVarCorp = $('#js-adrCorp').val()
        qAddress.adVarApp = $('#js-adrApp').val()
    };
    return false;
};
//#####   END   ############################################################################




QCarList = function() {
    this.init = function(b, c, d){
        var a = this;
        this.carBrandInput = b;
        this.carModelInput = c;
        this.carVaryInput = d;

        this.carModelInput.attr("disabled", true)
        this.carVaryInput.attr("disabled", true)

        this.carBrandInput.change(function(){
            var valBrand = $(this).val();
            qCarList.carChangeBrand(valBrand);
        });

        this.carModelInput.change(function(){
            var valModel = $(this).val();
            qCarList.carChangeModel(valModel);
        });
    };

    this.carChangeBrand = function(brand){
        brand = typeof(brand) != 'undefined' ? brand : 'none';
        if (brand == 'none' || brand == ''){
            this.carModelInput.attr("disabled", true);
            this.carVaryInput.attr("disabled", true);
        } else {
            qCarList.carModelInput.attr("disabled", true);
            qCarList.carModelInput.empty();
            qCarList.carModelInput.append('<option value>загружаем</option>')

            var callback = function(request){
                qCarList.carModelInput.empty();
                qCarList.carModelInput.append('<option value>----</option>')
                for(var x=0; x < request.length; x++ ){
                    var active = request[x];
                    qCarList.carModelInput.append('<option value="'+active.pk+'">'+active.fields.name+'</option>');
                }
                qCarList.carModelInput.attr("disabled", false);
            };
            qCarList.carPost('brand', brand, callback);

        }
    };

    this.carChangeModel = function(model){
        model = typeof(model) != 'undefined' ? model : 'none';
        if (model == 'none' || model == ''){
            this.carVaryInput.attr("disabled", true);
        } else {
            qCarList.carVaryInput.attr("disabled", true);
            qCarList.carVaryInput.empty();
            qCarList.carVaryInput.append('<option value>загружаем</option>')

            var callback = function(request){
                qCarList.carVaryInput.empty();
                qCarList.carVaryInput.append('<option value>----</option>')
                for(var x=0; x < request.length; x++ ){
                    var active = request[x];
                    qCarList.carVaryInput.append('<option value="'+active.pk+'">'+active.fields.name+'</option>');
                }
                qCarList.carVaryInput.attr("disabled", false);
            };
            qCarList.carPost('model', model, callback);

        }
    };


    this.carPost = function(type, val, func){
        $.post("/aj-carform/", {
                type : type,
                value : val
            },
            function(data) {
//                var ggg = jQuery.parseJSON(data.dump)
//                for(var x=0; x < ggg.length; x++ ){
//                    var active = ggg[x];
//                    alert('id: '+active.fields.name);
//                }
                if (data == 'error'){
                    qPopBox.boxShow(data);
                } else {
//                    alert(data)
                    func(jQuery.parseJSON(data.dump));
//                    return jQuery.parseJSON(data)

                }
            });
    };
    return false;
};






// START ON DOM READY
// inits for all stuff
$(document).ready(function () {
    qBasket = new QBasket();
    qBasket.init(
        $('#searchResult'),         // блок для результтов поиска
        $("a.js-basketAdd"),        // кнопка - добавить в корзину
        $("a.js-basketDel"),        // кнопка удалить
        $("#js-basketBlock"),        // блок для миникорзины
        $('a.js-basketPlus'),
        $('a.js-basketDeduct')
    );


    qPopBox = new QPopBox();
    qPopBox.init();

    qOpener = new QOpener();
    qOpener.init($('.js-openerTrigger'), $('.js-openerContent'));


    qAddress = new QAddress();
    qAddress.init($('#js-addressAdd'), $('a.js-delEdit'), $('a.js-delDelete'));

    qCarList = new QCarList();
    qCarList.init($('#id_producer'), $('#id_model'), $('#id_vary'))
});