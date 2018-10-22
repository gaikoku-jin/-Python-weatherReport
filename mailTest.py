import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

author = formataddr((str(Header(u'Marcin', 'utf-8')), "zakrzews@agh.edu.pl"))
toaddr = "marcin.zakrzewski@koliber.org"
msg = MIMEMultipart()
msg['From'] = author
msg['To'] = toaddr
msg['Subject'] = "Python email"
body = "Python test mail"
msg.attach(MIMEText(body, 'plain'))
print (msg)

##smtpObj = smtplib.SMTP_SSL('poczta.agh.edu.pl', 465)
##smtpObj.ehlo()
####smtpObj.starttls()
##smtpObj.login('zakrzews@agh.edu.pl', 'Zino-val')
##text = msg.as_string()
##smtpObj.sendmail(author, toaddr, text)
##smtpObj.quit()

import datetime

now = datetime.datetime.now()
print(now.strftime("%d-%m-%Y"))
