# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2025-02-05 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0037_oracleinterfacesystem_invoice_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='abn',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
