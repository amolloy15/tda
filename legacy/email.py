import poplib
import smtplib
import socket
import ssl

from legacy.constants import c

pw = c['STOCKEMAIL_PW']
schedules = ['all', 'week', 'month', 'none']
settings = ['name', 'email', 'schedule']
debugEmail = ['amolloy.15@gmail.com']


def union(a, b):
    ret = a
    for e in b:
        if e not in a:
            ret.append(e)
    return ret


def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def send(receiver_emails, subject, msg):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    sender_email = "stocktradingreceipts@gmail.com"

    context = ssl.create_default_context()

    if not isinstance(receiver_emails, list):
        return

    if not isinstance(msg, str):
        msg = str(msg)

    message = ('Subject: %s\n\n' % subject) + msg

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, pw)

            for email in receiver_emails:
                server.sendmail(sender_email, email, message)

    except socket.gaierror:
        pass

