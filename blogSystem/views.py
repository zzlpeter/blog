# coding: utf-8

from django.shortcuts import render_to_response, RequestContext, render, HttpResponse

import models as blog_models
import json

# Create your views here.

def index(req, tmp_name='index.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))

def postDetail(req, category1=None, category2=None, post_id=None, tmp_name='postDetail.html'):
    postObj = blog_models.Post.objects.get(pk=2)
    return render_to_response(tmp_name, {'postObj': postObj}, context_instance=RequestContext(req))

def makePost(req, tmp_name='makePost.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))

def send_mail(req):
    import json
    # # from django.core.mail import EmailMessage
    # import smtplib
    # from email.mime.text import MIMEText
    # from email.header import Header
    # sender = 'from@runoob.com'
    # receivers = ['zhangzhiliang@cmcm.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #
    # # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    # message['From'] = Header("菜鸟教程", 'utf-8')
    # message['To'] = Header("测试", 'utf-8')
    #
    # subject = 'Python SMTP 邮件测试'
    # message['Subject'] = Header(subject, 'utf-8')
    #
    # try:
    #     smtpObj = smtplib.SMTP()
    #     smtpObj.connect('smtp.gmail.com', 25)
    #     smtpObj.starttls()
    #     smtpObj.login('liveme_cms_finance@conew.com', 'wckckzuthxcgivop')
    #     for _ in range(5):
    #         status = smtpObj.sendmail(sender, receivers, message.as_string())
    #         print "邮件发送成功", status
    #     return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')
    # except smtplib.SMTPException, exc:
    #     print exc
    #     print "Error: 无法发送邮件"
    #     return HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')
    from django.core.mail import EmailMessage
    try:
        # email = EmailMessage('test', 'this is a test mail', 'test@test.com', ['zhangzhiliang@cmcm.com'])
        # email.content_subtype = 'html'
        # email.attach('/Users/zhangzhiliang/zzl/mail.xls')
        # email.send()
        # return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')

        html_content = "Comment tu vas?"
        email = EmailMessage("my subject", html_content, "paul@polo.com", ['zhangzhiliang@cmcm.com','823515849@qq.com'])
        email.content_subtype = "html"

        fd = open('/Users/zhangzhiliang/zzl/mail.xls', 'r')
        email.attach('mail.xls', fd.read(), 'text/plain')

        res = email.send()
        return HttpResponse(json.dumps({'msg': 'success', 'num': res}), content_type='application/json')
    except Exception, exc:
        return HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

def postList(req, category1=None, category2=None, tmp_name='postList.html'):
    # if category2:
    #     obj = blog_models.Category.objects.filter()
    return render_to_response(tmp_name, context_instance=RequestContext(req))


def makePostTrue(req):
    author = req.user
    content = req.POST.get('content')
    blog_models.Post.objects.create(content=content, author_id=author.id, img_id=1)
    json_str = {'status': 1, 'msg': u'提交成功'}
    return _response_json(json_str)




def _response_json(data):
    return HttpResponse(json.dumps(data), content_type='application/json')



















