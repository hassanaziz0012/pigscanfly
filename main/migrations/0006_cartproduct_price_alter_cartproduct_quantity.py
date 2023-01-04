# Generated by Django 4.0.4 on 2022-12-20 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='quantity',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
