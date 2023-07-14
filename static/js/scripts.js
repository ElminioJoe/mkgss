$(function () {
	("use strict");
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

	// destroy messages div after 5 seconds
	setTimeout(function () {
		if ($("#message").length > 0) {
			$(".messages").empty();
		}
	}, 5000);

	// form DOM Manipulation

	// Bind a click event handler to the body element using event delegation
	$("#openPostModal").on("show.bs.modal", function (event) {
		// Button that triggered the modal
		var button = $(event.relatedTarget);
		// Extract form, url & title from data- attribute
		var form = button.data("form");
		var url = button.data("url");
		var formTitle = button.data("title");
		// Show the selected form
		var modal = $(this);
		modal.find(".modal-title").text("School Info: " + formTitle); // Display the form title
		modal.find("fieldset.aligned").addClass("d-none");
		modal.find(`#${form}`).removeClass("d-none");
		$(`#${form}`).load(url, function () {
			$("form.myForm").attr("action", url);
		});
	});

	$("#openPostModal").on("hide.bs.modal", function () {
		$(this).find("fieldset.aligned").addClass("d-none");
	});

	$("#deleteModal").on("show.bs.modal", function (event) {
		// Button that triggered the modal
		var button = $(event.relatedTarget);
		// Extract form, url & title from data- attribute
		var form = button.data("form");
		var url = button.data("url");
		var formTitle = button.data("title");
		// Show the selected form
		var modal = $(this);
		// Display the form title
		modal.find(".modal-title").text("School Info: " + formTitle);
		$(`#${form}`).load(url, function () {
			$("form.myForm").attr("action", url);
		});
	});

	// Toggle between View and Delete modes
	var toggleSwitch = $("#toggleSwitch");
	var galleryBoxes = $(".gallery-box");
	var selectAllCheckbox = $("#select-all-checkbox");

	$(".gallery-actions").hide();
	// Add an event listener to the toggle switch
	toggleSwitch.on("change", function () {
		if (toggleSwitch.prop("checked")) {
			// Delete mode is active
			// Replace anchor tags with buttons and bind click event to check the corresponding checkbox

			// Loop through each gallery box
			galleryBoxes.each(function () {
				var galleryBox = $(this);
				// Get the anchor tag and its href
				var anchorTag = galleryBox.find("a");
				var img = galleryBox.find("img");
				var href = anchorTag.attr("href");
				var elemClass = anchorTag.attr("class");

				// Replace anchor tag with button
				var button = $("<button>")
					.attr({
						type: "button",
						class: elemClass,
					})
					.html(anchorTag.html());
				anchorTag.replaceWith(button);

				// Set the href on the button
				button.data("href", href);

				// Bind click event to button
				button.on("click", function () {
					var deleteCheckbox = galleryBox.find(
						'.checkbox-container input[type="checkbox"]',
					);
					var isChecked = !deleteCheckbox.prop("checked");
					deleteCheckbox.prop("checked", isChecked).trigger("change");
				});

				// Bind click event to img
				img.on("click", function () {
					var deleteCheckbox = galleryBox.find(
						'.checkbox-container input[type="checkbox"]',
					);
					var isChecked = !deleteCheckbox.prop("checked");
					deleteCheckbox.prop("checked", isChecked).trigger("change");
				});

				// Show the delete checkbox
				var deleteCheckbox = galleryBox.find(".checkbox-container");
				deleteCheckbox.removeClass("d-none");
				$(".gallery-actions").slideDown();
			});
		} else {
			// View mode is active
			// Replace buttons with anchor tags and hide the delete checkbox
			// Loop through each gallery box
			galleryBoxes.each(function () {
				var galleryBox = $(this);

				// Get the button and its href
				var button = galleryBox.find("button");
				var href = button.data("href");
				var elemClass = button.attr("class");

				// Replace button with anchor tag
				var anchorTag = $("<a>")
					.attr({
						href: href,
						class: elemClass,
					})
					.html(button.html());
				button.replaceWith(anchorTag);

				// Hide the delete checkbox
				var deleteCheckbox = galleryBox.find(".checkbox-container ");
				deleteCheckbox.addClass("d-none");
			});

			$(".gallery-actions").slideUp();
			// Reset the selected items to unchecked
			$('.checkbox-container input[type="checkbox"]').prop("checked", false);
			selectAllCheckbox.prop("checked", false);
		}
	});

	var selectedCheckboxes = $(".selected-checkbox");
	var deleteSelectedButton = $("#delete-selected-button");

	deleteSelectedButton.prop("disabled", true);

	// Add an event listener to the delete selected button
	deleteSelectedButton.on("click", function () {
		// Build an array of selected image IDs
		var selectedImageIds = [];
		selectedCheckboxes.each(function () {
			if ($(this).prop("checked")) {
				selectedImageIds.push($(this).val());
			}
		});

		// Check if any checkbox is selected
		if (selectedImageIds.length === 0) {
			// No checkbox selected, do not submit the form
			return;
		}

		// Set the action and selected images in the form inputs
		$("#action-input").val("delete_selected_images");
		$("#selected-images-input").val(JSON.stringify(selectedImageIds));

		// Submit the form
		$("#myForm").submit();
	});

	// Add an event listener to the select all checkbox
	selectAllCheckbox.on("change", function () {
		selectedCheckboxes.prop("checked", selectAllCheckbox.prop("checked"));
		deleteSelectedButton.prop(
			"disabled",
			selectedCheckboxes.filter(":checked").length === 0,
		);
	});

	// Add an event listener to the individual selectedCheckboxes
	selectedCheckboxes.on("change", function () {
		// If any checkbox is unchecked, uncheck the select all checkbox
		if (!$(this).prop("checked")) {
			selectAllCheckbox.prop("checked", false);
		} else {
			selectAllCheckbox.prop(
				"checked",
				selectedCheckboxes.filter(":checked").length ===
					selectedCheckboxes.length,
			);
		}

		// Enable/disable delete button based on checkbox selection
		deleteSelectedButton.prop(
			"disabled",
			selectedCheckboxes.filter(":checked").length === 0,
		);
	});

	// convert newline('/n') to <br>
	/*
  $(".para-br").each(function() {
    let text = $(this).text();
    text = text.replace(/\n/g, "<br><br>");
    $(this).html(text);
  });
*/
});
