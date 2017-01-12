# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 16:07
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import shop.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='产品名称')),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='产品描述')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='基础价格')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='折扣')),
                ('stock', models.PositiveIntegerField(verbose_name='库存量')),
                ('available', models.BooleanField(default=True, verbose_name='在售？')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='上架时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('image_front', models.ImageField(blank=True, null=True, upload_to=shop.utils.front_product_image, verbose_name='正面图片')),
                ('image_back', models.ImageField(blank=True, null=True, upload_to=shop.utils.back_product_image, verbose_name='背面图片')),
                ('image_back_available', models.BooleanField(default=False, verbose_name='有背面？')),
                ('attribute', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='产品特有属性')),
                ('sale', models.PositiveIntegerField(verbose_name='销量')),
            ],
            options={
                'verbose_name_plural': '基础产品',
                'verbose_name': '基础产品',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='目录名称')),
                ('slug', models.SlugField(max_length=150)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='折扣')),
                ('description', models.TextField(verbose_name='目录介绍')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('publisher', models.ForeignKey(max_length=300, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布人')),
            ],
            options={
                'verbose_name_plural': '产品目录',
                'verbose_name': '产品目录',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='类型名称')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='类型描述')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('catalog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='shop.Catalog', verbose_name='产品目录')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.Category', verbose_name='父类型')),
            ],
            options={
                'verbose_name_plural': '产品分类',
                'verbose_name': '产品分类',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveIntegerField(default=0, verbose_name='产品类型')),
                ('name', models.CharField(max_length=200, verbose_name='商品名称')),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='设计描述')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='设计师价格')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='折扣')),
                ('available', models.BooleanField(default=True, verbose_name='在售？')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='上传时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('image_front', models.ImageField(blank=True, null=True, upload_to=shop.utils.front_design_image, verbose_name='正面图片')),
                ('image_back', models.ImageField(blank=True, null=True, upload_to=shop.utils.back_design_image, verbose_name='背面图片')),
                ('image_back_available', models.BooleanField(default=False, verbose_name='有背面？')),
                ('sale', models.PositiveIntegerField(verbose_name='销量')),
                ('base_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.BaseProduct', verbose_name='基础产品')),
                ('designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='designers', to=settings.AUTH_USER_MODEL, verbose_name='设计师')),
            ],
            options={
                'verbose_name_plural': '销售成品',
                'verbose_name': '销售成品',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='产品属性名称')),
                ('type', models.CharField(max_length=20, verbose_name='产品属性类型')),
                ('description', models.TextField(verbose_name='产品属性描述')),
            ],
            options={
                'verbose_name_plural': '产品属性',
                'verbose_name': '产品属性',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='评论名称')),
                ('slug', models.SlugField(max_length=200)),
                ('review', models.TextField(verbose_name='评论内容')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='')),
                ('created', models.DateTimeField(auto_now=True)),
                ('design_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Product', verbose_name='被评论商品')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='shop.ProductReview', verbose_name='回复的评论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='评论的用户')),
            ],
            options={
                'verbose_name_plural': '商品评价',
                'verbose_name': '商品评价',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_products', to='shop.Category', verbose_name='产品类型'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='maker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='makers', to=settings.AUTH_USER_MODEL, verbose_name='制造商'),
        ),
        migrations.AlterIndexTogether(
            name='baseproduct',
            index_together=set([('id', 'slug')]),
        ),
    ]
