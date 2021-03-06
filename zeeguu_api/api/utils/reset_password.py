from smtplib import SMTP

from zeeguu_api.app import app

def content_of_email_with_code(from_email, to_email, code):
    from email.mime.text import MIMEText

    body = "\r\n".join([
              "Hi there,",
              " ",
              "Please use this code to reset your password: " + str(code) + ".",
              " ",
              "Cheers,",
              "The Zeeguu Team"
          ])

    message = MIMEText(body)
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = 'Reset your password'

    return message.as_string()

def send_password_reset_email(to_email, code):
    # Fetch SMTP info
    server_name = app.config.get('SMTP_SERVER')
    our_email = app.config.get('SMTP_USERNAME')
    password = app.config.get('SMTP_PASSWORD')

    # Construct message
    message = content_of_email_with_code(from_email=our_email, to_email=to_email, code=code)

    # Send email
    server = SMTP(server_name)
    server.ehlo()
    server.starttls()
    server.login(user=our_email, password=password)
    server.sendmail(from_addr=our_email, to_addrs=to_email, msg=message)
    server.quit()
