$(function () {
  "use strict";
  // navbar hover function
  $("nav .dropdown").hover(
    function () {
      var $this = $(this);
      $this.addClass("show");
      $this.find("> a").attr("aria-expanded", true);
      $this.find(".dropdown-menu").addClass("show");
    },
    function () {
      var $this = $(this);
      $this.removeClass("show");
      $this.find("> a").attr("aria-expanded", false);
      $this.find(".dropdown-menu").removeClass("show");
    },
  );

  // destroy messages div after 2 seconds
  setTimeout(function () {
    if ($("#message").length > 0) {
      $("#message").remove();
    }
  }, 5000);

  // form DOM Manipulation

  // Bind a click event handler to the body element using event delegation
  $("#openPostModal").on("show.bs.modal", function (event) {
    // Button that triggered the modal
    var button = $(event.relatedTarget);
    // Extract form, url & title from data- attribute
    var form = button.data("form");
    var url = button.data("url")
    var formTitle = button.data("title");
    // Show the selected form
    var modal = $(this);
    modal.find(".modal-title").text("School Info: " + formTitle); // Display the form title
    modal.find("fieldset.aligned").addClass("d-none");
    modal.find(`#${form}`).removeClass("d-none");
    $(`#${form}`).load(url, function(){
      $("form.myForm").attr("action", url);
    });
  });

	$("#openPostModal").on("hide.bs.modal", function () {
		$(this).find("fieldset.aligned").addClass("d-none");
	});



});
