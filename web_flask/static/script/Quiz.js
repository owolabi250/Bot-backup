$(document).ready(function() {
     $('#quiz-btn').click(function() {
        var requestsent = false
        if (requestsent) {
          return;
        }
       var answers = {};
       var data = {};
       var dataID = $('.data_id').text().trim().split(' ').pop();

       $('.input-group input[type="text"]').each(function() {
         var answer = $(this).val().trim();
         var question = $(this).closest('.qanda').find('.question p').text().trim();
         if (answer.split(/\s+/).length <= 250) {
             if (answers.hasOwnProperty(question)) {
                answers[question].push(answer);
                 } else {
          answers[question] = [answer];
          data[dataID] = answers
        }
      }
       });
         console.log(data)

         
       $.ajax({
         type: 'POST',
         url: 'http://127.0.0.1:5001/api/v1/quiz',
         data: JSON.stringify(data),
         contentType: 'application/json',
         success: function(response) {
           console.log(response);
            var correction_button = '<button id="view-correction" class="btn btn-info">View Correction</button>';
             if ($('#view-correction').length === 0) {
                    $('#quiz-btn').after(correction_button);
                }
            $('#view-correction').on('click', function() {
                console.log('im in')
                $.each(response, function(Key, value) {
                    console.log(Key, value)
                    $.each(value, function(K, V) {
                    console.log(K)
                    if (K === "True" || K === "False") {
                            $.each(V, function(q, a) {
                                console.log(q)
                                var question = $('.qanda .question p').filter(function() {
                                            return $(this).text().trim() === q;
                                });
                                console.log(question)
                                if (question.length > 0 && K === "True") {
                                    console.log('im in to check')
                                    if (question.next('span.correct').length === 0) {
                                            question.after('<span class="correct"><iconify-icon icon="icon-park:correct"></iconify-icon></span>');
                                    }
                                } else {
                                     if (question.next('span.incorrect').length === 0) {
                                            question.after('<span class="incorrect"><iconify-icon icon="icon-park-solid:file-failed"></iconify-icon></span>');
                                            console.log('im in to check again')
                                        }
                                }
                        });
                    }
                });
            });
        });
 
            var message = $("<div>");
            message.addClass("flash-message success");
            message.text("You have successfully completed the quiz.");
           $("body").append(message);
 
           // Automatically hide the message after a few seconds
           setTimeout(function() {
             message.hide();
           }, 5000);
            requestsent = true;

         },
         error: function(xhr, textStatus, errorThrown) {
           console.log('Error:', errorThrown);
            var message = $("<div>");
            message.addClass("flash-message fail");
            message.text("Some error occured while submitting quiz request");
           $("body").append(message);
 
           // Automatically hide the message after a few seconds
           setTimeout(function() {
             message.hide();
           }, 5000);

         }
       });
    
       
     });
   });

/*
$(Document).ready(function() {
    $('#view-correction').click(function() {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1.5001/api/v1/quiz',
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                console.log(data)
                $.each(data, function(key, value) {
                    if (key === "True" || key === "False") {
                        $.each(value, function(q, a) {
                            var answer = $('input[name="' + q + '"]');
                            if (answer.val() === a) {
                                answer.after('<span class="correct">✔</span>');
                                } else {
                                    answer.after('<span class="incorrect">✘</span>');
                                }
                        });
                            }
                });
            },
            error: function(xhr, textstatus, errorThrown) {
                console.log('Error', errorThrown)
            }
        });
    });
});
*/
