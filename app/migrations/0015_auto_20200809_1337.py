# Generated by Django 3.0.8 on 2020-08-09 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20200809_1337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='products',
            new_name='product',
        ),
    ]