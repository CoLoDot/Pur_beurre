# Generated by Django 2.1.7 on 2019-04-11 13:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0023_auto_20190411_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None),
        ),
    ]
