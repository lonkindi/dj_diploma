# Generated by Django 3.0.8 on 2020-08-09 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200804_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default='2020-08-09', verbose_name='Дата'),
            preserve_default=False,
        ),
    ]