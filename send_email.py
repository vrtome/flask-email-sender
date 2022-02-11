#from multiprocessing import context
import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, body, sender, recipient, senderPassword, file):
    port = 465  #SSL
    smtp_server = "smtp.gmail.com"
    #"v1tr.test+sender@gmail.com"
    sender_email = sender
    #"v1tr.test+receiver@gmail.com"
    receiver_email = recipient
    #tVdMrb78fqNZzfh
    password = senderPassword  #input("Type your password and press enter: ")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Bcc"] = receiver_email

    text = body
    html = "<html><body><p>" + body + "</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    filename = file
    if filename != "":
        with open(filename, "rb") as attachment:
            part3 = MIMEBase("application", "octet-stream")
            part3.set_payload(attachment.read())

        encoders.encode_base64(part3)

        part3.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part3)

    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def main():
    send_email()


if __name__ == '__main__':
    main()
