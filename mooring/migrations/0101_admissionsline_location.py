# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-14 05:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0100_admissionslocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionsline',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mooring.AdmissionsLocation'),
            preserve_default=False,
        ),
    ]
