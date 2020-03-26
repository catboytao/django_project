from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30,unique=True,verbose_name="用户名",db_index=True)
    password = models.CharField(max_length=200,verbose_name="密码")
    email = models.CharField(max_length=30,unique=True,verbose_name="邮箱")
    phone_num = models.CharField(max_length=32,verbose_name="手机号")
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "用户信息"

class Files(models.Model):
    path = models.CharField(max_length=100,verbose_name="文件路径")
