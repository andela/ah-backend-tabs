# Generated by Django 2.0.7 on 2018-08-06 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20180806_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='ratings',
        ),
    ]
