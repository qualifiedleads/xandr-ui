# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0035_auto_20160620_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='first_run',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='last_run',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]