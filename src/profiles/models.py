from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class BaseProfile(models.Model):
    TYPE_OF_USERS = (
        (None, '选择用户类型'),
        ('customer', '客户'),
        ('designer', '设计师'),
        ('maker', '制造商'),
        ('seller', '销售员'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True, verbose_name="用户")
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    picture = models.ImageField('用户照片',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField("个人简介", max_length=200, blank=True, null=True)
    first_name = models.CharField("名字", max_length=200, null=True)
    last_name = models.CharField("姓氏", max_length=200, null=True)

    user_type = models.CharField("用户类型", choices=TYPE_OF_USERS, max_length=20, null=True)
    phone = models.CharField("手机号", max_length=20, null=True)
    # User's address information
    country = models.CharField('国家', max_length=50, null=True)
    province = models.CharField('省份', max_length=50, null=True)
    city = models.CharField('城市', max_length=50, null=True)
    county = models.CharField('区县', max_length=50, null=True)
    street = models.CharField('详细地址', max_length=200, null=True)
    # Shipping address for the user
    ship_address = JSONField('送货地址', null=True)
    # The bank account or other financial accounts used for user's profit.
    income = models.PositiveIntegerField('销售收入', null=True)
    accounts = JSONField('资金帐户', null=True)


    email_verified = models.BooleanField("邮件地址", default=False)

    class Meta:
        abstract = True
        verbose_name = "详细信息"
        verbose_name_plural = "详细信息"


@python_2_unicode_compatible
class Profile(BaseProfile):

    def __str__(self):
        return "{}'s profile". format(self.user)
