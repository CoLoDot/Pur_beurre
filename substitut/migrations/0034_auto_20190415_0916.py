# Generated by Django 2.1.7 on 2019-04-15 09:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0033_auto_20190415_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=1000), size=None), default=list, size=1),
        ),
    ]
