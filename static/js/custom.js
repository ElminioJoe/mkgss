/*---------------------------------------------------------------------
    File Name: custom.js
---------------------------------------------------------------------*/

$(function () {
  ("use strict");

  /* Preloader
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  setTimeout(function () {
    $(".loader_bg").fadeToggle();
  }, 1500);

  /* JQuery Menu
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
    /* OwlCarousel - Blog Post slider
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  var owl = $(".carousel-slider-post");
  owl.owlCarousel({
    items: 1,
    loop: true,
    margin: 10,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
  });

  /* OwlCarousel - Banner Rotator Slider
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  var owl = $(".banner-rotator-slider");
  owl.owlCarousel({
    items: 1,
    loop: true,
    margin: 10,
    nav: true,
    dots: false,
    navText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>",
    ],
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
  });

  /* OwlCarousel - Product Slider
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  var owl = $("#product-in-slider");
  owl.owlCarousel({
    loop: true,
    nav: true,
    margin: 10,
    navText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>",
    ],
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 2,
      },
      960: {
        items: 3,
      },
      1200: {
        items: 4,
      },
    },
  });
  owl.on("mousewheel", ".owl-stage", function (e) {
    if (e.deltaY > 0) {
      owl.trigger("next.owl");
    } else {
      owl.trigger("prev.owl");
    }
    e.preventDefault();
  });

  /* Scroll to Top
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  $(window).on("scroll", function () {
    scroll = $(window).scrollTop();
    if (scroll >= 100) {
      $("#back-to-top").addClass("b-show_scrollBut");
    } else {
      $("#back-to-top").removeClass("b-show_scrollBut");
    }
  });
  $("#back-to-top").on("click", function () {
    $("body,html").animate(
      {
        scrollTop: 0,
      },
      1000,
    );
  });

  /* Fancybox
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  // Fancybox.bind('[data-fancybox="gallery"]', {
  //   caption: function (_fancybox, carousel, slide) {
  //     return (
  //       `${slide.index + 1} / ${carousel.slides.length} <br />` + slide.caption
  //     );
  //   },
  // });

  /* Toggle sidebar
  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  // Javascript to enable link to tab
  var hash = document.location.hash;
  var prefix = "tab_";
  if (hash) {
    $('#list-tab a[href="' + hash.replace(prefix, "") + '"]').tab("show");
  }

  // Change hash for page-reload
  $("#list-tab a").on("shown.bs.tab", function (e) {
    window.location.hash = e.target.hash.replace("#", "#" + prefix);
  });

  /* Product slider
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
  // optional
  $("#blogCarousel").carousel({
    interval: 5000,
  });

  /* Magnific Popup
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */

  var popup_btn = $('.gallery');

  popup_btn.magnificPopup({
    delegate: "a",
    type: "image",
    tLoading: "Loading image #%curr%...",
    closeOnContentClick: false,
    closeBtnInside: false,
    mainClass: "mfp-with-zoom mfp-img-mobile",
    gallery: {
      enabled: true,
      preload: [0, 3],
      navigateByImgClick: true,
      arrowMarkup:
        '<button title="%title%" type="button" class="mfp-arrow mfp-arrow-%dir%"></button>', // markup of an arrow button

      tPrev: "Previous",
      tNext: "Next",
      tCounter: '<span class="mfp-counter">%curr% of %total%</span>',
    },
    image: {
      verticalFit: true,
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
    },
    // zoom: {
    //   enabled: true,
    //   duration: 300, // don't forget to change the duration also in CSS
    //   easing: 'ease-in-out',
    //   opener: function(element) {
    //     return element.find('img');
    //   }
    // }
  });
  
});