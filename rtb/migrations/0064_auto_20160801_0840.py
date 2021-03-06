# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 08:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0063_auto_20160726_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkAnalyticsReport_ByPlacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('imps', models.IntegerField(blank=True, null=True)),
                ('clicks', models.IntegerField(blank=True, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=10, max_digits=35, null=True)),
                ('total_convs', models.IntegerField(blank=True, null=True)),
                ('campaign', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Campaign')),
                ('placement', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Placement')),
                ('seller_member', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.PlatformMember')),
            ],
            options={
                'db_table': 'network_analytics_report_by_placement',
            },
        ),
        migrations.AlterIndexTogether(
            name='networkanalyticsreport_byplacement',
            index_together=set([('campaign', 'hour')]),
        ),
    ]
