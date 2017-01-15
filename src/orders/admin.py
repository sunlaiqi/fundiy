from django.contrib import admin
from .models import Country, Province, City, County, Order, OrderItem

# Register your models here.

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Country, CountryAdmin)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Province, ProvinceAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(City, CityAdmin)

class CountyAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(County, CountyAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'country', 'province', 'city',
                    'county', 'address', 'postal_code',
                    'paid', 'received', 'created', 'updated']
    list_filter = ['paid', 'received', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)