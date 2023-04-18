let xhr;
let url = 'http://127.0.0.1:5001/api/v1/settings/'
let flashMsg = function(msg, type) {
    let message = $("<div>");
    message.addClass("flash-message " + type);
    message.text(msg);
    $("body").append(message);
    setTimeout(function() {
        message.hide();
    }, 7000);
}
let loader = function(btn) {
		  $(btn).html(
              '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...'
     );
}

let RequestCall = function(type, url, data, btn, text, callback) {
     $.ajax({
        url: url,
        type: type,
        headers: {
            "Content-Type": "application/json",
        },
        data: JSON.stringify(data),
        beforeSend: function(xhr) {
            xhr.setRequestHeader('x-access-token', getCookie('access_token'));
        },
        success: function(response) {
            
            callback(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('Error', textStatus, errorThrown);
            $(btn).html(text).find('span').remove();
            flashMsg(errorThrown, 'fail');
        }
    });
}


function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
 }    

$(document).ready(function () {
        const exampleModal = $('#exampleModal');
    exampleModal.on('show.bs.modal', function (event) {
            const button = $(event.relatedTarget)
            const recipient = button.data('bs-whatever');
            const modalBodyInput = exampleModal.find('#recipient-name');
            modalBodyInput.val(recipient);
        })
        $('#bi-modal').on('click', function() {
            exampleModal.modal('toggle');
            const recipientVal = exampleModal.find('#recipient-name').val();
            const key = exampleModal.find('#recipient-password').val();
            const data = {
                'Key': key,
                'Value': recipientVal,
                'option': 'username'
            };
            RequestCall('PUT', url, data, null, null, function(response) {
                location.reload();
            });
      });
    })

$(document).ready(function () {
    let opt;
    $("#mail-reset").click(function() {
        opt =  $(this).val();
        console.log(opt);
    });
    $('#send-confirm').on('click', function() {
        let btn = "#send-confirm";
        loader(btn);
        let text = "Send verification code"
        xhr = RequestCall('POST', url, {'option': 'email'}, btn, text, function(response) {
            $("#send-confirm").html(text).find('span').remove();
            $('#exampleModalToggle2').modal('show');
        });

    });
    $('#send-verifyCode').click(function() {
        const data = {}
        var code = $('#verify-code').val();
        data['code'] = code;
        data['option'] = 'confirmation';
        let btn = "#send-verifyCode";
        loader(btn);
        let text = "Next"
        RequestCall('POST', url, data, btn, text, function(response) {
            $(btn).html(text).find('span').remove();
            if (opt === 'email-reset') {
                $('#exampleModalToggle3').modal('show');
            } else {
                $('#exampleModalToggle4').modal('show');
            }
        });
        
    });
        $('#send-verifyEmail').click(function() {
            const data = {}
            var email = $('#email-reset').val();
            var passkey = $('#password-reset').val();
            data['email'] = email;
            data['passkey'] = passkey;
            data['option'] = 'emailreset';
            let btn = "#send-verifyEmail";
            loader(btn);
            let text = "Sent"

            RequestCall('PUT', url, data, btn, text, function(response) {
                $("#send-verifyEmail").html(text).find('span').remove();
                flashMsg("Email Reset", "success");
                location.reload();
            });

        });
    $('#account-removal').click(function() {
        const data = {}
        data['confirmDelete'] = true;
        data['option'] = 'deleteAccount';

        RequestCall('DELETE', url, data, null, null, function(response) {
            flashMsg(response.message, "success");
            window.location.replace('/login');
        });
    });

});

$("#cancel-btn").click(function() {
  // Check if xhr object exists and is not in a completed state
  if (xhr && xhr.readyState !== 4) {
    // Abort the Ajax request and update button text
    xhr.abort();
  }
});

$(document).ready(function () {
    $("#Mycontact").click(function() {
        console.log('clicked')
        let data = {}
        let btn = "Mycontact"
        loader(btn);
        let phone_number = $('#phone-number').val();
        data['phone_number'] = phone_number;
        data['option'] = 'contact';
        let btn2 = "#phone-contact";
        xhr = RequestCall('PUT', url, data, btn2, null, function(response) {
            $(btn2).find('span').remove();
            flashMsg(response.message, 'success');
            location.reload();
        });
    }); 
});


