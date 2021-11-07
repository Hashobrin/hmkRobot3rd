import os

from email.mime.text import MIMEText
from email.utils import formatdate
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime import text
from email.mime.image import MIMEImage

from pathlib import Path

import smtplib
import ssl

from dbController import getRow
from config import config

def add_header(email):
    msg = MIMEMultipart()
    msg['Subject'] = config.subject
    msg['From'] = config.me
    # msg['To'] = ','.join(config.to)
    msg['To'] = email
    msg['Date'] = formatdate(localtime=True)
    return msg

def add_text(msg, text):
    _text = MIMEText(text+'\n', 'plain', config.charset)
    msg.attach(_text)
    return msg

def add_image(msg, fname):
    with open(fname, 'rb') as f:
        img = f.read()
        image = MIMEImage(img, name=fname.name)
    msg.attach(image)
    return msg

def compose(email):
    msg = add_header(email)
    msg = add_text(msg, 'testing')
    img_name = str(os.getcwd()) + '/qrcode/' + str(getRow()) + '.png'
    msg = add_image(msg, Path(img_name))
    return msg

def send(msg):
    server = smtplib.SMTP(config.host, config.port, timeout=10)
    server.starttls()
    server.ehlo()
    server.login(config.username, config.password)
    server.ehlo()
    server.send_message(msg)
    server.quit()

def main(email):
    msg = compose(email)
    send(msg)


if __name__ == '__main__':
    main()
