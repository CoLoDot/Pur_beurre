# Generated by Django 2.1.7 on 2019-03-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0012_auto_20190329_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saving',
            name='saved_product_key',
            field=models.CharField(max_length=100),
        ),
    ]
