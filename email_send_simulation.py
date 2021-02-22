import smtplib

SERVER = "localhost"
PORT = 1025
FROM = "admin@ericsson.com"


def simulate_sending_mails(email_list: list):
    if len(email_list) == 0:
        print("No emails to send!")
        return
    server = smtplib.SMTP(SERVER, PORT)
    for email in email_list:
        message = """\
        From: %s
        To: %s
        Topic: %s

        %s
        """ % (
            FROM, email.target_email, email.email_topic,
            email.email_content)

        server.sendmail(FROM, email.target_email, message)

    server.quit()
