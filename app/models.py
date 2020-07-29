from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.FileField(upload_to='products/%Y/%m/%d/')
    inf = models.TextField()
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Section(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Article(models.Model):
    caption = models.CharField(max_length=150)
    text = models.TextField()
    product = models.ManyToManyField(Product)


class Order(models.Model):
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
