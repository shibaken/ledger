# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-02 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0018_auto_20161201_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampsiteClassPriceHistory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('rate_id', models.IntegerField()),
                ('adult', models.DecimalField(decimal_places=2, max_digits=8)),
                ('concession', models.DecimalField(decimal_places=2, max_digits=8)),
                ('child', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'ordering': ['-date_start'],
                'db_table': 'parkstay_campsiteclass_pricehistory_v',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='campground',
            name='bookable_online',
            field=models.BooleanField(default=False),
        ),
    ]
