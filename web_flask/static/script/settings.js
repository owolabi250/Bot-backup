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
           $.ajax({
          url: url,
          type: 'PUT',
          headers: {
            "Content-Type": "application/json",
          },
          data: JSON.stringify(data),
          beforeSend: function(xhr) {
            xhr.setRequestHeader('x-access-token', getCookie('access_token'));
          },
          success: function(response) {
            // upon success get response from request and append response to the chatbot div
             location.reload();

          },
          error: function(jqXHR, textStatus, errorThrown) {
            // upon error log error message and output a flash message on the chatbot div
            console.log('Error', textStatus, errorThrown);
            $('#nav-id').css('border', '.2em solid #FF5349');
            flashMsg(errorThrown, 'fail');
          }
        });
      });
    })

$(document).ready(function () {
    $('#send-confirm').on('click', function() {
        $(this).html(
            '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...'
    );
        xhr = $.ajax({
            url: url,
            type: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            data: JSON.stringify({'option': 'email'}),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('x-access-token', getCookie('access_token'));
            },
            success: function(response) {
                // upon success get response from request and append response to the chatbot div
                $("#send-confirm").html("Success!").find('span').remove();
                 $('#exampleModalToggle2').modal('show');
    },

            error: function(jqXHR, textStatus, errorThrown) {
                // upon error log error message and output a flash message on the chatbot div
                console.log('Error', textStatus, errorThrown);
                $("#myButton").html("Error!").find('span').remove();
            }

        });
    });
    $('#send-verifyCode').click(function() {
        $(this).html(
            '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...'
        );
        const data = {}
        var code = $('#verify-code').val();
        data['code'] = code;
        data['option'] = 'confirmation';
        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            data: JSON.stringify(data),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('x-access-token', getCookie('access_token'));
            },
            success: function(data) {
                $("#send-verifyCode").html("Success!").find('span').remove();
                $('#exampleModalToggle3').modal('show');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // upon error log error message and output a flash message on the chatbot div
                console.log('Error', textStatus, errorThrown);
                $("#send-verifyCode").html("Error!").find('span').remove();
            }
        });
    });
    $('#send-verifyEmail').click(function() {
        $(this).html(
            '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...'
        );
        const data = {}
        var email = $('#email-reset').val();
        var passkey = $('#password-reset').val();
        data['email'] = email;
        data['passkey'] = passkey;
        data['option'] = 'emailreset';
        $.ajax({
            url: url,
            type: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            data: JSON.stringify(data),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('x-access-token', getCookie('access_token'));
            },
            success: function(data) {
                console.log(data)
                $("#send-verifyEmail").html("Sent").find('span').remove();;
                location.reload();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // upon error log error message and output a flash message on the chatbot div
                console.log('Error', textStatus, errorThrown);
                $("#send-verifyEmail").html("Error").find('span').remove();
            }
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
        $(this).html(
            '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...'
    );
        let phone_number = $('#phone-number').val();
        data['phone_number'] = phone_number;
        data['option'] = 'contact';
        xhr = $.ajax({
            url: url,
            type: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            data: JSON.stringify(data),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('x-access-token', getCookie('access_token'));
            },
            success: function(response) {
                console.log(response)
                $("#phone-contact").find('span').remove();
                flashMsg(response.message, 'success');
                location.reload();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Error', textStatus, errorThrown);
                $("#phone-contact").find('span').remove();
                flashMsg(errorThrown, 'fail');
            }
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
          $(".modal-body").prepend(
            '<div class="alert alert-success" role="alert">' +
              message +
              "</div>"
          );
            setTimeout(function() {
            $(".alert").remove();
          }, 1000);
            location.reload();
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
        $.ajax({
            url: url,
            type: 'DELETE',
            headers: {
                "Content-Type": "application/json",
            },
            data: JSON.stringify({'option': 'chatHistory', 'id': id}),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('x-access-token', getCookie('access_token'));
            },
            success: function(data) {
                flashMsg(data.message, 'success');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Error', textStatus, errorThrown);
                flashMsg(errorThrown, 'fail');
            }
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
         $.ajax({
             url: url,
             type: "POST",
             beforeSend: function(xhr) {
                 xhr.setRequestHeader('x-access-token', getCookie('access_token'));
             },
             headers: {
                 "Content-Type": "application/json",
             },
             data: JSON.stringify(data),
             success: function(response) {
                 console.log(response);
                 flashMsg(response.message, 'success');
                },   
             error: function(xhr, status, error) {
                 console.log(error);
                 flashMsg(error, 'fail');
             }
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
    $.ajax({
        url: url,
        type: "DELETE",
        beforeSend: function(xhr) {
            xhr.setRequestHeader('x-access-token', getCookie('access_token'));
        },
        headers: {
            "Content-Type": "application/json",
        },
        data: JSON.stringify(data),
        success: function(response) {
            console.log(response);
            flashMsg(response.message, 'success');
        },
        error: function(xhr, status, error) {
            console.log(error);
            flashMsg('RECORD'+' '+ error, 'fail');
        }
  });
});
});
