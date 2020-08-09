from datetime import datetime

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Товар')
    photo = models.FileField(upload_to='products/%Y/%m/%d/', verbose_name='Фотография')
    inf = models.TextField(verbose_name='Описание товара')
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

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
    date = models.DateTimeField(verbose_name='Дата', default=datetime.now())
    caption = models.CharField(max_length=150, verbose_name='Статья')
    text = models.TextField(verbose_name='Текст статьи')
    product = models.ManyToManyField(Product, through='ArticleRelation')

    def __str__(self):
        return f'{self.caption}'

    class Meta:
        verbose_name = 'Статья о товаре'
        verbose_name_plural = 'Статьи о товаре'
        ordering = ["-date", ]

class ArticleRelation(models.Model):
    # pub_date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')

    class Meta:
        verbose_name = 'Товар в статье'
        verbose_name_plural = 'Товары в статье'




class Order(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    product = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    session = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} про {self.product.name}'

    class Meta:
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товаре'
