from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Category, BaseProduct, Product


def category_list(request):
    return render(request, "shop/category_list.html",
                              {'nodes': Category.objects.all()})


'''
class CategoryList(ListView):
    model = Category
    template_name = "category_list.html"
'''

def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        #由于设计师product表的category不是Category表的外键，所以不能直接categrory=category
        products = products.filter(category=category.id)


    return render(request, "shop/product_list.html",
                  {'category': category,
                    'nodes': categories,
                   'products': products,})

'''
class ProductList(ListView):
    model = DesignProduct
    template_name = "shop/product_list.html"
'''

def product_detail(request, category_id, id, slug):

    categories = Category.objects.all()

    category = get_object_or_404(Category, pk=category_id)
        #由于设计师product表的category不是Category表的外键，所以不能直接categrory=category


    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
#    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product_detail.html',
                  {'product': product,
                  'nodes': categories,
                  'category': category})
#                   'cart_product_form': cart_product_form})