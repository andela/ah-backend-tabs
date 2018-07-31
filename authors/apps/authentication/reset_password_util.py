from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template
import smtplib
import os


class ResetPasswordUtil():
    def send_mail(self, request, sender_email, reciever_email, token):
        msg = MIMEMultipart()

        if sender_email == None or reciever_email == None:
            raise ValueError('Invalid parameters!')

        msg['From'] = sender_email
        msg['To'] = reciever_email
        msg['Subject'] = "Reseting password for your Author's Haven account."
        body = self.html_renderer(request, token)
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', os.environ.get('EMAIL_PORT'))
        server.starttls()
        server.login(os.environ.get('EMAIL_HOST_USER'),
                     os.environ.get('EMAIL_HOST_USER_PASSWORD'))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    def html_renderer(self, request, token):
        template = get_template('authentication/reset_link.html')
        context = {'link': 'api/users/password/reset', 'token': token}
        return template.render(context, request)
