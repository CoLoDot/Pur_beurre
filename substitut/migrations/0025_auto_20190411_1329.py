# Generated by Django 2.1.7 on 2019-04-11 13:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0024_auto_20190411_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=900), blank=True, size=None),
        ),
    ]