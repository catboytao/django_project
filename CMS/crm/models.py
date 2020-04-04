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


class PricePolicy(models.Model):
    '''
    价格策略
    '''
    CATEGORY_CHOICE = (
        (1,"免费版"),
        (2,"收费版"),
        (3,"其他"),
    )
    category = models.SmallIntegerField(verbose_name="收费类型",choices=CATEGORY_CHOICE,default=2)
    title = models.CharField(verbose_name="标题",max_length=32)
    price = models.PositiveIntegerField(verbose_name="价格")
    # PositiveIntegerField 正整数
    project_num = models.PositiveIntegerField(verbose_name="项目数")
    project_member = models.PositiveIntegerField(verbose_name="项目成员数")
    project_space = models.PositiveIntegerField(verbose_name="单项目空间")
    per_file_size = models.PositiveIntegerField(verbose_name="单文件大小（M）")

    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

class Transaction(models.Model):
    '''
    交易记录
    '''
    STATUS_CHOICE = (
        (1,"未支付"),
        (2,"已支付")
    )

    status = models.SmallIntegerField(verbose_name="状态",choices=STATUS_CHOICE)

    order = models.CharField(verbose_name="订单号",max_length=64,unique=True)
    user = models.ForeignKey(verbose_name="用户",to="User",on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name="价格策略",to="PricePolicy",on_delete=models.CASCADE)

    count = models.IntegerField(verbose_name="数量（年）",help_text="0表示无限期")
    price = models.IntegerField(verbose_name="实际支付价格")

    start_datetime = models.DateTimeField(verbose_name="开始时间",null=True,blank=True)
    end_datetime = models.DateTimeField(verbose_name="结束时间",null=True,blank=True)

    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

class Project(models.Model):
    '''
    项目表
    '''
    COLOR_CHOICE = (
        (1,"#56b8eb"),
        (2,"#f28033"),
        (3,"#ebc656"),
        (4,"#a2d148"),
        (5,"#20BFA4"),
        (6,"#7461c2"),
        (7,"#20bfa3"),
    )
    project_name = models.CharField(verbose_name="项目名",max_length=64)
    desc = models.CharField(verbose_name="项目描述",max_length=255,null=True,blank=True)
    color = models.SmallIntegerField(verbose_name="颜色",choices=COLOR_CHOICE,default=1)
    use_space = models.IntegerField(verbose_name="项目已使用空间",default=0)
    star = models.BooleanField(verbose_name="星标",default=False)

    join_count = models.SmallIntegerField(verbose_name="参与人数",default=1)
    creator = models.ForeignKey(verbose_name="创建者",to="User",on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

class ProjectUser(models.Model):
    '''
    项目参与者
    '''

    user = models.ForeignKey(verbose_name="参与者",to="User",related_name='a',on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name="项目",to="Project",on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name="星标",default=False)
    invitee = models.ForeignKey(verbose_name="邀请者",to="User",related_name='b',on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)




