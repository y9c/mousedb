# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 04:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mouse',
            name='injectvirus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.InjectVirus'),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='breed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Breed'),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='feed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Feed'),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='genotype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Genotype'),
        ),
        migrations.AlterField(
            model_name='mouse',
            name='phenotype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Phenotype'),
        ),
    ]