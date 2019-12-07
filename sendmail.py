# This python file will be used in order to send mail when an
# unrecognized face is detected
# Kirk Fay 11/28/19
import smtplib
def send():
    admin_account = 'INSERTADMINMAILHERE'
    admin_password = 'INSERTPASSHERE'
    sent_from = admin_account
    to = 'INSERTMAILHERE'
    subject = 'Unverified user detected!'
    body = "Please take appropriate action.\n\n"

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
        #Create an encrypted smtp server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(admin_account, admin_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        return ('Email sent successfully!')
    except:
        return ('Something went wrong...')
