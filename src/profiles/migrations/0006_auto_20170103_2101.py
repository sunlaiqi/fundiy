# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20170102_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('customer', '客户'), ('designer', '设计师'), ('maker', '制造商'), ('seller', '销售员')], max_length=20, null=True, verbose_name='用户类型'),
        ),
    ]
