# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 18:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0002_auto_20160405_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 5, 2, 28, 13, 496208), verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='novel',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 5, 2, 28, 26, 672290), verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]
