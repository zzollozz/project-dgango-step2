from django import template
from django.conf import settings

register = template.Library()

def media_folder_products(path_to_folder):
    """ Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg """

    if not path_to_folder:
        path_to_folder = 'products_images/default.jpg'
    return f'{settings.MEDIA_URL}{path_to_folder}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    """ Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg """
    if not string:
        string = 'users_avatars/default.jpg'
    return f'{settings.MEDIA_URL}{string}'

# Зарегистрировали их в библиотеке фильтров
register.filter('media_folder_products', media_folder_products)

