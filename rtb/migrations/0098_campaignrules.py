# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-31 08:09
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0097_merge_20161026_0706'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignRules',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rules', django.contrib.postgres.fields.jsonb.JSONField()),
                ('campaign', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Campaign')),
            ],
            options={
                'db_table': 'campaign_rules',
            },
        ),
    ]
