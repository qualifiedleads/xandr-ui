# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-24 15:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0145_auto_20170224_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='UIUsualCampaignsGraph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField(db_index=True)),
                ('evaluation_date', models.DateTimeField(db_index=True)),
                ('window_start_date', models.DateTimeField(db_index=True)),
                ('day_chart', django.contrib.postgres.fields.jsonb.JSONField(default=[], null=True)),
                ('advertiser', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Advertiser')),
            ],
            options={
                'db_table': 'ui_usual_advertisers_graph',
            },
        ),
        migrations.AlterUniqueTogether(
            name='uiusualcampaignsgraph',
            unique_together=set([('advertiser', 'type')]),
        ),
    ]