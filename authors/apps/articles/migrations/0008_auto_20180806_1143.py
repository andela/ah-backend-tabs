# Generated by Django 2.0.7 on 2018-08-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='amount',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]