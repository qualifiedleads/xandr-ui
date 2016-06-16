# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0013_auto_20160615_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteDomainPerformanceReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('site_domain', models.TextField(blank=True, db_index=True, null=True)),
                ('campaign', models.IntegerField(blank=True, db_index=True, null=True)),
                ('line_item_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('deal_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('campaign_group', models.IntegerField(blank=True, db_index=True, null=True)),
                ('buyer_member_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('operating_system_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('supply_type', models.TextField(blank=True, choices=[(b'web', b'web'), (b'mobile_app', b'mobile_app'), (b'mobile_web', b'mobile_web')], null=True)),
                ('mobile_application_id', models.TextField(blank=True, db_index=True, null=True)),
                ('mobile_application_name', models.TextField(blank=True, db_index=True, null=True)),
                ('mobile_application', models.TextField(blank=True, db_index=True, null=True)),
                ('fold_position_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('age_bucket_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('gender', models.TextField(blank=True, choices=[(b'm', b'm'), (b'f', b'f'), (b'u', b'u')], null=True)),
                ('is_remarketing', models.IntegerField(blank=True, null=True)),
                ('conversion_pixel_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('booked_revenue', models.DecimalField(decimal_places=10, max_digits=35)),
                ('clicks', models.IntegerField(blank=True, null=True)),
                ('click_thru_pct', models.FloatField(blank=True, null=True)),
                ('convs_per_mm', models.FloatField(blank=True, null=True)),
                ('convs_rate', models.FloatField(blank=True, null=True)),
                ('cost_ecpa', models.DecimalField(decimal_places=10, max_digits=35)),
                ('cost_ecpc', models.DecimalField(decimal_places=10, max_digits=35)),
                ('cpm', models.DecimalField(decimal_places=10, max_digits=35)),
                ('ctr', models.FloatField(blank=True, null=True)),
                ('imps', models.IntegerField(blank=True, null=True)),
                ('media_cost', models.DecimalField(decimal_places=10, max_digits=35)),
                ('post_click_convs', models.IntegerField(blank=True, null=True)),
                ('post_click_convs_rate', models.FloatField(blank=True, null=True)),
                ('post_view_convs', models.IntegerField(blank=True, null=True)),
                ('post_view_convs_rate', models.FloatField(blank=True, null=True)),
                ('profit', models.DecimalField(decimal_places=10, max_digits=35)),
                ('profit_ecpm', models.DecimalField(decimal_places=10, max_digits=35)),
                ('imps_viewed', models.IntegerField(blank=True, null=True)),
                ('view_measured_imps', models.IntegerField(blank=True, null=True)),
                ('view_rate', models.FloatField(blank=True, null=True)),
                ('view_measurement_rate', models.FloatField(blank=True, null=True)),
                ('advertiser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rtb.Advertiser')),
                ('second_level_category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_level_category_id', to='rtb.ContentCategory')),
                ('top_level_category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='top_level_category_id', to='rtb.ContentCategory')),
            ],
            options={
                'db_table': 'site_domain_performance_report',
            },
        ),
    ]
