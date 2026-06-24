(function ($) {
	"use strict";

	/*------------------------------------
			Preloader
		--------------------------------------*/

	$(window).on('load', function () {
		// $('#preloader').delay(350).fadeOut('slow');
		// $('body').delay(350).css({ 'overflow': 'visible' });
		// -------------------- Site Preloader
		$('#ctn-preloader').fadeOut(); // will first fade out the loading animation
		$('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
		$('body').delay(350).css({ 'overflow': 'visible' });
	});


	// ---------------- Data CSS Js
	$("[data-background").each(function () {
		$(this).css("background-image", "url( " + $(this).attr("data-background") + "  )");
	});

	$("[data-width]").each(function () {
		$(this).css("width", $(this).attr("data-width"));
	});

	$("[data-bg-color]").each(function () {
		$(this).css("background-color", $(this).attr("data-bg-color"));
	});


	/*------------------------------------
		Mobile Menu
	--------------------------------------*/

	$('#mobile-menu').meanmenu({
		meanMenuContainer: '.mobile-menu',
		meanScreenWidth: "991",
		meanExpand: '+',
		meanShowChildren: true,
		meanExpandableChildren: true,
		meanContract: "-",
		meanDisplay: "block"
	});

	$('#mobile-menu2').meanmenu({
		meanMenuContainer: '.mobile-menu2',
		meanScreenWidth: "1920",
		meanExpand: '+',
		meanShowChildren: true,
		meanExpandableChildren: true,
		meanContract: "-",
		meanDisplay: "block"
	});

	$('#mobile-menu-active').metisMenu();

	$('#mobile-menu-active .has-dropdown > a').on('click', function (e) {
		e.preventDefault();
	});

	$(".hamburger-menu > a").on("click", function (e) {
		e.preventDefault();
		$(".slide-bar").toggleClass("show");
		$("body").addClass("on-side");
		$('.body-overlay').addClass('active');
		$(this).addClass('active');
	});

	$(".close-mobile-menu > a").on("click", function (e) {
		e.preventDefault();
		$(".slide-bar").removeClass("show");
		$("body").removeClass("on-side");
		$('.body-overlay').removeClass('active');
		$('.hamburger-menu > a').removeClass('active');
	});

	$('.body-overlay').on('click', function () {
		$(this).removeClass('active');
		$(".slide-bar").removeClass("show");
		$("body").removeClass("on-side");
		$('.hamburger-menu > a').removeClass('active');
	});



	//sticky-menu
	$(window).on('scroll', function () {
		var scroll = $(window).scrollTop();
		if (scroll < 200) {
			$(".main-header-area").removeClass("sticky-menu");
		} else {
			$(".main-header-area").addClass("sticky-menu");
		}
	});

	// Add .active class to current navigation based on URL
	var pgurl = window.location.href.substr(window.location.href.lastIndexOf("/") + 1);
	$(".menu-list > li  a").each(function () {
		if ($(this).attr("href") == pgurl || $(this).attr("href") == '')
			$(this).addClass("active");
		// $(this).parent("li").addClass("active");
	})


	//shopping-cart-bar
	$(".shopping-cart").on("click", function () {
		$(".cart-menu-right").addClass('cart-info');
	});
	$(".close-icon").click(function () {
		$(".cart-menu-right").removeClass('cart-info');

	});

	//gear-box
	$(".gear-icon").on("click", function () {
		$(".gear-box").addClass('open-gear');
	});

	$(".close-icon").click(function () {
		$(".gear-box").removeClass('open-gear');

	});


	//brand-slide-active
	$('.brand-slide-active').slick({
		slidesToShow: 3,
		slidesToScroll: 1,
		arrows: false,
		infinite: true,
		autoplay: true,
		autoplaySpeed: 1500,
		centerMode: false,
		loop: true,
		// cssEase: 'linear',
		responsive: [
			{
				breakpoint: 425,
				settings: {
					slidesToShow: 1,
					centerMode: false,
				}
			},
			{
				breakpoint: 767,
				settings: {
					slidesToShow: 1,
					centerMode: false,
				}
			},
			{
				breakpoint: 991,
				settings: {
					slidesToShow: 1,
					centerMode: false,
				}
			},
			{
				breakpoint: 1200,
				settings: {
					slidesToShow: 2,
					centerMode: false,
				}
			},
			{
				breakpoint: 1500,
				settings: {
					slidesToShow: 3,
					centerMode: false,
				}
			},

		]
	});


	//feedback-active
	$('.feedback-active').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		arrows: true,
		dots: true,
		nextArrow: $('.next_t1'),
		prevArrow: $('.prev_t1'),
		infinite: true,
		autoplay: true,
		loop: true,
		responsive: [
			{
				breakpoint: 425,
				settings: {
					slidesToShow: 1,
					centerMode: false,
				}
			},
			{
				breakpoint: 991,
				settings: {
					slidesToShow: 1,
					centerMode: false,
				}
			},

			{
				breakpoint: 992,
				settings: {
					slidesToShow: 3,
					centerMode: false,
				}
			},
		]
	});


	//feedback-active
	$('.cta-active').slick({
		slidesToShow: 3,
		slidesToScroll: 1,
		arrows: false,
		dots: false,
		nextArrow: $('.next_t1'),
		prevArrow: $('.prev_t1'),
		infinite: true,
		autoplay: true,
		loop: true,
		responsive: [
			{
				breakpoint: 1199,
				settings: {
					arrows: false,
					slidesToShow: 1,
				}
			},
		]
	});




	$(function () {
		$('.chart').easyPieChart({
			animate: {
				duration: 1000,
				enabled: true
			},
			scaleLength: 0,
			size: 190,
			trackColor: 'rgba(24, 24,24, 0.1)',
			barColor: '#FF8A00',
			scaleColor: 'false',
			lineWidth: 10,
			trackWidth: 1,
			lineCap: 'round',
			rotate: 90,
		});
	});




	// -------------------- Remove Placeholder When Focus Or Click
	$("input,textarea").each(function () {
		$(this).data('holder', $(this).attr('placeholder'));
		$(this).on('focusin', function () {
			$(this).attr('placeholder', '');
		});
		$(this).on('focusout', function () {
			$(this).attr('placeholder', $(this).data('holder'));
		});
	});


	/* magnificPopup video view */
	$('.popup-video').magnificPopup({
		type: 'iframe'
	});



	var scrollToTopBtn = $('#scrollToTopBtn');

	$(window).scroll(function () {
		if ($(window).scrollTop() > 300) {
			scrollToTopBtn.addClass('show');
		} else {
			scrollToTopBtn.removeClass('show');
		}
	});

	scrollToTopBtn.on('click', function (e) {
		e.preventDefault();
		$('html, body').animate({ scrollTop: 0 }, '300');
	});



	$('.counter').counterUp({
		delay: 10,
		time: 2000
	});

	$('select').niceSelect();

	AOS.init();



	const links = document.querySelectorAll(".left-menu ul a");

	for (let linkes of links) {
		linkes.addEventListener("click", clickHandler);
	};

	function clickHandler(e) {
		e.preventDefault();
		const href = this.getAttribute("href");
		const offsetTop = document.querySelector(href).offsetTop;

		scroll({
			top: offsetTop,
			behavior: "smooth"
		});
	}

	const lenis = new Lenis()

	lenis.on('scroll', () => {

	})

	function raf(time) {
		lenis.raf(time)
		requestAnimationFrame(raf)
	}

	requestAnimationFrame(raf)




	let paralaxThumb = document.getElementsByClassName('paralaxThumb1');
	new simpleParallax(paralaxThumb, {
		orientation: 'right',
		overflow: true,
		delay: 5
	});

	let paralaxThumbs2 = document.getElementsByClassName('paralaxThumb2');
	new simpleParallax(paralaxThumbs2, {
		orientation: 'left',
		overflow: true,
		delay: 5
	});


	$("#checkbox").click(function () {
		$("body").toggleClass("dark-theme");
	});



})(jQuery);