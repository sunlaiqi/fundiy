from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
from . import views
# to make home point to product_list
from orders.views import order_create
from shop.views import product_list

urlpatterns = [
    # 让主页指向产品列表
    url(r'^$', product_list, name='home'),
    # make sure include cart.urls before shop.urls
    url(r'^cart/', include('cart.urls', namespace='cart')),
    # make sure inlcude orders.urls before shop.urls
    url(r'^order/', include('orders.urls', namespace='orders')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^', include(accounts.urls, namespace='accounts')),

]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
