$(function () {

  $(".flag").on("click", function (e) {
    $(this).attr({class: "flag flag-selected"});
    $(".flag").not(this).attr({class: "flag flag-not-selected"});
  });

});
