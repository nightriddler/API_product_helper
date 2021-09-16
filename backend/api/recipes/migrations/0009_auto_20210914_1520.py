# Generated by Django 3.2.7 on 2021-09-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20210914_1519'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='recipe and author in shooping_cart restraint',
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'author'), name='recipe and author in Favorite restraint'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('author', 'recipe'), name='recipe and author in ShoppingCart restraint'),
        ),
    ]
