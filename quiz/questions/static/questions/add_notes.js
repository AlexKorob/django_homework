$(function() {
  $(".note").click(function() {
    let val = $(this).text();
    $("<p>").attr({
      style: "text-align: center; border-radius: 10px; border: 2px solid black;" +
              "margin-bottom: 10px; padding: 15px; font-size: 20px;"
    }).text(val).appendTo($("#added_notes"));

    $("<br>").appendTo($("#added_notes"));

    $(this).remove();
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });

    $.ajax({
			type: "POST",
			url: window.location.pathname,
			data: {"note": val, "csrftoken": Cookies.get('csrftoken')},
			cache: false,
			success: function(){}
		});
  });
});
