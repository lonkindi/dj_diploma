from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.FileField(upload_to='products/%Y/%m/%d/')
    inf = models.TextField()
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Section(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'


class Article(models.Model):
    caption = models.CharField(max_length=150)
    text = models.TextField()
    product = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Order(models.Model):
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Review(models.Model):
    name = models.CharField(max_length=100, verbose_name='Пользователь')
    text = models.TextField()
    rating = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} про {self.product.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
