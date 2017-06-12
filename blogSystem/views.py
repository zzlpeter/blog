# coding: utf-8

from django.shortcuts import render_to_response, RequestContext, render, HttpResponse

# Create your views here.

def index(req, tmp_name='index.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))

def postDetail(req, tmp_name='postDetail.html'):
    data = '''
    ### Django用gmail短时间内多次发邮件的问题
- [ ] **问题描述**
    - ```Django + uwsgi + gmail + smtplib```短时间内多次发邮件，如果短时间内触发了5封邮件的动作，发现只能收到3封邮件，而且这三封邮件几乎没有任何延迟就可以收到。但是3封之后的邮件就有问题了，一直无法收到；而且也没有报任何异常。
- [ ] **解决问题**
    - 为了解决这个问题，可算是费了半天劲儿。
    - 开始加日志的时候少传一个参数，导致即便是邮件发送失败了，但是依然没有报任何异常，且对比以下两段代码：
    
        ```
        try:
            for _ in range(5):
                smtpObj = smtplib.SMTP()
                smtpObj.connect('smtp.gmail.com', 25, fail_silently=False)
                smtpObj.starttls()
                smtpObj.login('liveme_cms_finance@conew.com','wckckzuthxcgivop')
                status = smtpObj.sendmail(sender, receivers, message.as_string())
                print "邮件发送成功",status
        except smtplib.SMTPException, exc:
            print exc
            print "Error: 无法发送邮件"
            
        5个邮件只能收到3个，第四个会报[Errno 101] Network is unreachable异常
        ```
        
        ```
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect('smtp.gmail.com', 25, fail_silently=False)
            smtpObj.starttls()
            smtpObj.login('liveme_cms_finance@conew.com','wckckzuthxcgivop')
            for _ in range(5):
                status = smtpObj.sendmail(sender, receivers, message.as_string())
                print "邮件发送成功",status
        except smtplib.SMTPException, exc:
            print exc
            print "Error: 无法发送邮件"
        
        5个邮件都可以正常收到
        ```
- [ ] **问题分析**
    - 如果不加参数fail_silently=False的话，那么即便邮件发送失败了，也不会报任何异常。
    - 第一种方式之所以会失败，是因为每次发邮件都需要建立一次链接，系统的25端口可能由于安全机制的策略，如果短时间内频繁访问25端口的话就直接报[Errno 101] Network is unreachable异常，默认情况下系统的80和443端口是永久开放并不受类似于iptables的限制的
    - 第二种方式之所以都可以发送成功，是因为只建立了一次链接，只要该链接不关闭，正常情况下是可以不断的发送邮件的；经本地测试，只要链接不关闭，连续发10个是没有问题的。
       
    '''
    return render_to_response(tmp_name, {'data':data}, context_instance=RequestContext(req))

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

def postList(req, tmp_name='postList.html'):
    return render_to_response(tmp_name, context_instance=RequestContext(req))