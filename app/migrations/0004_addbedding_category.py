# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20161014_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbedding',
            name='category',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
