from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now
from datetime import timedelta

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватар')
    age = models.PositiveIntegerField(verbose_name='возраст')


    # ключ подтверждения --> activation_key будем создавать с помощью хеш-функции при регистрации пользователя.
    activation_key = models.CharField(max_length=128, blank=True)
    # Срок действия ключа --> activation_key_expires
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    def is_activation_key_expires(self):
        # выполняет проверку актуальности ключа.
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
