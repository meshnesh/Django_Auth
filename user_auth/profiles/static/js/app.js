$(function() {
	$( ".signup-panel" ).draggable();
});

$(document).foundation();
// initialize is-active and is-visible states on "first" tab and slides.
$("[class^=slide]").find("li").eq(0).addClass("is-active");
$("[class$=content]").find("[class$=pane]").eq(0).addClass("slide--content__pane--is-visible");

// click functions for tabs and slides
$("[class^=slide]").on("click", "li", function () {
    var $this = $(this)
        , listIndex = $this.index(); // gets the index of the clicked list item

    // add active class to currently "clicked" list item
    $this.closest("ul").find("li").removeClass("is-active"); // remove class from previously clicked li's
    $this.addClass("is-active"); // add to newly clicked li

    // display associated pane and associate the pane of the same index with the list item being clicked
    var paneIndex = $(".slide--content__pane:eq(" + listIndex + ")");
    $(".slide--content").children().removeClass("slide--content__pane--is-visible");
    paneIndex.addClass("slide--content__pane--is-visible");
});

$(document).ready(function(){
	var $Menu = $('.Img');
	$('.Img').mouseenter(function() {
        $('.PopUp').css('opacity', '1');
		$('.PopUp').css('margin-top', '20px');
    });
		$('.Img').mouseleave(function() {
        $('.PopUp').css('opacity', '0');
		$('.PopUp').css('margin-top', '0px');
    });
	$('.Img').on('click', function() {
		if($Menu.hasClass('Img')){
				$('.Img').addClass('click');
		$('.Img').removeClass('Img');
				$('.Profile').addClass('clickProfile');
				$('.Profile').removeClass('Profile');
				$('.clickPopUp').css('display', 'block');
				$('.PopUp').css('display', 'none');
		}else{
		$('.click').addClass('Img');
		$('.click').removeClass('click');
				$('.clickProfile').addClass('Profile');
				$('.clickProfile').removeClass('clickProfile');
								$('.clickPopUp').css('display', 'none');
				$('.PopUp').css('display', 'block');
			}
		});
	});
	
// navigation 
$(document).foundation();
$(document).ready(function () {
    $('.button').on('click', function () {
        $('.content').toggleClass('isOpen');
    });
});

//SIGN-UP SECTION

var LoginModalController = {
    tabsElementName: ".logmod__tabs li"
    , tabElementName: ".logmod__tab"
    , inputElementsName: ".logmod__form .input"
    , hidePasswordName: ".hide-password",

    inputElements: null
    , tabsElement: null
    , tabElement: null
    , hidePassword: null,

    activeTab: null
    , tabSelection: 0, // 0 - first, 1 - second

    findElements: function () {
        var base = this;

        base.tabsElement = $(base.tabsElementName);
        base.tabElement = $(base.tabElementName);
        base.inputElements = $(base.inputElementsName);
        base.hidePassword = $(base.hidePasswordName);

        return base;
    },

    setState: function (state) {
        var base = this
            , elem = null;

        if (!state) {
            state = 0;
        }

        if (base.tabsElement) {
            elem = $(base.tabsElement[state]);
            elem.addClass("current");
            $("." + elem.attr("data-tabtar")).addClass("show");
        }

        return base;
    },

    getActiveTab: function () {
        var base = this;

        base.tabsElement.each(function (i, el) {
            if ($(el).hasClass("current")) {
                base.activeTab = $(el);
            }
        });

        return base;
    },

    addClickEvents: function () {
        var base = this;

        base.hidePassword.on("click", function (e) {
            var $this = $(this)
                , $pwInput = $this.prev("input");

            if ($pwInput.attr("type") == "password") {
                $pwInput.attr("type", "text");
                $this.text("Hide");
            } else {
                $pwInput.attr("type", "password");
                $this.text("Show");
            }
        });

        base.tabsElement.on("click", function (e) {
            var targetTab = $(this).attr("data-tabtar");

            e.preventDefault();
            base.activeTab.removeClass("current");
            base.activeTab = $(this);
            base.activeTab.addClass("current");

            base.tabElement.each(function (i, el) {
                el = $(el);
                el.removeClass("show");
                if (el.hasClass(targetTab)) {
                    el.addClass("show");
                }
            });
        });

        base.inputElements.find("label").on("click", function (e) {
            var $this = $(this)
                , $input = $this.next("input");

            $input.focus();
        });

        return base;
    },

    initialize: function () {
        var base = this;

        base.findElements().setState().getActiveTab().addClickEvents();
    }
};

$(document).ready(function () {
    LoginModalController.initialize();
});


//END OF SIGN-UP SECTION