from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from services.utils import NULLABLE


class CurrencyChoice(models.TextChoices):
    """ Валюта """
    RUB = 'RUB'
    USD = 'USD'


class Item(models.Model):
    """ Модель элемента """
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.CharField(max_length=1500, verbose_name='Описание', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена', default=0)
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoice.choices,
        verbose_name='Валюта',
        default=CurrencyChoice.RUB
    )

    def __str__(self):
        return f'Object Item: {self.name}'

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'


class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата - время создания')
    comment = models.CharField(max_length=150, verbose_name='Комментарий', **NULLABLE)
    discount = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name='Скидка',
        default=0)
    tax = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name='Налоговая ставка',
        default=0
    )
    items = models.ManyToManyField(Item, verbose_name='Элементы')

    def __str__(self):
        return f'Object Order: {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
