from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.models import User
import json, os

JSON_PATH = 'mainapp/json'

def load_from_json(name_file):
    with open(os.path.join(JSON_PATH, name_file + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ Метод обновления данных в базе новыми данными """

        ProductCategory.objects.all().delete()
        categories = load_from_json('categories')
        """
        !!! В Н И М А Н И Е данные в базу добавляем Пакетной встакой !!!
        """
        categories_batch = []  # список Для пакетной вставки в базу
        for cat in categories:
            categories_batch.append(ProductCategory(
                name=cat.get('name'),
                description=cat.get('description')
                )
            )
        ProductCategory.objects.bulk_create(categories_batch)  # bulk_create <= Пакетная Вставка списка в базу

        products = load_from_json('products')
        Product.objects.all().delete()

        products_batch = []
        for product in products:
            category_name = product["category"]

            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)  # Заменяем название категории объектом
            print(_category)
            product['category'] = _category
            products_batch.append(Product(**product))   # **product <- значит указать (распоковать) все Поля

        Product.objects.bulk_create(products_batch)

            # new_product = Product(**product)
            # new_product.save()



        # Создаем суперпользователя при помощи менеджера модели
        super_user = ShopUser.objects.create_superuser('admin', 'admin@gb.com', '12345', age=43)
