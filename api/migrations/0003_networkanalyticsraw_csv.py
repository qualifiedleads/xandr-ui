# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160606_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkanalyticsraw',
            name='csv',
            field=models.TextField(blank=True, null=True),
        ),
    ]
