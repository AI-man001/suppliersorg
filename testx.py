#!/usr/bin/python

import smtplib
from smtplib import SMTPException

sender = 'dzbusiness01@gmail.com'
receivers = ['divinezvenyika18@gmail.com']

message = """From: From Person <dzbusiness01@gmail.com>
To: To Person <divinezvenyika18@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
  smtpObj = smtplib.SMTP('localhost')
  smtpObj.sendmail(sender, receivers, message)
  print("Successfully sent email")
except SMTPException:
  print("Error: unable to send email")
