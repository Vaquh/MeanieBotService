import smtplib
from email.MIMEMultipart    import MIMEMultipart
from email.MIMEText         import MIMEText
from contextlib             import contextmanager
from timeit                 import default_timer        as timer

#Grabs email addresses from emails.txt, puts strings into an array(list)
email_list = []
with open('emails.txt', 'r') as text_file:
    for line in text_file:
        line = line.strip()
        if line:
            email_list.append(line)

@contextmanager
def logined(sender, password, smtp_host = 'smtp.gmail.com', smtp_port = 587):
    start = timer(); smtp_serv = smtplib.SMTP(smtp_host, smtp_port, timeout = 10)
    try: #Make smtp server and login
        smtp_serv.ehlo_or_helo_if_needed()
        smtp_serv.starttls()
        smtp_serv.ehlo()
        print('smtp setup took (%.2f seconds passed)' % (timer()-start,))
        start = timer(); smtp_serv.login(sender, password)
        print('login took %.2f seconds' % (timer()-start,))
        start = timer(); yield smtp_serv
    finally:
        print('Operations with smtp_serv took %.2f seconds' % (timer()-start,))
        start = timer(); smtp_serv.quit()
        print('Quiting took %.2f seconds' % (timer()-start,))

smtp_host = 'smtp.gmail.com'
login = 'meaniebotservices@gmail.com'; password = [redacted]
email_count = len(email_list)

with logined(login, password, smtp_host) as smtp_serv:
    for i in range(email_count):
        #Grabs recipients from email_list array
        reciever = email_list[i]
         
        #Message
        msg = MIMEMultipart('alternative')
        msg['From'] = login
        msg['To'] = reciever
        msg['Subject'] = "Daily Meanie"
        plain = 'Meanie.\r\n\r\nMeanie Bot is a programming experiment by a novice programmer, used to help learn some basic coding.  Your email will never be sold or used for any other purpose other than this service.'
        html = '''\
        <html>
            <head></head>
            <body>
                <p>Meanie.<br>
                <br>
                <font size=1><i>Meanie Bot is a programming experiment by a novice programmer, used to help learn some basic coding.<br>
                Your email will never be sold or used for any other purpose other than for the FaggotBot service.</i></font>
                </p>
            </body>
        </html>
        '''
        msg.attach(MIMEText(plain, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        smtp_serv.sendmail(login, reciever, msg.as_string())
