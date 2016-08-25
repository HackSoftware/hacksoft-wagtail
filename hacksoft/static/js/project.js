/* Project specific Javascript goes here. */

// here is the header picture, we have uploaded from django-cms

var url = window.location.href, idx = url.indexOf("#")
var hash = idx != -1 ? url.substring(idx + 1) : "";
if (hash == "success") {
  $('.popup-overlay').fadeIn();
  $('.success-popup').fadeIn();
}


fixed_header = $('.header');

$(window).on("scroll", function (e) {
  if ($(document).scrollTop() > 0) {
    fixed_header.addClass("scrolled-header");
  } else {
    fixed_header.removeClass("scrolled-header");
  }

});

$('.homepage-header').find('.scroll-down-landpage img').click(function () {
  var header = $('.homepage-header').height();
  $('html, body').animate({
    scrollTop: header
  }, 900);
});

$('.static-header').find('.scroll-down-arrow img').click(function () {
  var header = $('.static-header').height();
  $('html, body').animate({
    scrollTop: header
  }, 900);
});

$('.book-a-meeting-button').click(function () {
  $('#popup1').fadeIn();
});

$('.close').click(function () {
  $('#popup1').fadeOut();
  $('#success').fadeOut();
});

$(document).keydown(function (e) {
  //ESC button pressed
  if (e.keyCode == 27) {
    console.log('lil');
    $('#popup1').fadeOut();
    $('#success').fadeOut();
  }
});
