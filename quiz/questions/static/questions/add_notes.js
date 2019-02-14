$(function() {

  // create note
  $(".note").click(function() {
    let val = $(this).text();
    $("<p>").attr({
      class: "del-note",
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

  // delete note
  $(".del-note").click(function() {
    let val = $(this).text();
    $("<p>").attr({class: "note btn btn-primary",
                  style: "margin-bottom: 20px; padding: 15px; display: block;" +
                  "cursor: pointer; font-size: 20px;"
    }).text(val).appendTo($("#not_added_notes"));

    $("<br>").appendTo($("#not_added_notes"));

    $(this).remove();
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();

    url = window.location.pathname
    url_arr = url.split("/")
    id = url_arr[url_arr.length - 1]
    prefix = url_arr[2]
    url = "/tests/" + prefix + /delete_notes/ + id

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });
    alert(url)
    $.ajax({
			type: "POST",
			url: url,
			data: {"note": val, "csrftoken": Cookies.get('csrftoken')},
			cache: false,
			success: function(){}
		});
  });
});
