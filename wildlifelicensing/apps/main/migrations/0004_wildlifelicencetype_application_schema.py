# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 03:49
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wl_main', '0003_communicationslogentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildlifelicencetype',
            name='application_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
