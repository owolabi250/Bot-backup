window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
});

$(document).ready(function() {
    $('.set-alarm').click(function() {
        if ($("#datatablesSimple tbody tr").find("input[name='row-radio']").length > 0) {
            return;
        }

        $("#datatablesSimple tbody tr").each(function() {
            var currentDate = new Date().toISOString().slice(0,10);
            var dateValue = $(this).closest("tr").find("td:nth-child(3)").text();
	    if (new Date(Date.parse(dateValue)) >= new Date(currentDate) || new Date(Date.parse(dateValue)).toLocaleDateString() === new Date().toLocaleDateString()){
                var radioButton = $("<input type='radio' name='row-radio' class='radio-button'>");
                $(this).closest("tr").find("td:first-child").prepend(radioButton);
            }
        });

        $("input[name='row-radio']").click(function() {
            $('.datatable-bottom').append("<td><button class='send-btn'>Set Reminder</button></td>");
            var dateValue = $(this).closest("tr").find("td:nth-child(3)").text();
            var timeValue = $(this).closest("tr").find("td:nth-child(8)").text();
            var topicValue = $(this).closest("tr").find("td:nth-child(5)").text();
            var dateObj = new Date(dateValue + " " + timeValue);
            var reminderDateObj;
            var now;
            $(document).on("click", ".send-btn", function() {
                reminderDateObj = dateObj;
                now = new Date();
                var secondsUntilReminder = Math.floor((reminderDateObj.getTime() - now.getTime()) / 1000);
                if (reminderDateObj >= now){

                    console.log("Reminder set for " + secondsUntilReminder + " seconds from now.");
                    setInterval(function() {
                        const dateObj = new Date(Date.now() + secondsUntilReminder * 1000);
                        var postData = {
                                "text": "Don't forget to study your topic for the day" + topicValue,
                                "Time": timeValue,
                                "Date": dateValue
                                };
                        $.ajax({
                            url: "http://127.0.0.1:5001/api/v1/reminder/",
                            type: "POST",
                            data: JSON.stringify(postData),
                            headers: {    
                                        "Content-Type" : "application/json",
                                    },
                            success: function(response) {
                                    var message = $("<div>");
                                    message.addClass("flash-message success");
                                    message.text("Reminder set for!" + dateObj.toISOString());
                                    $("body").append(message);
 
              // Automatically hide the message after a few seconds
                                    setTimeout(function() {
                                            message.hide();
                                        }, 5000);
                                    },
                            error: function(error) {
                                var message = $("<div>");
                                message.addClass("flash-message fail");
                                message.text("some error occured while updating Data!");
                                $("body").append(message);
 
                                // Automatically hide the message after a few seconds
                                setTimeout(function() {
                                message.hide();
                                                }, 5000);
                                    }
                    });
                    }, secondsUntilReminder * 1000);
                } else {
                    alert("Reminder time is not valid.");
                    }
            });
        });
    });
});


$(document).ready(function() {
        getQuote(); // Call getQuote() function on page load
		setInterval(getQuote, 60000);
        function getQuote() {
				$.ajax({
					url: "https://api.adviceslip.com/advice",
					type: 'GET',
					dataType: 'json',
					success: function(data) {
						$('#get-quote').text(data.slip.advice);
					},
					error: function(jqXHR, textStatus, errorThrown) {
						console.log('Error: ' + textStatus + ' - ' + errorThrown);
					}
				});
        };
	});
