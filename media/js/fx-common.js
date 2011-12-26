LoginBox = function () {
    this.init = function (b, f, e, h, c, a, g) {
        var d = this;
        this.activeLayer = b;
        this.blockLayer = f;
        this.hideLayer = e;
        this.loginForm = h;
        this.submitController = g;
        this.usernameInput = c;
        this.passwordInput = a;
        this.isOpen = false;
        this.activeLayer.click(function (i) {
            var j = d.activeLayer.offset();
            d.blockLayer.css({
                top: j.top + 25 + "px",
                left: j.left - 31 + "px"
            });
            if (!d.isOpen) {
                d.show();
                d.isOpen = true
            } else {
                d.hide();
                d.isOpen = false
            }
        });
        this.hideLayer.click(function (i) {
            d.hide();
            d.isOpen = false
        });
        this.usernameInput.focus(function (i) {
            if (d.usernameInput.attr("value") == "EMAIL") {
                d.usernameInput.attr("value", "")
            }
        });
        this.usernameInput.blur(function (i) {
            if (d.usernameInput.attr("value") == "") {
                d.usernameInput.attr("value", "EMAIL")
            }
        });
        this.usernameInput.keypress(function (i) {
            if (i.which == 13) {
                d.submit()
            }
        });
        this.passwordInput.focus(function (i) {
            if (d.passwordInput.attr("value") == "PASSWORD") {
                d.passwordInput.attr("value", "")
            }
        });
        this.passwordInput.blur(function (i) {
            if (d.passwordInput.attr("value") == "") {
                d.passwordInput.attr("value", "PASSWORD")
            }
        });
        this.passwordInput.keypress(function (i) {
            if (i.which == 13) {
                d.submit()
            }
        });
        this.submitController.click(function (i) {
            d.submit()
        })
    };
    this.show = function () {
        this.blockLayer.slideDown("normal")
    };
    this.hide = function () {
        this.blockLayer.slideUp("normal")
    };
    this.submit = function () {
        this.loginForm.submit()
    }
};





$(document).ready(function () {
    loginBox = new LoginBox();
    loginBox.init($("#js-login-active"), $("#js-login-block"), $("#js-login-hide"), $("#js-login-form"), $("#js-login-username"), $("#js-login-password"), $("#js-login-send"));