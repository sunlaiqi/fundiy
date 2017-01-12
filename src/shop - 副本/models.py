from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from .utils import front_product_image, back_product_image, front_design_image, back_design_image



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

# 为了程序上的方便，将未有设计的产品命名为BaseProduct，将有设计的产品命名为Product
class BaseProduct(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='base_products', verbose_name="产品类型")
    name = models.CharField(max_length=200, db_index=True, verbose_name="产品名称")
    maker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='makers', verbose_name="制造商")

    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, verbose_name="产品描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="基础价格")
    discount = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="折扣")
    stock = models.PositiveIntegerField(verbose_name="库存量")
    available = models.BooleanField(default=True, verbose_name="在售？")
    created = models.DateTimeField(auto_now_add=True, verbose_name="上架时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    image_front = models.ImageField('正面图片',
                                upload_to=front_product_image,
                                null=True,
                                blank=True)
    image_back = models.ImageField('背面图片',
                                upload_to=back_product_image,
                                null=True,
                                blank=True)
    image_back_available = models.BooleanField(default=False, verbose_name="有背面？")
    attribute = JSONField(verbose_name="产品特有属性")
    sale = models.PositiveIntegerField(verbose_name="销量")


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = '基础产品'
        verbose_name_plural = '基础产品'

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

class Product(models.Model):

    #为了便于在View中展示，增加了category外键，属于冗余
    category = models.PositiveIntegerField(default=0, verbose_name="产品类型")
    name = models.CharField(max_length=200, verbose_name="商品名称")
    designer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='designers', verbose_name="设计师")
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, verbose_name="设计描述")
    base_product = models.ForeignKey(BaseProduct, related_name='products', verbose_name="基础产品")

    #为程序方便，BaseProduct和Product的价格都是price，设计师直接给出加价后的价格，但是不能小于BaseProduct的价格
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name="设计师价格")
    discount = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="折扣")
    available = models.BooleanField(default=True, verbose_name="在售？")
    created = models.DateTimeField(auto_now=True, verbose_name="上传时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    # 设计师生成的产品。attribute主要是前后左右的图片
    image_front = models.ImageField('正面图片',
                                upload_to=front_design_image,
                                null=True,
                                blank=True)
    image_back = models.ImageField('背面图片',
                                upload_to=back_design_image,
                                null=True,
                                blank=True)
    image_back_available = models.BooleanField(default=False, verbose_name="有背面？")
#    attribute = JSONField(verbose_name="设计师添加的属性")
    sale = models.PositiveIntegerField(verbose_name="销量")

    def save(self, *args, **kwargs):
        if not self.category:
            self.category = self.base_product.category.id
        super(Product, self).save(*args, **kwargs)


    class Meta:
        ordering = ('name',)
        verbose_name = '销售成品'
        verbose_name_plural = '销售成品'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.category, self.id, self.slug])

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


