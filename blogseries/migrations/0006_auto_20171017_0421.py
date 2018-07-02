# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogseries', '0005_auto_20171015_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='media')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='welcome_image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]
