from django.contrib import admin

# Register your models here.
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Catalog, Category, BaseProduct, ProductAttribute, Product, ProductReview

class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


#admin.site.unregister(Catalog)
admin.site.register(Catalog, CatalogAdmin)

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

#admin.site.unregister(Category)
admin.site.register(Category, CategoryAdmin)

class BaseProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'maker', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

#admin.site.unregister(Product)
admin.site.register(BaseProduct, BaseProductAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'description']

admin.site.register(ProductAttribute, ProductAttributeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'designer', 'image_front', 'price', 'available']
    list_filter = ['designer', 'available']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'review', 'rating']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ProductReview, ProductReviewAdmin)