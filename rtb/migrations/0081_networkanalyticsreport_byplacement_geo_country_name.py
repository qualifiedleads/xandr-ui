# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0080_add_indexes_amend_types_20160828_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkanalyticsreport_byplacement',
            name='geo_country_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
