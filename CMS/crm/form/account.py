#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 24/03/2020 15:58
# @Author  : Alan
# @Site    : 
# @File    : account.py
# @Software: PyCharm

## django ModelForm
import random

from django.core.exceptions import ValidationError
from django_redis import get_redis_connection

from crm import models
from django import forms
from django.core.validators import RegexValidator
# 注册
from utils.encrypt import md5
from crm.form.bootstrap import BootstrapFrom



class RegisterModelForm(BootstrapFrom,forms.ModelForm):
    phoneNumValidator = RegexValidator(r'^(1[3|4|5|6|7|8|9]\d{9}$)','手机号格式错误')
    phone_num = forms.CharField(label="手机号",validators=[phoneNumValidator])
    password = forms.CharField(label="密码",
                               min_length=8,
                               max_length=64,
                               error_messages={
                                 'min_length':'密码长度不能小于8个字符',
                                'max_length':'密码长度不能超过64个字符'
                               },
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="重复密码",widget=forms.PasswordInput(attrs={'placeholder':'请重复输入密码'}))
    code = forms.CharField(label="验证码")
    class Meta:
        #fields = "__all__"
        # 指定字段显示顺序
        fields = ["username","email","password","confirm_password","phone_num","code"]
        model = models.User
    # 重写__init__方法，对每一个字段都加上class=form-control


    # 校验用户名
    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username
    # 校验邮箱
    def clean_email(self):
        email = self.cleaned_data["email"]
        exists = models.User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("邮箱已存在")
        return email

    # 对密码进行md5加密
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return pwd
    # 校验两次密码是否相同
    def clean_confirm_password(self):
        # 注意 这里只能取到confirm_password前面的数据
        pwd = self.cleaned_data.get("password",None)
        confirm_pwd = self.cleaned_data["confirm_password"]
        if pwd != confirm_pwd:
            raise ValidationError("两次密码不一致")
        return confirm_pwd
    # 校验手机号
    def clean_phone_num(self):
        phone_num = self.cleaned_data["phone_num"]
        exists = models.User.objects.filter(phone_num=phone_num).exists()
        if exists:
            raise ValidationError("手机号已注册")
        return phone_num
    # 校验验证码
    def clean_code(self):
        phone_num = self.cleaned_data.get("phone_num")
        code = self.cleaned_data["code"].strip()
        if not phone_num:
            return code
        conn = get_redis_connection("default")
        redis_code = conn.get(phone_num)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")
        redis_code = redis_code.decode('utf-8')
        if code != redis_code:
            raise ValidationError("验证码输入错误，请重新输入")
        return code

from django.conf import settings
from utils.tencent.sms import send_sms_single
class SendSmsForm(forms.Form):
    phoneNumValidator = RegexValidator(r'^(1[3|4|5|6|7|8|9]\d{9}$)', '手机号格式错误')
    phone_num = forms.CharField(label="手机号", validators=[phoneNumValidator])

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request
    def clean_phone_num(self):
        '''
        手机号校验的钩子
        通过反射执行  判断是否已clean开头
        if hasattr(self, 'clean_%s' % name)
       '''
        phone_num = self.cleaned_data['phone_num']
        # 判断短信模板是否正确
        tpl = self.request.GET.get('tpl',None)
        tpl_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not tpl_id:
            raise ValidationError('短信模板错误')
        # 校验数据库中是否已有手机号
        if tpl == 'register':
            exists = models.User.objects.filter(phone_num=phone_num).exists()
            if exists:
                raise ValidationError('手机号已存在')

        # 校验都通过  发短信
        code = random.randrange(1000,9999)
        sms = send_sms_single(phone_num,tpl_id,[code,])
        if sms['result'] != 0:
            raise ValidationError('短信发送失败,{}'.format(sms['errmsg']))

        # 将验证码写入redis
        conn = get_redis_connection('default') # 获取连接
        conn.set(phone_num,code,ex=1000)

        return phone_num


# 登录Form

class LoginSmsForm(BootstrapFrom,forms.Form):
    phoneNumValidator = RegexValidator(r'^(1[3|4|5|6|7|8|9]\d{9}$)', '手机号格式错误')
    phone_num = forms.CharField(label="手机号", validators=[phoneNumValidator])
    code = forms.CharField(label="验证码",widget=forms.TextInput())
    # 校验手机号是否注册
    def clean_phone_num(self):
        phone_num = self.cleaned_data.get("phone_num")
        user_obj = models.User.objects.filter(phone_num=phone_num).first()
        if not user_obj:
            raise ValidationError("手机号不存在")
        return user_obj

    # 校验验证码
    def clean_code(self):
        user_obj = self.cleaned_data.get("phone_num")
        code = self.cleaned_data['code']
        if not user_obj:
            return code
        phone_num = user_obj.phone_num
        # 若phone_num未通过验证，不需要再验证code

        conn = get_redis_connection("default")
        redis_code = conn.get(phone_num)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")
        redis_code = redis_code.decode('utf-8')
        if code != redis_code:
            raise ValidationError("验证码输入错误，请重新输入")
        return code

# 用户名 密码 Form

class LoginForm(BootstrapFrom,forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密码",widget=forms.PasswordInput())
    code = forms.CharField(label="图片验证码")
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    # 对密码进行md5加密
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    # 验证图片验证码是否正确
    def clean_code(self):
        code = self.cleaned_data["code"].strip()
        # 去session中获取自己的验证码
        session_code = self.request.session.get("code")
        if not session_code:
            raise ValidationError("验证码过期，请重新获取")
        if code.upper() != session_code.upper():
            raise ValidationError("验证码输入有误")
        return code
