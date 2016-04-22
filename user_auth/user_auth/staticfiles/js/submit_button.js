jQuery(document).ready(function ($) {
    $( "#send").on('mouseover', function () {
	    if($( "#send").val() !== "Volunteer"){
	    	$( "#send").val("Already Volunteered");
	    } else {
	    	$( "#send").val("Volunteer");
	    }
		console.log($( "#send").text());
	
  });
});