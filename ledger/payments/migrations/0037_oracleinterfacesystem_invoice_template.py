# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2025-02-04 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0036_auto_20241107_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracleinterfacesystem',
            name='invoice_template',
            field=models.CharField(blank=True, choices=[('dbca_default', 'DBCA Default'), ('ria', 'RIA')], default='dbca_default', max_length=20, null=True),
        ),
    ]
