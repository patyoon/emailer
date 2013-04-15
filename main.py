from private_config import *
from apscheduler.scheduler import Scheduler
import sys, re, logging
logging.basicConfig(level=logging.INFO)
log_handler = logging.StreamHandler(stream=sys.stdout)
sched = Scheduler()
email_sent = False
logger = logging.getLogger("emailer")
logger.addHandler(log_handler)

@sched.interval_schedule(seconds=30)
def check_email():
    global email_sent
    from gmail_imap import gmail_imap
    from gmail_smtp import gmail_smtp
    if not email_sent:
        gmail_imap = gmail_imap(GMAIL_USERNAME, GMAIL_PASSWORD)
        gmail_smtp = gmail_smtp(GMAIL_USERNAME, GMAIL_PASSWORD, debug=True)
        gmail_smtp.login()
        gmail_imap.mailboxes.load()
        gmail_imap.messages.process("INBOX")
        for message_stub in gmail_imap.messages:
            message = gmail_imap.messages.getMessage(message_stub.uid)
            if TARGET_FROM in message.From and re.search(r'formal', message.Body, re.I):
                logger.info("target email found")
                gmail_smtp.send_email(TARGET_FROM, "Re: %s" %message.Subject, TARGET_BODY)
                logger.info("reply sent")
                email_sent = True
                break
        logger.info("target email not found")
        gmail_imap.logout()
        gmail_smtp.logout()
    else:
        logger.info("sent email. shutting down scheduler")
        sched.unschedule_job(check_email.job)

sched.start()
while not email_sent:
    pass
