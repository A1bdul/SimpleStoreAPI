$(function () {
    "use strict";
    //Loader
    $(function preloaderLoad() {
        if ($('.preloader').length) {
            $('.preloader').delay(200).fadeOut(300);
        }
        $(".preloader_disabler").on('click', function () {
            $("#preloader").hide();
        });
    });

    // Script Navigation
    !function (n, e, i, a) {
        n.navigation = function (t, s) {
            var o = {
                    responsive: !0,
                    mobileBreakpoint: 992,
                    showDuration: 300,
                    hideDuration: 300,
                    showDelayDuration: 0,
                    hideDelayDuration: 0,
                    submenuTrigger: "hover",
                    effect: "fade",
                    submenuIndicator: !0,
                    hideSubWhenGoOut: !0,
                    visibleSubmenusOnMobile: !1,
                    fixed: !1,
                    overlay: !0,
                    overlayColor: "rgba(0, 0, 0, 0.5)",
                    hidden: !1,
                    offCanvasSide: "left",
                    onInit: function () {
                    },
                    onShowOffCanvas: function () {
                    },
                    onHideOffCanvas: function () {
                    }
                }, u = this, r = Number.MAX_VALUE, d = 1, f = "click.nav touchstart.nav", l = "mouseenter.nav",
                c = "mouseleave.nav";
            u.settings = {};
            var t = (n(t), t);
            n(t).find(".nav-menus-wrapper").prepend("<span class='nav-menus-wrapper-close-button'>✕</span>"), n(t).find(".nav-search").length > 0 && n(t).find(".nav-search").find("form").prepend("<span class='nav-search-close-button'>✕</span>"), u.init = function () {
                u.settings = n.extend({}, o, s), "right" == u.settings.offCanvasSide && n(t).find(".nav-menus-wrapper").addClass("nav-menus-wrapper-right"), u.settings.hidden && (n(t).addClass("navigation-hidden"), u.settings.mobileBreakpoint = 99999), v(), u.settings.fixed && n(t).addClass("navigation-fixed"), n(t).find(".nav-toggle").on("click touchstart", function (n) {
                    n.stopPropagation(), n.preventDefault(), u.showOffcanvas(), s !== a && u.callback("onShowOffCanvas")
                }), n(t).find(".nav-menus-wrapper-close-button").on("click touchstart", function () {
                    u.hideOffcanvas(), s !== a && u.callback("onHideOffCanvas")
                }), n(t).find(".nav-search-button").on("click touchstart", function (n) {
                    n.stopPropagation(), n.preventDefault(), u.toggleSearch()
                }), n(t).find(".nav-search-close-button").on("click touchstart", function () {
                    u.toggleSearch()
                }), n(t).find(".megamenu-tabs").length > 0 && y(), n(e).resize(function () {
                    m(), C()
                }), m(), s !== a && u.callback("onInit")
            };
            var v = function () {
                n(t).find("li").each(function () {
                    n(this).children(".nav-dropdown,.megamenu-panel").length > 0 && (n(this).children(".nav-dropdown,.megamenu-panel").addClass("nav-submenu"), u.settings.submenuIndicator && n(this).children("a").append("<span class='submenu-indicator'><span class='submenu-indicator-chevron'></span></span>"))
                })
            };
            u.showSubmenu = function (e, i) {
                g() > u.settings.mobileBreakpoint && n(t).find(".nav-search").find("form").slideUp(), "fade" == i ? n(e).children(".nav-submenu").stop(!0, !0).delay(u.settings.showDelayDuration).fadeIn(u.settings.showDuration) : n(e).children(".nav-submenu").stop(!0, !0).delay(u.settings.showDelayDuration).slideDown(u.settings.showDuration), n(e).addClass("nav-submenu-open")
            }, u.hideSubmenu = function (e, i) {
                "fade" == i ? n(e).find(".nav-submenu").stop(!0, !0).delay(u.settings.hideDelayDuration).fadeOut(u.settings.hideDuration) : n(e).find(".nav-submenu").stop(!0, !0).delay(u.settings.hideDelayDuration).slideUp(u.settings.hideDuration), n(e).removeClass("nav-submenu-open").find(".nav-submenu-open").removeClass("nav-submenu-open")
            };
            var h = function () {
                n("body").addClass("no-scroll"), u.settings.overlay && (n(t).append("<div class='nav-overlay-panel'></div>"), n(t).find(".nav-overlay-panel").css("background-color", u.settings.overlayColor).fadeIn(300).on("click touchstart", function (n) {
                    u.hideOffcanvas()
                }))
            }, p = function () {
                n("body").removeClass("no-scroll"), u.settings.overlay && n(t).find(".nav-overlay-panel").fadeOut(400, function () {
                    n(this).remove()
                })
            };
            u.showOffcanvas = function () {
                h(), "left" == u.settings.offCanvasSide ? n(t).find(".nav-menus-wrapper").css("transition-property", "left").addClass("nav-menus-wrapper-open") : n(t).find(".nav-menus-wrapper").css("transition-property", "right").addClass("nav-menus-wrapper-open")
            }, u.hideOffcanvas = function () {
                n(t).find(".nav-menus-wrapper").removeClass("nav-menus-wrapper-open").on("webkitTransitionEnd moztransitionend transitionend oTransitionEnd", function () {
                    n(t).find(".nav-menus-wrapper").css("transition-property", "none").off()
                }), p()
            }, u.toggleOffcanvas = function () {
                g() <= u.settings.mobileBreakpoint && (n(t).find(".nav-menus-wrapper").hasClass("nav-menus-wrapper-open") ? (u.hideOffcanvas(), s !== a && u.callback("onHideOffCanvas")) : (u.showOffcanvas(), s !== a && u.callback("onShowOffCanvas")))
            }, u.toggleSearch = function () {
                "none" == n(t).find(".nav-search").find("form").css("display") ? (n(t).find(".nav-search").find("form").slideDown(), n(t).find(".nav-submenu").fadeOut(200)) : n(t).find(".nav-search").find("form").slideUp()
            };
            var m = function () {
                u.settings.responsive ? (g() <= u.settings.mobileBreakpoint && r > u.settings.mobileBreakpoint && (n(t).addClass("navigation-portrait").removeClass("navigation-landscape"), D()), g() > u.settings.mobileBreakpoint && d <= u.settings.mobileBreakpoint && (n(t).addClass("navigation-landscape").removeClass("navigation-portrait"), k(), p(), u.hideOffcanvas()), r = g(), d = g()) : k()
            }, b = function () {
                n("body").on("click.body touchstart.body", function (e) {
                    0 === n(e.target).closest(".navigation").length && (n(t).find(".nav-submenu").fadeOut(), n(t).find(".nav-submenu-open").removeClass("nav-submenu-open"), n(t).find(".nav-search").find("form").slideUp())
                })
            }, g = function () {
                return e.innerWidth || i.documentElement.clientWidth || i.body.clientWidth
            }, w = function () {
                n(t).find(".nav-menu").find("li, a").off(f).off(l).off(c)
            }, C = function () {
                if (g() > u.settings.mobileBreakpoint) {
                    var e = n(t).outerWidth(!0);
                    n(t).find(".nav-menu").children("li").children(".nav-submenu").each(function () {
                        n(this).parent().position().left + n(this).outerWidth() > e ? n(this).css("right", 0) : n(this).css("right", "auto")
                    })
                }
            }, y = function () {
                function e(e) {
                    var i = n(e).children(".megamenu-tabs-nav").children("li"),
                        a = n(e).children(".megamenu-tabs-pane");
                    n(i).on("click.tabs touchstart.tabs", function (e) {
                        e.stopPropagation(), e.preventDefault(), n(i).removeClass("active"), n(this).addClass("active"), n(a).hide(0).removeClass("active"), n(a[n(this).index()]).show(0).addClass("active")
                    })
                }

                if (n(t).find(".megamenu-tabs").length > 0) for (var i = n(t).find(".megamenu-tabs"), a = 0; a < i.length; a++) e(i[a])
            }, k = function () {
                w(), n(t).find(".nav-submenu").hide(0), navigator.userAgent.match(/Mobi/i) || navigator.maxTouchPoints > 0 || "click" == u.settings.submenuTrigger ? n(t).find(".nav-menu, .nav-dropdown").children("li").children("a").on(f, function (i) {
                    if (u.hideSubmenu(n(this).parent("li").siblings("li"), u.settings.effect), n(this).closest(".nav-menu").siblings(".nav-menu").find(".nav-submenu").fadeOut(u.settings.hideDuration), n(this).siblings(".nav-submenu").length > 0) {
                        if (i.stopPropagation(), i.preventDefault(), "none" == n(this).siblings(".nav-submenu").css("display")) return u.showSubmenu(n(this).parent("li"), u.settings.effect), C(), !1;
                        if (u.hideSubmenu(n(this).parent("li"), u.settings.effect), "_blank" == n(this).attr("target") || "blank" == n(this).attr("target")) e.open(n(this).attr("href")); else {
                            if ("#" == n(this).attr("href") || "" == n(this).attr("href")) return !1;
                            e.location.href = n(this).attr("href")
                        }
                    }
                }) : n(t).find(".nav-menu").find("li").on(l, function () {
                    u.showSubmenu(this, u.settings.effect), C()
                }).on(c, function () {
                    u.hideSubmenu(this, u.settings.effect)
                }), u.settings.hideSubWhenGoOut && b()
            }, D = function () {
                w(), n(t).find(".nav-submenu").hide(0), u.settings.visibleSubmenusOnMobile ? n(t).find(".nav-submenu").show(0) : (n(t).find(".nav-submenu").hide(0), n(t).find(".submenu-indicator").removeClass("submenu-indicator-up"), u.settings.submenuIndicator ? n(t).find(".submenu-indicator").on(f, function (e) {
                    return e.stopPropagation(), e.preventDefault(), u.hideSubmenu(n(this).parent("a").parent("li").siblings("li"), "slide"), u.hideSubmenu(n(this).closest(".nav-menu").siblings(".nav-menu").children("li"), "slide"), "none" == n(this).parent("a").siblings(".nav-submenu").css("display") ? (n(this).addClass("submenu-indicator-up"), n(this).parent("a").parent("li").siblings("li").find(".submenu-indicator").removeClass("submenu-indicator-up"), n(this).closest(".nav-menu").siblings(".nav-menu").find(".submenu-indicator").removeClass("submenu-indicator-up"), u.showSubmenu(n(this).parent("a").parent("li"), "slide"), !1) : (n(this).parent("a").parent("li").find(".submenu-indicator").removeClass("submenu-indicator-up"), void u.hideSubmenu(n(this).parent("a").parent("li"), "slide"))
                }) : k())
            };
            u.callback = function (n) {
                s[n] !== a && s[n].call(t)
            }, u.init()
        }, n.fn.navigation = function (e) {
            return this.each(function () {
                if (a === n(this).data("navigation")) {
                    var i = new n.navigation(this, e);
                    n(this).data("navigation", i)
                }
            })
        }
    }(jQuery, window, document), $(document).ready(function () {
        $("#navigation").navigation()
    });

    // Product Preview
    $('.sp-wrap').smoothproducts();

    // Range Slider Script
    $(".js-range-slider").ionRangeSlider({
        type: "double", min: 0, max: 1000, from: 100, to: 750, grid: true
    });

    // Tooltip
    $('[data-toggle="tooltip"]').tooltip();
    !(function () {
        let is_user,j,
            user_cart = getToken('user_cart') ? JSON.parse(getToken('user_cart')) : {products: []};
        fetch('api/user', {
            method: 'GET',
        })
            .then(r => r.json())
            .then(data => {
                const carts = data['cart'].quantity_total,
                    wish_count = data['wish_list'][0];
                j = data['wish_list']
                document.querySelectorAll('.wish_counter').forEach(wishes => wishes.innerHTML = wish_count);
                document.querySelectorAll('.cart-counter').forEach(cart => cart.innerHTML = carts)
                is_user = true;
            })
            .catch(error => {
                document.querySelectorAll('.wish_or_remove').forEach(wishes => wishes.remove());
                document.querySelectorAll('.cart-counter').forEach(cart => cart.innerHTML = user_cart.products.length);
                is_user = false;
            })
        fetch('api/product', {
            method: 'GET'
        }).then(r => r.json())
            .then(data => {
                let l;
                for (const products in data) {
                    let product = data[products]
                    if (data.hasOwnProperty(products)) {
                        l = `<div class="col-xl-3 col-lg-4 col-md-6 col-6"><div class="product_grid card b-0">`
                        l += '<div class="badge bg-info text-white position-absolute ft-regular ab-left text-upper">' + product.label + '</div>' + '<div class="card-body p-0"><div class="shop_thumb position-relative">';
                        l += '<a class="card-img-top d-block overflow-hidden" href="shop-single-v1.html"><img class="card-img-top" src="/assets/img/product/1.jpg" alt="..."></a>' + '<div class="product-hover-overlay d-flex align-items-center justify-content-between">' + '<div class="edlio"><a href="javascript:void(0);" class="text-underline fs-sm ft-bold snackbar-addcart" id="cart-' + product.id + '"><i class="bx bx-cart" style="font-size: 1.5rem"></i></a></div>' + '<div class="edlio d-flex align-items-center">'
                        l += is_user ? '<button class="btn auto btn_love mr-2 snackbar-wishlist" id="wish-' + product.id + '"><i class="bx bx-heart"></i></button>' : '';
                        l += '<a href="#" class="text-underline" id="modal-' + product.id + '" data-toggle="modal" data-target="#quickview"><i class="bx bx-expand"></i></a>' + '</div>' + '</div>' + '</div>' + '</div>' + '<div class="card-footer b-0 p-0 pt-2 bg-white d-flex align-items-start justify-content-between">' + '<div class="text-left">' + '<div class="text-left">' + '<div class="star-rating align-items-center d-flex justify-content-left mb-1 p-0">' + '<i class="bx bxs-star filled"></i>' + '<i class="bx bxs-star filled"></i>' + '<i class="bx bxs-star filled"></i><i class="bx bxs-star filled"></i><i class="bx bx-star"></i>' + '<span class="small">(5 Reviews)</span>' + '</div><h5 class="fs-md mb-0 lh-1 mb-1"><a href="shop-single-v1.html">' + product.name + '</a></h5>' + '<div class="elis_rty"><span class="ft-bold text-dark fs-sm">$' + product.price + '</span></div>' + '</div></div></div></div></div>'
                    }
                    document.getElementById('products').insertAdjacentHTML('beforeend', l)
                    document.getElementById(`modal-${product.id}`).addEventListener('click', () => {
                        for (let image in product.images) {
                            document.querySelector('.quick_view_slide').insertAdjacentHTML('beforeend', `<div class="single_view_slide"><img src="/assets/img/product/1.jpg" class="img-fluid" alt="" /></div>`)
                        }
                    });
                    document.getElementById(`cart-${product.id}`).addEventListener('click', () => {
                        if (is_user) {
                            fetch('/api/cart', {
                                method: 'POST', headers: {
                                    'X-CSRFToken': getToken("csrftoken"),
                                    "Accept": "application/json",
                                    'Content-Type': 'application/json'
                                }, body: JSON.stringify({
                                    'id': product.id
                                })
                            })
                                .then(res => res.json())
                                .then(carts => {
                                    document.querySelectorAll('.cart-counter').forEach(counter => counter.innerHTML = carts['count'])
                                    cart_snackbar(carts['update'], product.name)
                                })
                        } else {
                            if (user_cart.products.includes(product.name)) {
                                user_cart.products.splice(user_cart.products.indexOf(product.name), 1)
                                cart_snackbar('removed', product.name)
                            } else {
                                user_cart.products.push(product.name)
                                cart_snackbar('added', product.name)
                            }
                            document.cookie = 'user_cart=' + JSON.stringify(user_cart);
                            document.querySelectorAll('.cart-counter').forEach(counter => counter.innerHTML = user_cart.products.length)
                        }

                    })
                    let favourite = document.getElementById(`wish-${product.id}`);
                    favourite && favourite.addEventListener('click', () => {
                        fetch('api/user', {
                            method: 'POST', headers: {
                                'X-CSRFToken': getToken("csrftoken"),
                                "Accept": 'application/json',
                                "Content-Type": 'application/json',
                            }, body: JSON.stringify({
                                id: product.id
                            })
                        }).then(r => r.json())
                            .then(data => {
                                let wish_count = data['wish_list'][0],
                                    liked = favourite.getAttribute('liked');
                                document.querySelectorAll('.wish_counter').forEach(wishes => wishes.innerHTML = wish_count);
                                if (liked) {
                                    favourite.removeAttribute('liked')
                                    favourite.childNodes.forEach(likes => likes.remove())
                                    favourite.insertAdjacentHTML('beforeend', '<i class="bx bx-heart"></i>')
                                    wish_snackbar('removed', product.name)
                                } else {
                                    favourite.setAttribute('liked', 'true')
                                    favourite.childNodes.forEach(likes => likes.remove())
                                    favourite.insertAdjacentHTML('beforeend', '<i class="bx bxs-heart"></i>')
                                    wish_snackbar('added', product.name)
                                }
                            })
                    })
                }
            })
        if (is_user){
                for (const i in j['wish_list'][1]) {
                    if (j['wish_list'].hasOwnProperty(i)) {
                        let favourites = document.getElementById(`wish-${j['wish_list'][1][i]}`)
                        if (favourites) {
                            favourites.setAttribute('liked', 'true')
                            favourites.childNodes.forEach(likes => likes.remove())
                            favourites.insertAdjacentHTML('beforeend', '<i class="bx bxs-heart"></i>')
                        }
                    }
                }
        }
    })()

    // Snackbar for Add To Cart Product
    function cart_snackbar(type, product) {
        let text = `${product} was ${type} to cart successfully!`
        Snackbar.show({
            text: text,
            pos: 'top-right',
            showAction: false,
            actionText: "Dismiss",
            duration: 3000,
            textColor: '#fff',
            backgroundColor: '#15151+5'
        });
    }


    // Snackbar for wishlist Product
    function wish_snackbar(type, product) {
        let text = `${product} was ${type} to wishlist successfully!`

        Snackbar.show({
            text: text,
            pos: 'top-right',
            showAction: false,
            actionText: "Dismiss",
            duration: 3000,
            textColor: '#fff',
            backgroundColor: '#151515'
        });
    }

    // Bottom To Top Scroll Script
    $(window).on('scroll', function () {
        var height = $(window).scrollTop();
        if (height > 100) {
            $('#back2Top').fadeIn();
        } else {
            $('#back2Top').fadeOut();
        }
    });


    // Script For Fix Header on Scroll
    $(window).on('scroll', function () {
        var scroll = $(window).scrollTop();

        if (scroll >= 50) {
            $(".header").addClass("header-fixed");
        } else {
            $(".header").removeClass("header-fixed");
        }
    });

    // Brand-slide
    $('.smart-brand').slick({
        slidesToShow: 6, arrows: false, dots: false, infinite: true, autoplaySpeed: 2000, autoplay: true, responsive: [{
            breakpoint: 1024, settings: {
                arrows: false, dots: false, slidesToShow: 4
            }
        }, {
            breakpoint: 600, settings: {
                arrows: false, dots: false, slidesToShow: 3
            }
        }]
    });

    // reviews-slide
    $('.reviews-slide').slick({
        slidesToShow: 1, arrows: true, dots: false, infinite: true, autoplaySpeed: 2000, autoplay: true, responsive: [{
            breakpoint: 1024, settings: {
                arrows: true, dots: false, slidesToShow: 1
            }
        }, {
            breakpoint: 600, settings: {
                arrows: true, dots: false, slidesToShow: 1
            }
        }]
    });

    // quick_view_slide
    $('.quick_view_slide').slick({
        slidesToShow: 1, arrows: true, dots: true, infinite: true, autoplaySpeed: 2000, autoplay: true, responsive: [{
            breakpoint: 1024, settings: {
                arrows: true, dots: true, slidesToShow: 1
            }
        }, {
            breakpoint: 600, settings: {
                arrows: true, dots: true, slidesToShow: 1
            }
        }]
    });

    // item Slide
    $('.slide_items').slick({
        slidesToShow: 4,
        arrows: true,
        dots: false,
        infinite: true,
        speed: 500,
        cssEase: 'linear',
        autoplaySpeed: 2000,
        autoplay: true,
        responsive: [{
            breakpoint: 1024, settings: {
                arrows: true, dots: false, slidesToShow: 3
            }
        }, {
            breakpoint: 600, settings: {
                arrows: true, dots: false, slidesToShow: 1
            }
        }]
    });

    // Home Slider
    $('.home-slider').slick({
        centerMode: false, slidesToShow: 1, arrows: true, dots: true, responsive: [{
            breakpoint: 768, settings: {
                arrows: true, slidesToShow: 1
            }
        }, {
            breakpoint: 480, settings: {
                arrows: true, slidesToShow: 1
            }
        }]
    });

    // fullwidth home slider
    function inlineCSS() {
        $(".home-slider .item").each(function () {
            var attrImageBG = $(this).attr('data-background-image');
            var attrColorBG = $(this).attr('data-background-color');
            if (attrImageBG !== undefined) {
                $(this).css('background-image', 'url(' + attrImageBG + ')');
            }
            if (attrColorBG !== undefined) {
                $(this).css('background', '' + attrColorBG + '');
            }
        });
    }

    inlineCSS();

});


function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}