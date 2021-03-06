# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-12 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0116_auto_20161204_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='RtbClickTracker',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('CpId', models.TextField(blank=True, null=True)),
                ('AdvId', models.TextField(blank=True, null=True)),
                ('CreativeId', models.TextField(blank=True, null=True)),
                ('AuctionId', models.TextField(blank=True, null=True)),
                ('Date', models.DateTimeField(blank=True, db_index=True, null=True)),
            ],
            options={
                'db_table': 'rtb_click_tracker',
            },
        ),
        migrations.CreateModel(
            name='RtbConversionTracker',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('CpId', models.TextField(blank=True, null=True)),
                ('AdvId', models.TextField(blank=True, null=True)),
                ('CreativeId', models.TextField(blank=True, null=True)),
                ('AuctionId', models.TextField(blank=True, null=True)),
                ('Date', models.DateTimeField(blank=True, db_index=True, null=True)),
            ],
            options={
                'db_table': 'rtb_conversion_tracker',
            },
        ),
    ]
