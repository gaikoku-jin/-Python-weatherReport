#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import smtplib
import urllib3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def sendMail(messageBody, recipient):
    author = formataddr((str(Header(u'Marcin', 'utf-8')), "zakrzews@agh.edu.pl"))
    toaddr = recipient
    msg = MIMEMultipart()

    date = datetime.datetime.now().strftime("%d-%m-%Y")
    msg['From'] = author
    msg['To'] = toaddr
    msg['Subject'] = "Podwawelski raport pogodowy "+date
    body = messageBody
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    smtpObj = smtplib.SMTP_SSL('poczta.agh.edu.pl', 465)
    smtpObj.ehlo()
    smtpObj.login('zakrzews@agh.edu.pl', 'Zino-val')
    text = msg.as_string()
    smtpObj.sendmail(author, toaddr, text)
    smtpObj.quit()
