# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 14:11
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='baseproduct',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='baseproduct',
            name='category',
        ),
        migrations.RemoveField(
            model_name='baseproduct',
            name='maker',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': '产品', 'verbose_name_plural': '产品'},
        ),
        migrations.AddField(
            model_name='product',
            name='attribute',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='attribute', verbose_name='产品特有属性'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owners', to=settings.AUTH_USER_MODEL, verbose_name='所有者'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.Product', verbose_name='基础产品'),
        ),
        migrations.AddField(
            model_name='product',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=10, verbose_name='库存量'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Category', verbose_name='产品类型'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='上架时间'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='产品描述'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='产品名称'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='base_product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='designer',
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set([('id', 'slug')]),
        ),
        migrations.DeleteModel(
            name='BaseProduct',
        ),
    ]
