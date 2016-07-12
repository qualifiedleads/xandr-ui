# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0047_language_fetch_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creative',
            name='first_run',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='creative',
            name='last_run',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='creative',
            name='sla_eta',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
