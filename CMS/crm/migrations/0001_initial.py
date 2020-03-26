# Generated by Django 3.0.3 on 2020-02-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('email', models.CharField(max_length=30, unique=True, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '用户信息',
            },
        ),
    ]
