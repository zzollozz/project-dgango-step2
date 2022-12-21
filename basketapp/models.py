from django.db import models
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)


# def total_basket(self):
#     basket_total = {
#         'quantity_products_bsket': 0,
#         'price_products_bsket': 0
#     }
#     for itm in Basket.objects.filter(user=self.user):
#         basket_total['quantity_products_bsket'] += itm.quantity
#         basket_total['price_products_bsket'] += Product.objects.get(pk=itm.product_id).price * basket_total[
#             'quantity_products_bsket']
#     return basket_total

    @property
    def product_cost(self):
        "возвратная стоимость всех продуктов этого типа"
        return self.product.price * self.quantity


    @property
    def total_quantity(self):
        " вернуть общее количество для пользователя "
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity


    @property
    def total_cost(self):
        "вернуть общую стоимость для пользователя"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost
