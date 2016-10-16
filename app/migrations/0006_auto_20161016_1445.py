# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161016_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='get_genotype',
            name='litter',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='get_genotype',
            name='mate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Mate'),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='status',
            field=models.IntegerField(choices=[(0, 'idle'), (1, 'suckling'), (2, 'mating'), (3, 'lactating'), (4, 'dead')], default=0),
        ),
    ]
