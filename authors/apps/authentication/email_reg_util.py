import os
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import jwt
from authors.settings.base import SECRET_KEY


class SendAuthEmail:
    def send_reg_email(self, request=None, sender_email=None, reciever_email=None, callback=None, token=None):

        msg = MIMEMultipart()

        if request == None or sender_email == None or reciever_email == None or token == None:
            raise ValueError('Invalid parameters!')

        msg['From'] = sender_email
        msg['To'] = reciever_email
        msg['Subject'] = "Welcome to Author's Haven!"
        body = self.html_renderer(request, callback, token)
        # body = 'hi there'
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', os.environ.get('EMAIL_PORT'))
        server.starttls()
        server.login(os.environ.get('EMAIL_HOST_USER'),
                     os.environ.get('EMAIL_HOST_USER_PASSWORD'))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    def html_renderer(self, request, callback, token):
        template = get_template('authentication/email_reg_util.html')
        decoded_token = jwt.decode(token, SECRET_KEY, 'HS256')
        decoded_token['callback'] = callback
        encoded_token = jwt.encode(
            decoded_token, SECRET_KEY, 'HS256').decode('utf-8')
        context = {'token': encoded_token}
        return template.render(context, request)
