# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0019_auto_20160705_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkanalyticsreport',
            name='bid_type',
            field=models.TextField(blank=True, choices=[(b'Manual', b'Manual'), (b'Learn', b'Learn'), (b'Optimized', b'Optimized'), (b'Unknown', b'Unknown'), (b'Optimized give up', b'Optimized give up'), (b'Learn give up', b'Learn give up'), (b'Manual give up', b'Manual give up')], null=True),
        ),
        migrations.AlterField(
            model_name='networkanalyticsreport',
            name='buyer_type',
            field=models.TextField(blank=True, choices=[(b'1', b'Blank'), (b'2', b'PSA'), (b'3', b'Default Error'), (b'4', b'Default'), (b'5', b'Kept'), (b'6', b'Resold'), (b'7', b'RTB'), (b'8', b'PSA Error'), (b'9', b'External Impression'), (b'10', b'External Click'), (b'11', b'Insertion')], null=True),
        ),
        migrations.AlterField(
            model_name='networkanalyticsreport',
            name='imp_type_id',
            field=models.IntegerField(blank=True, choices=[(b'Manual', b'Manual'), (b'Learn', b'Learn'), (b'Optimized', b'Optimized'), (b'Unknown', b'Unknown'), (b'Optimized give up', b'Optimized give up'), (b'Learn give up', b'Learn give up'), (b'Manual give up', b'Manual give up')], null=True),
        ),
        migrations.AlterField(
            model_name='networkanalyticsreport',
            name='revenue_type_id',
            field=models.IntegerField(blank=True, choices=[(b'-1', b'No Payment'), (b'0', b'Flat CPM'), (b'1', b'Cost Plus CPM'), (b'2', b'Cost Plus Margin'), (b'3', b'CPC'), (b'4', b'CPA'), (b'5', b'Revshare'), (b'9', b'CPVM')], null=True),
        ),
    ]