# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-19 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0022_auto_20160619_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertiser',
            name='fetch_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='fetch_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
