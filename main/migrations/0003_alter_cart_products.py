# Generated by Django 4.0.4 on 2022-12-20 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_cartproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart_products', to='main.cartproduct'),
        ),
    ]
