# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 05:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bBlock', '0002_auto_20160328_1620'),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AddField(
            model_name='article',
            name='block',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bBlock.bBlock', verbose_name='版块'),
            preserve_default=False,
        ),
    ]