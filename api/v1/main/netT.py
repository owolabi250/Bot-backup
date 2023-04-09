import smtplib
import os
def send_email(user):
    try:
        sender_email = os.environ.get('MAIL_USERNAME')
        port = os.environ.get('MAIL_PORT')
        myserver = os.environ.get('MAIL_SERVER')
        passK = os.environ.get('MAIL_PASSWORD')
        token = user.generate_confirmation_code()
        code = token[0]
        receiver_email = user.Email
        msg = f"""<p>Before we change the email on your account,
                we just need to confirm that this is you. 
                Below is the verification code for your Discord account.
                {code}
                Don't share this code with anyone.
                If you didn't ask for this code, please ignore this email </p>.
            """
        with smtplib.SMTP(myserver, port) as server:
            server.starttls()
            server.login(sender_email, passK)
            server.sendmail(sender_email, receiver_email, msg)
            print("Email sent successfully")
    except Exception as e:
        return f"some error occured {e}"