$(document).ready(function() {
  $('#reset-form').submit(function(event) {
    event.preventDefault();
   // var form_data = $(this).serialize();
     // console.log(form_data)
      var data = {
          "old_password": $('#old-pass').val(),
          "new_password": $('#new-pass').val(),
          "confirm_password": $('#new-passC').val(),
          "option": "password"
        }

    $.ajax({
      type: "PUT",
      url: url,
        headers: {
            "Content-Type": "application/json",
        }, 
      data: JSON.stringify(data),
        beforeSend: function(xhr) {
            xhr.setRequestHeader('x-access-token', getCookie('access_token'));
        },
        success: function(response) {
            var status = response.status;
            var message = response.message
          console.log(response)
          console.log(status)
          console.log(message)
        if (status == "success") {
          // Display success message
            location.reload();
            flashMsg(message, 'success');
        } else {
          // Display error message
          $(".modal-body").prepend(
            '<div class="alert alert-danger" role="alert">' +
              message +
              "</div>"
          );
        }
          setTimeout(function() {
            $(".alert").remove();
          }, 1000);
      },
      error: function(xhr, status, error) {
          console.log("Error: " + error);
      }
    });
  });
});

$(document).ready(function() {
    $('#clear-chatHistory').click(function() {
        var id = $('#usr-id').val();
        RequestCall('DELETE', url, {'option': 'chatHistory', 'id': id}, null, null, function(response) {
            flashMsg(response.message, 'success');
        });
    });
});

$(document).ready(function() {
    var checkBox = $('#flexSwitchCheckReverse').val()
    console.log(checkBox)
      if (checkBox === 'False') {
         $('#flexSwitchCheckReverse').attr('checked', false);
      }
        if (checkBox === 'True'){
              $('#flexSwitchCheckReverse').attr('checked', true);
        }
$('#flexSwitchCheckReverse').change(function() {
         var isChecked = $(this).is(':checked');
        var data = {
            'isChecked': isChecked,
            'option': 'checkBox'
        }
        if (isChecked) {
            isChecked = 'true';
        } else {
            isChecked = 'false';
        }
        
        RequestCall('POST', url, data, null, null, function(response) {
            flashMsg(response.message, 'success');
        });
    });
 
 });

$(document).ready(function() {
  $('#delete-course').click(function() {
    var course = $('input[name="listGroupRadio"]:checked').val();
    console.log(course);
    let data = {
        'course': course,
        'option': 'deleteCourse'
    }
      RequestCall('DELETE', url, data, null, null, function(response) {
            flashMsg(response.message, 'success');
        });
});
});

$(document).ready(function() {
    var course;
     var tempo = 0;
     $("#decrease-btn").click(function() {
         tempo--;
         $('#Icon-btn').css('color', '#29990a');
         $("#learning-pace").text(tempo + " Days");
         if (tempo < 0) {
             tempo=0
             $('#icon-btn').css('color', 'red');
            $("#learning-pace").text(tempo + " Days");
         }
     });
     $("#increase-btn").click(function() {
         tempo++;
         $('#icon-btn').css('color', '#29990a');
         $("#learning-pace").text(tempo + " Days");
         if (tempo >= 7) {
             tempo=7
             $('#Icon-btn').css('color', 'red');
            $("#learning-pace").text(tempo + " Days");
         }
     });

    $(".dropdown-item").click(function() {

            course = $(this).text();
            console.log(course)
            console.log(tempo)
    });
    $('#save-pace').click(function() {
        data = {
            "course": course,
            "tempo" : tempo,
            "option": "course_tempo"
        }
        if (tempo !== 0 && course !== ' '){
            RequestCall('PUT', url, data, null, null, function(response) {
            flashMsg(response.message, 'success');
        });
        }
        else {
            console.log('date can\'t be zero')
        };
    });
});

$(document).ready(function() {
    $("#btnNavbarSearch").click(function() {
        let text = $('#search-bar').val();
        let url = 'http://127.0.0.1:5001/api/v1/search/'
        let data = {
            'text': text,
            'option': 'search'
        }
        RequestCall('POST', url, data, null, null, function(response) {
            $("#staticBackdrop8").modal('show');
            $("#search-text").html(response);
            $("#staticBackdropLabel8").html('Search Results for ' + text);
        });
    });
});


