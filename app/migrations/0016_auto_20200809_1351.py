# Generated by Django 3.0.8 on 2020-08-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200809_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlerelation',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]
