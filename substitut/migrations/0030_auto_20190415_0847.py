# Generated by Django 2.1.7 on 2019-04-15 08:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0029_auto_20190415_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=900), default=list, null=True, size=30),
        ),
    ]
