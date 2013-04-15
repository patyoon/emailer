import smtplib
from private_config import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage

class gmail_smtp:

    def __init__(self, username, password, debug = False):
        self.smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        self.username = username
        self.password = password
        self.logged_in = False
        self.debug = debug

    def login(self):
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.ehlo
        self.smtp_server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        self.logged_in = True

    def send_email(self, to, subject, body):
        if not self.logged_in:
            self.smtp_server.login()
        #header = 'To:%s\nFrom:%s <%s>\nSubject:%s \n' %(to, GMAIL_NAME,
        #                                                GMAIL_USERNAME, subject)
        #msg = '%s\n %s \n\n' %(header, body)
        msg = MIMEMultipart("mixed")
        #body = MIMEMultipart("alternative")
        msg['From'] = "%s <%s>" %(GMAIL_NAME, self.username)
        msg['To'] = to
        #msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        smtp_result = self.smtp_server.sendmail(GMAIL_USERNAME, to,
                                                msg.as_string().encode('ascii'))
        if self.debug and smtp_result:
            errstr = ""
            for recip in smtpresult.keys():
                errstr = """Could not delivery mail to: %s

Server said: %s
%s
 
%s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
            raise smtplib.SMTPException, errstr
        
    def logout(self):
        if(not self.logged_in):
            self.logged_in = False
            self.smtp_server.close()
