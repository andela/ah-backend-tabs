# Generated by Django 2.0.7 on 2018-08-06 11:54

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20180806_1143'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='rating',
            managers=[
                ('rating', django.db.models.manager.Manager()),
            ],
        ),
    ]
