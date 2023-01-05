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
    var button = $(event.relatedTarget); // Button that triggered the modal
    var form = button.data("form"); // Extract form from data-form attribute
    var url = button.data("url")
    var formTitle = button.data("title"); // Extract form title from data-title attribute
    // Show the selected form
    var modal = $(this);
    modal.find(".modal-title").text("School Info: " + formTitle); // Display the form title
    $.ajax({
      type: 'GET',
      url: url,
      data: {
      	'form_name': form
      },
      success: (data)=>{
        console.log(data)
      	$('#formContainer').html(data)
    	}
    });
    // modal.find("#schoolInfoForm .form-group").addClass("d-none");
    // modal.find(`#${form}`).removeClass("d-none");
  });

	// $("#openPostModal").on("hide.bs.modal", function () {
	// 	$(this).find(".form-group").addClass("d-none");
	// });



});
