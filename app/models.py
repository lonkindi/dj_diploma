from datetime import datetime

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Товар')
    photo = models.FileField(upload_to='products/%Y/%m/%d/', verbose_name='Фотография')
    inf = RichTextField(verbose_name='Описание товара')
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Section(MPTTModel):
    name = models.CharField(max_length=50, verbose_name='Товарная секция')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товарная секция'
        verbose_name_plural = 'Товарные секции'


class Article(models.Model):
    date = models.DateTimeField(verbose_name='Дата', default=datetime.now)
    caption = models.CharField(max_length=150, verbose_name='Статья')
    text = RichTextField(verbose_name='Текст статьи')
    product = models.ManyToManyField(Product, through='ArticleRelation')

    def __str__(self):
        return f'{self.caption}'

    class Meta:
        verbose_name = 'Статья о товаре'
        verbose_name_plural = 'Статьи о товаре'
        ordering = ["-date", ]


class ArticleRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')

    class Meta:
        verbose_name = 'Товар в статье'
        verbose_name_plural = 'Товары в статье'


class Order(models.Model):
    date = models.DateTimeField(verbose_name='Дата заказа', default=datetime.now)
    user = models.CharField(max_length=50, verbose_name='Пользователь')
    number = models.PositiveIntegerField(verbose_name='Номер заказа')
    product = models.ManyToManyField(Product, through='OrderRelation')

    def __str__(self):
        return f'{self.date} *** {self.user}'

    def product_count(self):
        return OrderRelation.objects.filter(order=self).count()

    @property
    def total_price(self):
        order_positions = OrderRelation.objects.filter(order=self)
        total_summ = 0
        for position in order_positions:
            total_summ += position.product.price * position.quantity
        return total_summ

    product_count.short_description = 'Товаров в заказе'
    total_price.fget.short_description = 'Сумма заказа'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ["-date", ]


class OrderRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'Цена: {self.product.price} руб.'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Review(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} про {self.product.name}'

    class Meta:
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товаре'
