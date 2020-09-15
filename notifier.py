import os
import smtplib
from email.message import EmailMessage
from requests_html import HTMLSession
import time

SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASS = os.environ.get('SENDER_PASS')
RECEIVER_EMAIL = os.environ.get('MAIN_EMAIL')
STREAMERS = ['soadsoap', 'noahb', 'burningamaranth']

def check_whos_online():
    session = HTMLSession()
    r = session.get('https://strims.gg/')
    r.html.render()

    online_streams = r.html.find('div.streams', first=True).find('div', first=True)
    streams_info = []

    # adds streamer info to a list; streamer name, title, viewer count
    for stream in online_streams.find('div.stream-caption'):
        t = stream.text.split(' ')
        if t[0] in STREAMERS:
            streams_info.append(t[0] + ' - ' +' '.join(t[2:]))

    return streams_info

def send_email(content):
    msg = EmailMessage()
    msg['Subject'] = 'Streamer Online!'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASS)

        smtp.send_message(msg)

if __name__ == '__main__':
    while True:
        message = ''
        info = []
        # if something goes wrong in the request, tries again in 1 minute
        try:
            info = check_whos_online()
        except:
            time.sleep(60)
            continue

        for line in info:
            message = message + line + '\n'

        send_email(message)

        time.sleep(300)