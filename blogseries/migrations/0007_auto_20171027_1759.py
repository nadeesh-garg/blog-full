# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogseries', '0006_auto_20171017_0421'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContentImages',
        ),
        migrations.AlterField(
            model_name='blog',
            name='welcome_image',
            field=models.ImageField(blank=True, upload_to='blog_welcome'),
        ),
    ]
