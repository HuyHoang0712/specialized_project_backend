import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ... import constants

port = 465  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = constants.sender_email
password = constants.password


def send_welcome_email(username, user_password, receiver_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Account created for user %s!" % (username)
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = """\
    <html>
    <body>
        <p>Welcome %s,</p>
        <br>Hear is your account information:<br> 
        <br>Username: %s<br>
        <br>Password: %s<br>
    </body>
    </html>
    """ % (
        username,
        username,
        user_password,
    )

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


# send_welcome_email("FuruyaRei", "viethung2002", "vuviethungnbee@gmail.com")
