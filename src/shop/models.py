from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from .utils import front_image, back_image



class Catalog(models.Model):
    name = models.CharField(max_length=255, verbose_name="目录名称") # 目录的名称
    slug = models.SlugField(max_length=150)	#slug字段
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, max_length=300, verbose_name="发布人")	#发布者或者生产者
    discount = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="折扣")
    description = models.TextField(verbose_name="目录介绍")	#目录描述信息
    created = models.DateTimeField(auto_now_add=True) #发布日期
    updated = models.DateTimeField(auto_now=True)  #更新的日期

    class Meta:
        ordering = ('name',)
        verbose_name = '产品目录'
        verbose_name_plural = '产品目录'

    def __str__(self):
        return self.name

class Category(MPTTModel):
    catalog = models.ForeignKey('Catalog', related_name='categories', verbose_name="产品目录", blank=True, null=True) #指向Catalog
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name="父类型") # 指向自己，创建分类的树形目录结构
    name = models.CharField(max_length=200,
                            db_index=True, verbose_name="类型名称")
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
    description = models.TextField(blank=True, verbose_name="类型描述")
    class Meta:
        ordering = ('name',)
        verbose_name = '产品分类'
        verbose_name_plural = '产品分类'
        # verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(MPTTModel):

    category = models.ForeignKey(Category,
                                 related_name='products', verbose_name="产品类型")
    name = models.CharField(max_length=200, verbose_name="产品名称")
    # parent指向自己，创建产品的树形目录结构
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name="基础产品")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owners', verbose_name="所有者")
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, verbose_name="产品描述")

    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name="价格")
    discount = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="折扣")
    stock = models.PositiveIntegerField(verbose_name="库存量")
    available = models.BooleanField(default=True, verbose_name="在售？")
    created = models.DateTimeField(auto_now=True, verbose_name="上架时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 设计师生成的产品。attribute主要是前后左右的图片
    image_front = models.ImageField('正面图片',
                                upload_to=front_image,
                                null=True,
                                blank=True)
    image_back = models.ImageField('背面图片',
                                upload_to=back_image,
                                null=True,
                                blank=True)
    image_back_available = models.BooleanField(default=False, verbose_name="有背面？")
    attribute = JSONField(verbose_name="产品特有属性")
    sale = models.PositiveIntegerField(verbose_name="销量")

    # 由于产品之间存在父子关系，子产品的某些属性依赖于父产品
    def save(self, *args, **kwargs):
        if self.parent:
            self.category = self.parent.category
            self.stock = self.parent.stock
            self.attribute = self.parent.attribute
            if not self.parent.image_back_available:
                self.image_back_available = False

            if not self.parent.available:
                self.available = False

        super(Product, self).save(*args, **kwargs)



    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = '产品'
        verbose_name_plural = '产品'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class ProductAttribute(models.Model):
    name = models.CharField(max_length=20, verbose_name="产品属性名称")
    type = models.CharField(max_length=20, verbose_name="产品属性类型")
    description = models.TextField(verbose_name="产品属性描述")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = '产品属性'
        verbose_name_plural = '产品属性'

class ProductReview(models.Model):
    # 可能有安全隐患，用户可能会无限回复导致垃圾数据
    name = models.CharField(max_length=200, verbose_name="评论名称")
    slug = models.SlugField(max_length=200, db_index=True)
    design_product = models.ForeignKey(Product, related_name='products', verbose_name="被评论商品")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users', verbose_name="评论的用户")
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', verbose_name="回复的评论") # 指向自己，创建评论树
    review = models.TextField(verbose_name="评论内容")
    rating = models.PositiveSmallIntegerField(verbose_name="")
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = '商品评价'
        verbose_name_plural = '商品评价'

    def __str__(self):
        return self.name


