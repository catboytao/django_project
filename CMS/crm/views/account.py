import datetime
import json
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from crm import models
from utils.encrypt import md5


def auth(func):

    def wapper(request,*args,**kwargs):
        username = request.session.get("username","")
        if username:
            res = func(request,*args,**kwargs)
            return res
        else:
            return redirect("/crm/login/sms/")
    return wapper


# def login(request):
#     msg = ''
#     if request.method == "GET":
#         #models.User.objects.create(username="Tom",password="123456",email="913614628@qq.com")
#         return render(request,"login.html",{"msg":msg})
#     elif request.method == "POST":
#         username = request.POST.get("username","")
#         password = request.POST.get("pwd","")
#         count = models.User.objects.filter(username=username,password=password).count()
#         if count == 1:
#             request.session["username"] = username
#             return redirect("/index")
#         else:
#             msg = "用户名或密码错误"
#             return render(request,"login.html",{"msg":msg})
#     else:
#         return render(request,"login.html",{"msg":msg})

#@auth
def index(request):

    return render(request, "index.html")

@auth
def logout(request):
    request.session.clear()
    return render(request, "login.html")


@auth
def upload(request):

    if request.method == "GET":
        file_list = models.Files.objects.all()
        return render(request, "upload.html", {"file_list":file_list})
    elif request.method == "POST":
        res = {"status": False, "path": None,"file_id":None,"msg":''}
        name = request.POST.get("username",None)
        fe = request.FILES.get("file",None)
        if fe:
            file_path = os.path.join("../static", "upload", fe.name)
            with open(file_path,'wb') as f:
                for chunk in fe.chunks():
                    f.write(chunk)
            file_obj = models.Files.objects.create(path=file_path)
            res["status"] = True
            res["file_id"] = file_obj.id
            res["path"] = file_path
            return HttpResponse(json.dumps(res))
        else:
            res["msg"] = "文件不能为空"
            return HttpResponse(json.dumps(res))
    else:
        return redirect("/upload.html")

@auth
def del_img(request):
    ret = {'status':True}
    try:
        img_id = request.GET.get('img_id',None)
        print(img_id)
        if img_id:
            models.Files.objects.filter(id=img_id).delete()
            ret["img_id"] = img_id
        else:
            ret["status"] = False
    except Exception as e:
        ret["status"] = False
    return HttpResponse(json.dumps(ret))


from crm.form.account import RegisterModelForm, SendSmsForm, LoginSmsForm, LoginForm


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, "register2.html", {"form":form})
    # 将数据传给ModelForm做校验
    form = RegisterModelForm(data=request.POST)
    ret = {"status":True,"msg":"注册成功"}
    if form.is_valid():
        # 验证成功  保存用户信息到数据库
        form.instance.password = md5(form.cleaned_data['password'])
        # 在用户表中新建一条数据
        instance = form.save() # 将数据保存到数据库，会自动剔除没用的字段
        # 创建交易记录
        policy_obj = models.PricePolicy.objects.filter(category=1,title="个人免费版").first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_obj,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
        ret["data"] = "/crm/login/sms/"
    else:
        ret["status"] = False
        ret["msg"] = "注册失败"
        ret["error"] = form.errors
    return JsonResponse(ret)

#  redis 操作
from django_redis import get_redis_connection

def redis_index(reqeust):
    value = None
    try:
        conn = get_redis_connection('default')
        value = conn.get('18223176663')
    except Exception as e:
        value = "redis连接失败"
    return HttpResponse(value)


# 检查验证码

def send_sms(request):
    '''发送短信'''
    #phone_num = request.GET.get('phone_num',None)
    #tpl = request.GET.get('tpl',None)
    # 将数据传给SendSmsForm做校验  data 为QueryDict类型
    form = SendSmsForm(request,data=request.GET)
    #只校验手机号，不能为空、格式是否正确
    if form.is_valid():
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,"error":form.errors})


# 短信认证登录
def login_sms(request):
    if request.method == 'GET':
        form = LoginSmsForm()
        return render(request, "sms_login.html", {"form":form})
    form = LoginSmsForm(data=request.POST)

    if form.is_valid():
        user_obj = form.cleaned_data['phone_num']
        # 将用户信息存入session中
        request.session['username'] = user_obj.username
        return JsonResponse({"status":True,"msg":"登录成功","data":"/crm/project/list"})
    return JsonResponse({"status":False,"error":form.errors})


# 用户名 密码登录

def login(request):
    if request.method == "GET":
        form = LoginForm(request)
        return render(request, "login.html", {"form":form})
    form = LoginForm(request,data=request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user_obj = models.User.objects.filter(username=username,password=password).first()
        if user_obj:
            request.session["user_id"] = user_obj.id
            request.session.set_expiry(60*60)
            return redirect("crm:project_list")
        else:
            form.add_error("username","用户名或密码错误")
    return render(request, 'login.html', {"form":form})
# 生成图片验证码
def image_code(request):
    from utils.image_code import check_code
    from io import BytesIO
    image_obj,img_code = check_code()
    # 将图片验证码写入session中
    request.session["code"] = img_code
    #设置session过期时间
    request.session.set_expiry(60) # 60秒
    # 将图片写入内存中
    stream = BytesIO()
    image_obj.save(stream,'png')
    return HttpResponse(stream.getvalue())

from crm.form.formsetDemo import ArticleFormSet

def formset(request):
    formset = ArticleFormSet()
    return render(request, "table.html", {"formset":formset})


# 退出登录

def logout(request):
    # 将session中数据清空
    request.session.flush()
    return redirect('crm:login')