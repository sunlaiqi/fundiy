from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """
        初始化购物车

        :param request: request里面包含了session信息
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 在session里保存一个空的购物车
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        向购物车里添加一个产品或者更新其数量
        :param product:
        :param quantity:
        :param update_quantity:
        :return:
        """
        # Django使用JSON序列化session的数据，因此，需要把product id转换成字符串
        # 因为JSON只允许字符串为key名。对产品价格，是同理
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # 更新 session中的购物车
        self.session[settings.CART_SESSION_ID] = self.cart
        # 将session标记为modified以保证其被保存
        self.session.modified = True

    def remove(self, product):
        """
        从购物车中删除某个产品
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        遍历在购物车中的所有条目，并从数据库中获得相应的产品信息
        :return:
        """
        product_ids = self.cart.keys()
        # 获取产品对象并将他们添加到购物车
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        计算购物车中条目的总数
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # 将购物车从session中删除
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
