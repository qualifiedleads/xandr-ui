# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 04:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('rtb', '0050_auto_20160712_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adprofilebrand',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='advertiserbrand',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='brandincountry',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='creative',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='creativecompetitivebrand',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='dealbrand',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='memberbrandexception',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='networkanalyticsreport',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='publisherbrandexceptions',
            name='brand',
        ),
    ]
