# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 04:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('rtb', '0062_auto_20160725_1756'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membershipusertoadvertiser',
            unique_together=set([('advertiser', 'frameworkuser')]),
        ),
    ]
