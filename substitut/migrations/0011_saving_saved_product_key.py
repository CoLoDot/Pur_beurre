# Generated by Django 2.1.7 on 2019-03-29 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0010_saving'),
    ]

    operations = [
        migrations.AddField(
            model_name='saving',
            name='saved_product_key',
            field=models.IntegerField(default=9),
        ),
    ]