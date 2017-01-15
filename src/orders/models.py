from django.db import models
from shop.models import Product
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='国家')

    class Meta:
        verbose_name = '国家'
        verbose_name_plural = '国家'

    def __str__(self):
        return self.name

class Province(models.Model):
    country = models.ForeignKey(Country, verbose_name='国家')
    name = models.CharField(max_length=50, verbose_name='省份')

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = '省份'

    def __str__(self):
        return self.name

class City(models.Model):
    province = models.ForeignKey(Province, verbose_name='省份')
    name = models.CharField(max_length=50, verbose_name='城市')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = '城市'

    def __str__(self):
        return self.name

class County(models.Model):
    city = models.ForeignKey(City, verbose_name='城市')
    name = models.CharField(max_length=50, verbose_name='区县')

    class Meta:
        verbose_name = '区县'
        verbose_name_plural = '区县'

    def __str__(self):
        return self.name

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='名字')
    last_name = models.CharField(max_length=50, verbose_name='姓氏')
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name='电话号码')
    # 地址用smart-selects来进行筛选
    country = models.ForeignKey(Country, verbose_name='国家')

    province = ChainedForeignKey(Province,
                             chained_field="country",
                             chained_model_field="country",
                             show_all=False,
                             auto_choose=True,
                             sort=True, verbose_name='省份')

    city = ChainedForeignKey(City,
                             chained_field="province",
                             chained_model_field="province",
                             show_all=False,
                             auto_choose=True,
                             sort=True, verbose_name='城市')

    county = ChainedForeignKey(County,
                             chained_field="city",
                             chained_model_field="city",
                             show_all=False,
                             auto_choose=True,
                             sort=True, verbose_name='区县')
#    area = JSONField(blank=True, null=True, verbose_name='所在区域')
    address = models.CharField(max_length=250, verbose_name='收货地址')
    postal_code = models.CharField(max_length=20, verbose_name='邮政编码')
    created = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    paid = models.BooleanField(default=False, verbose_name='已支付？')
    received = models.BooleanField(default=False, verbose_name='已收货？')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customers', verbose_name='购买人')

    class Meta:
        ordering = ('-created',)
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return '订单 {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.item.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name='订单号')
    product = models.ForeignKey(Product, related_name='order_items', verbose_name='产品')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')

    class Meta:
        verbose_name = '订单内容'
        verbose_name_plural = '订单内容'

    def __str__(self):
        return '{}'.format(settings.id)

    def get_cost(self):
        return self.price * self.quantity


