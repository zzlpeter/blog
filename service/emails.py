# coding: utf-8

from django.core.mail import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import json
import smtplib
import logging
from django.conf import settings
from email.utils import formatdate

logger = logging.getLogger(__name__)


class Email():
    def __init__(self, mail_to, mail_content):
        # self.mail_subject = mail_subject
        self.mail_to = mail_to
        self.mail_from = 'yinuo@blog.com'
        self.user = settings.EMAIL_HOST_USER
        self.pwd = settings.EMAIL_HOST_PASSWORD
        self.content = mail_content

    def send(self):
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        # message = MIMEText('激活邮件', 'plain', 'utf-8')
        # message['From'] = Header("激活邮件", 'utf-8')
        # message['To'] = Header("激活邮件", 'utf-8')
        subject = '博客-激活邮件'
        # message['Subject'] = Header(subject, 'utf-8')
        # message.attach(MIMEText(self.content, _subtype='html', _charset='utf-8'))

        msg = MIMEMultipart()
        msg['From'] = self.mail_from
        msg['Subject'] = subject
        msg['To'] = self.mail_to  # COMMASPACE==', '
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(self.content, _subtype='html', _charset='utf-8'))

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect('smtp.gmail.com', 25)
            smtpObj.starttls()
            smtpObj.login(self.user, self.pwd)
            status = smtpObj.sendmail(self.mail_from, self.mail_to, msg.as_string())
            print "邮件发送成功", status
            # return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')
        except smtplib.SMTPException, exc:
            logger.error(exc, exc_info=True)
            logger.error(u'Error: 无法发送邮件')