# coding: utf-8

from django.core.mail import EmailMessage
from email.mime.text import MIMEText
from email.header import Header
import json
import smtplib
import logging

logger = logging.getLogger(__name__)


class Email():
    def __init__(self, mail_subject, mail_to):
        self.mail_subject = mail_subject
        self.mail_to = mail_to
        self.mail_from = 'yinuo@blog.com'

    def send(self):
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
        message['From'] = Header("菜鸟教程", 'utf-8')
        message['To'] = Header("测试", 'utf-8')

        subject = 'Python SMTP 邮件测试'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect('smtp.gmail.com', 25)
            smtpObj.starttls()
            smtpObj.login('liveme_cms_finance@conew.com', 'wckckzuthxcgivop123')
            # for _ in range(5):
            status = smtpObj.sendmail(self.mail_from, self.mail_to, message.as_string())
            print "邮件发送成功", status
            # return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')
        except smtplib.SMTPException, exc:
            logger.error(exc, exc_info=True)
            logger.error(u'Error: 无法发送邮件')