# Generated by Django 2.1.5 on 2019-03-26 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('substitut', '0003_auto_20190325_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='ownedproducts',
            name='email',
        ),
        migrations.AddField(
            model_name='ownedproducts',
            name='contact',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='substitut.Users'),
        ),
        migrations.RemoveField(
            model_name='ownedproducts',
            name='product',
        ),
        migrations.AddField(
            model_name='ownedproducts',
            name='product',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='substitut.Products'),
        ),
    ]
