# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-11 14:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wildlifecompliance', '0107_merge_20181211_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnUserAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('what', models.TextField()),
                ('return_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_logs', to='wildlifecompliance.Return')),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-when',),
            },
        ),
    ]
