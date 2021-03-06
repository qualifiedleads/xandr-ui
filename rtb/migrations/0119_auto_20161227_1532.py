# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0118_auto_20161212_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='MLDecisionTreeClassifierResults',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.IntegerField(db_index=True)),
                ('test_number', models.IntegerField(db_index=True, null=True)),
                ('expert_decision', models.NullBooleanField(db_index=True)),
                ('good', models.NullBooleanField()),
                ('placement', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='rtb.Placement')),
            ],
            options={
                'db_table': 'ml_decision_tree_classifier_results',
            },
        ),
        migrations.AlterUniqueTogether(
            name='mldecisiontreeclassifierresults',
            unique_together=set([('placement', 'day', 'test_number')]),
        ),
    ]
