import re
from smtplib import SMTP_SSL as SMTP  # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.text import MIMEText

url_validator = lambda x: re.compile(
    r'(^(?:http|ftp)s?://)?' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE).match(x) is not None


def send_email(to, url):
    SMTPserver = 'smtp.126.com'
    sender =     'watchfox@126.com'
    destination = [to]

    USERNAME = "watchfox"
    PASSWORD = "watchfox179"

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'


    content="""Dear user,

Thanks for using WatchFox service. You are now subscribing %s. 

If there are any further changes, we will inform you through this email address.

Regards,

WatchFox Team
""" % url

    subject="[WatchFox]Kindly Reminder"


    # from smtplib import SMTP
    #  use this for standard SMTP protocol   (port 25, no encryption)

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except:
        pass