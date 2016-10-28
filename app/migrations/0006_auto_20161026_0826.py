# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161026_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='breed',
            name='litter_alive',
            field=models.IntegerField(blank=True, null=True, verbose_name='number of pups alive'),
        ),
        migrations.AddField(
            model_name='breed',
            name='litter_dead',
            field=models.IntegerField(blank=True, null=True, verbose_name='number of pups dead'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='litter_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='total number of pups'),
        ),
    ]