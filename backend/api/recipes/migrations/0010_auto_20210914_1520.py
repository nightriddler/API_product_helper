# Generated by Django 3.2.7 on 2021-09-14 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_auto_20210914_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppings', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppings', to='recipes.recipe', verbose_name='Рецепт для списка покупок'),
        ),
    ]