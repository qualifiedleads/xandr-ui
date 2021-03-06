# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-04 23:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0135_video_ad_hour_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='MLVideoAdCampaignsModels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.TextField()),
                ('type', models.TextField()),
                ('advertiser', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Advertiser')),
                ('campaign', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Campaign', unique=True)),
            ],
            options={
                'db_table': 'ml_video_ad_campaigns_models',
            },
        ),
        migrations.CreateModel(
            name='MLVideoAdCampaignsModelsInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField(db_index=True)),
                ('finish', models.DateTimeField(db_index=True)),
                ('evaluation_date', models.DateField(db_index=True)),
                ('path', models.TextField()),
                ('type', models.TextField()),
                ('score', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('campaign', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Campaign')),
            ],
            options={
                'db_table': 'ml_video_ad_campaigns_models_info',
            },
        ),
        migrations.CreateModel(
            name='MLVideoAdCampaignsResults',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('fill_rate', models.DecimalField(decimal_places=10, max_digits=35)),
                ('cpm', models.DecimalField(decimal_places=10, max_digits=35)),
                ('profit_loss', models.DecimalField(decimal_places=10, max_digits=35)),
                ('advertiser', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Advertiser')),
                ('campaign', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Campaign')),
            ],
            options={
                'db_table': 'ml_video_ad_campaigns_results',
            },
        ),
        migrations.CreateModel(
            name='MLVideoImpsTracker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('CpId', models.IntegerField(blank=True, db_index=True, null=True)),
                ('AdvId', models.IntegerField(blank=True, db_index=True, null=True)),
                ('CreativeId', models.IntegerField(blank=True, null=True)),
                ('AuctionId', models.BigIntegerField(blank=True, null=True)),
                ('Date', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('LocationsOrigins', models.TextField(blank=True, null=True)),
                ('UserCountry', models.TextField(blank=True, null=True)),
                ('SessionFreq', models.TextField(blank=True, null=True)),
                ('PricePaid', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('AdvFreq', models.TextField(blank=True, null=True)),
                ('UserState', models.TextField(blank=True, null=True)),
                ('CpgId', models.IntegerField(blank=True, null=True)),
                ('CustomModelLastModified', models.TextField(blank=True, null=True)),
                ('UserId', models.BigIntegerField(blank=True, null=True)),
                ('XRealIp', models.TextField(blank=True, null=True)),
                ('BidPrice', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('SegIds', models.IntegerField(blank=True, null=True)),
                ('UserAgent', models.TextField(blank=True, null=True)),
                ('RemUser', models.IntegerField(blank=True, null=True)),
                ('UserCity', models.TextField(blank=True, null=True)),
                ('Age', models.IntegerField(blank=True, null=True)),
                ('ReservePrice', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('CacheBuster', models.IntegerField(blank=True, null=True)),
                ('Ecp', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('CustomModelId', models.IntegerField(blank=True, null=True)),
                ('PlacementId', models.IntegerField(blank=True, db_index=True, null=True)),
                ('SeqCodes', models.TextField(blank=True, null=True)),
                ('CustomModelLeafName', models.TextField(blank=True, null=True)),
                ('XForwardedFor', models.TextField(blank=True, null=True)),
                ('cpvm', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('is_imp', models.BooleanField(db_index=True)),
            ],
            options={
                'db_table': 'ml_video_imps_tracker',
            },
        ),
        migrations.CreateModel(
            name='VideoAdPlacements',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(db_index=True)),
                ('hour', models.DateTimeField(db_index=True, null=True)),
                ('imp_hour', models.IntegerField(null=True)),
                ('ad_starts_hour', models.IntegerField(null=True)),
                ('spent_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('cpm_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('spent_cpm_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('bid_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('cpvm_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('spent_cpvm_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('fill_rate_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('profit_loss_hour', models.DecimalField(decimal_places=10, max_digits=35, null=True)),
                ('campaign', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Campaign')),
                ('placement', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Placement')),
            ],
            options={
                'db_table': 'video_ad_placements',
            },
        ),
        migrations.AlterUniqueTogether(
            name='mlvideoadcampaignsmodelsinfo',
            unique_together=set([('campaign', 'type')]),
        ),
    ]
