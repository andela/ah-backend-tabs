# Generated by Django 2.0.7 on 2018-08-16 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20180816_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_token',
            field=models.CharField(blank=True, max_length=800),
        ),
    ]
