# Generated by Django 2.0.7 on 2018-07-31 12:32

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20180731_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
