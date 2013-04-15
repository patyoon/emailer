from private_config import *
from gmail_imap import *
from gmail_smtp import gmail_smtp
from apscheduler.scheduler import Scheduler

sched = Scheduler()
email_sent = False
          
@sched.interval_schedule(seconds=30)
def check_email():
    global email_sent
    if not email_sent:
        gmail_imap = gmail_imap(GMAIL_USERNAME, GMAIL_PASSWORD)
        gmail_smtp = gmail_smtp(GMAIL_USERNAME, GMAIL_PASSWORD, debug=True)
        gmail_smtp.login()
        gmail_imap.mailboxes.load()
        gmail_imap.messages.process("INBOX")
        print "\n"
        #Print the full message text for the first two messages in the box
        for message_stub in gmail_imap.messages:
          message = gmail_imap.messages.getMessage(message_stub.uid)
          print message.From
          print message.Body
          if TARGET_FROM in message.From and re.search(r'formal', message.Body, re.I):
              print "found"
              gmail_smtp.send_email(TARGET_FROM, "Re: %s" %message.Subject, TARGET_BODY)
              print "sent"
        gmail_imap.logout()
        gmail_smtp.logout()

if __name__ == '__main__':
    sched.start()
    while True:
        pass
