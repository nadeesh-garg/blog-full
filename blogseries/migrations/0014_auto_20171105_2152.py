# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 21:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogseries', '0013_auto_20171104_2037'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tagulous_Series_tags',
        ),
        migrations.RemoveField(
            model_name='series',
            name='tags',
        ),
    ]
