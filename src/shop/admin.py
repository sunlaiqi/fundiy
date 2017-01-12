from django.contrib import admin

# Register your models here.
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Catalog, Category, ProductAttribute, Product, ProductReview

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

class ProductAdmin(MPTTModelAdmin):
    list_display = ['name', 'owner', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['parent', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', 'owner')}

#admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'description']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'review', 'rating']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ProductReview, ProductReviewAdmin)