#!/bin/env python
import csv
import datetime
import time
import decimal
import gc
import json
from trace import Trace

import os
import sys
import traceback
from itertools import imap, izip, islice, ifilter
from multiprocessing.pool import ThreadPool, Pool
from django.db.models import Avg, Count, Sum, Max
import django.db.models as django_types
from django.db import transaction, IntegrityError, reset_queries, connection
import re
from report import nexus_get_objects, replace_tzinfo, update_object_from_dict, date_type, get_auth_token, \
    get_specified_report, nexus_get_objects_by_id
from django.conf import settings
import models
from models import Advertiser, Campaign, SiteDomainPerformanceReport, Profile, LineItem, InsertionOrder, \
    OSFamily, OperatingSystemExtended, NetworkAnalyticsReport, GeoAnaliticsReport, Member, Developer, BuyerGroup, \
    AdProfile, ContentCategory, Deal, PlatformMember, User, Publisher, Site, OptimizationZone, MobileAppInstance, \
    YieldManagementProfile, PaymentRule, ConversionPixel, Country, Region, DemographicArea, AdQualityRule, Placement, \
    Creative, Brand, CreativeTemplate, Category, Company, MediaType, MediaSubType, CreativeFormat, CreativeFolder, \
    Language
from pytz import utc
from utils import get_all_classes_in_models, column_sets_for_reports, get_current_time, clean_old_files

table_names = {c._meta.db_table: c for c in get_all_classes_in_models(models)}

_default_values_for_types = {
    django_types.DateField: datetime.date.today,
    # django_types.related.ForeignObject: None,
    django_types.BigIntegerField: 0,
    django_types.IntegerField: 0,
    django_types.PositiveIntegerField: 1,
    django_types.GenericIPAddressField: '127.0.0.1',
    django_types.CharField: '',
    django_types.DurationField: datetime.timedelta(0),
    django_types.TextField: '',
    django_types.BooleanField: False,
    django_types.DecimalField: decimal.Decimal(0),
    django_types.DateTimeField: get_current_time,
    django_types.SmallIntegerField: 0,
    django_types.IPAddressField: '127.0.0.1',
    django_types.SlugField: '',
    django_types.TimeField: lambda: get_current_time().timetz(),
    # django_types.proxy.OrderWrt: 0,
    django_types.CommaSeparatedIntegerField: '0',
    # django_types.AutoField: None,
    django_types.URLField: 'www.example.com',
    # django_types.files.ImageField: '',
    django_types.EmailField: 'admin@www.example.com',
    django_types.FloatField: 0.0,
    django_types.Field: '',
    # django_types.related.ManyToManyField: None,
    # django_types.related.OneToOneField: None,
    # django_types.related.ForeignKey: None,
    django_types.NullBooleanField: None,
    django_types.UUIDField: '00000000-0000-0000-0000-000000000000',
    django_types.BinaryField: '',
    django_types.PositiveSmallIntegerField: 1,
    # django_types.files.FileField: '',
    django_types.FilePathField: '/tmp',
}


def fill_null_values(o):
    for field in o._meta.fields:
        if not field.null and not field.primary_key:
            val = field.get_default()
            # t = field.get_internal_type
            if val is None:
                val = _default_values_for_types.get(type(field))
                if hasattr(val, '__call__'):
                    val = val()
            setattr(o, field.name, val)


def try_resolve_foreign_key(objects, dicts, e):
    if e.message.find('foreign key constraint') < 0:
        return False
    m = re.search(
        r'Key \((\w+)\)=\(([^\)]+)\) is not present in table "([^\"]+)"',
        e.message)
    if not m:
        return False
    key_field, key_value, table_name = m.groups()
    try:
        objectClass = table_names[table_name]
        o = objectClass()
        o.pk = key_value
        cd = get_current_time()
        name = 'Unknown, autocreated at %s' % cd
        if key_field.endswith('_id'):
            first = list(
                islice(
                    ifilter(
                        lambda x: str(
                            getattr(
                                x[1],
                                key_field)) == key_value,
                        enumerate(objects)),
                    0,
                    1))
            if first:
                new_name = dicts[first[0][0]].get(
                    key_field[:-2] + 'name', '--')
                if new_name != '--':
                    name = new_name
        if hasattr(o, 'name'):
            o.name = name
        if hasattr(o, 'fetch_date'):
            o.fetch_date = cd
        fill_null_values(o)
        o.save()
    except Exception as e:
        print "Failed try_resolve_foreign_key...", e
        return False
    return True


_create_execute_context_ = {
    # 'all_fields':None,
    # 'need_filter_fields':None,
    # 'foreign_fields':None,
    # 'nullable_keys':None,
    # 'float_keys':None,
    # 'modelClass':None,
    # 'time_fields':None,
    # 'fetch_date':None,
}


def context_initializer(context):
    global _create_execute_context_
    _create_execute_context_ = context


def create_object_from_dict(data_row):
    try:
        data = {k: data_row[k] for k in _create_execute_context_['all_fields']} \
            if _create_execute_context_['need_filter_fields'] else data_row
        for k in _create_execute_context_['foreign_fields']:
            try:
                data[k] = int(data.get(k))
            except:
                data[k] = None
        for k in _create_execute_context_['nullable_keys']:
            val = data.get(k)
            if val[:2] == '--' or val == 'Undisclosed':
                data[k] = None
        for k in _create_execute_context_['float_keys']:
            s = str(data.get(k, ''))
            if s.endswith('%'):
                data[k] = s[:-1]
        modelClass = _create_execute_context_['modelClass']
        try:
            c = modelClass(**data)
            replace_tzinfo(c, _create_execute_context_['time_fields'])
        except:
            c = modelClass()
            update_object_from_dict(
                c, data, _create_execute_context_['time_fields'])
        c.fetch_date = _create_execute_context_['fetch_date']
        if hasattr(c, 'TransformFields'):
            c.TransformFields(data_row, _create_execute_context_)
        return c
    except Exception as e:
        print "Interest error", e
        return None


def get_all_class_fields(modelClass):
    return [
        field.name +
        '_id' if isinstance(
            field,
            django_types.ForeignObject) else field.name for field in modelClass._meta.fields]


def test_foreign_keys(objects_to_save, rows):
    if not objects_to_save:
        return
    token = get_auth_token()
    first = objects_to_save[0]
    foreign_keys = {x.name: x for x in first._meta.fields if isinstance(x, django_types.ForeignKey)}
    for k in foreign_keys:
        key_id = k + '_id'
        entity = foreign_keys[k].related_model
        ids = set(imap(lambda x: getattr(x, key_id), objects_to_save))
        ids.discard(None)
        if 0 in ids:
            for x in objects_to_save:
                if getattr(x, key_id) == 0:
                    setattr(x, key_id, None)
            ids.discard(0)
        ids_in_db = set(entity.objects.filter(pk__in=ids).values_list('pk', flat=True))
        ids_to_load = ids - ids_in_db
        if not ids_to_load:continue
        saved = nexus_get_objects_by_id(token,entity,ids_to_load)
        if len(saved)!=len(ids_to_load):
            print "Auto-fetch of depended rows in %s completed partially"%entity
            print "%d rows saved (to save: %d)"%(len(saved),len(ids_to_load))
        ids_to_load -= saved
        if ids_to_load:
            # manual create of objects
            print 'Some objects will created as stubs'
            key_name= k + '_name'
            try:
                f=entity._meta.get_field('name')
            except:
                f=None
            if f:
                if key_name in rows[0]:

                    ids_dict={int(x[key_id]):x[key_name] for x in rows
                                   if int(x[key_id]) in ids_to_load}
                    ids_and_names= [{'id': x[0], 'name':x[1]} for x in ids_dict.items()]
                else:
                    ids_and_names = [{'id': x, 'name': 'Automatically created object %d'%x} for x in ids_to_load]
            else:
                ids_and_names = [{'id': x} for x in ids_to_load]
            for obj_dict in ids_and_names:
                obj=entity(**obj_dict)
                if hasattr(obj,'last_modifed'):
                    obj.last_modifed = get_current_time()
                if hasattr(obj, 'fetch_date'):
                    obj.fetch_date = get_current_time()
                obj.save()


def analize_csv(filename, modelClass, metadata={}):
    with open(filename, 'r') as csvFile:
        # dialect='excel-tab' or excel ?
        reader = csv.DictReader(csvFile, delimiter=',')
        print 'Begin analyzing csv file ...'
        # result = []
        context = {}
        context['modelClass'] = modelClass
        context['fetch_date'] = get_current_time()
        class_fields = set(get_all_class_fields(modelClass))
        csv_fields = set(reader.fieldnames)
        context['all_fields'] = class_fields & csv_fields
        context['need_filter_fields'] = bool(
            csv_fields -
            class_fields) and modelClass.api_report_name not in column_sets_for_reports
        context['time_fields'] = [
            field.name for field in modelClass._meta.fields if date_type(field)]
        context['nullable_keys'] = [
            field.name for field in modelClass._meta.fields if field.null and not isinstance(
                field, (django_types.CharField, django_types.TextField)) and field.name in csv_fields]
        context['float_keys'] = [
            field.name for field in modelClass._meta.fields if isinstance(
                field, (django_types.FloatField, django_types.DecimalField))]
        foreign_fields = [
            field.name +
            '_id' for field in modelClass._meta.fields if isinstance(
                field,
                django_types.ForeignObject)]
        context['foreign_fields'] = filter(
            lambda x: x in csv_fields, foreign_fields)
        context.update(metadata)
        worker = Pool(
            initializer=context_initializer, initargs=(
                context,), maxtasksperchild=100000)
        counter = 0
        reset_queries()
        try:
            while True:
                rows = list(islice(reader, 0, 4000))
                if not rows:
                    break
                if len(rows) > 100:
                    objects_to_save = worker.map(create_object_from_dict, rows)
                else:
                    context_initializer(context)
                    objects_to_save = map(create_object_from_dict, rows)
                if len(rows) != len(objects_to_save):
                    print "There are error in multithreaded map"
                if not all(objects_to_save):
                    print "There are error objects"
                objects_saved = False
                errors = 0
                while not objects_saved:
                    try:
                        modelClass.objects.bulk_create(objects_to_save)
                        objects_saved = True
                    except IntegrityError as e:
                        errors += 1
                        if errors > 3:
                            print '---------------------------------------------------'
                            print "Continue errors", errors
                            print '---------------------------------------------------'
                        if errors > 10:
                            print 'Too many DB integrity errors'
                            print e
                            raise
                        test_foreign_keys(objects_to_save, rows)
                counter += len(objects_to_save)
                print '%d rows fetched' % counter
                print "Sql queries fired:", len(connection.queries)
                reset_queries()
                if counter % 100000 == 0:
                    gc.collect()
        except Exception as e:
            print 'Error in main loop in analize_csv', e
            print traceback.print_exc()
        finally:
            gc.collect()
            worker.close()
            worker.join()


# load data, needed for filling SiteDomainPerformanceReport
# Data saved to local DB
def load_depending_data(token):
    # nexus_get_objects\(.*?'(https://api.appnexus.com/[\w-]+)',\s*\{[^\}]*\},\s*(\w+)
    try:
        cd = get_current_time()
        with transaction.atomic():
            advertisers = nexus_get_objects(token,
                                            {"id__gt": 0},
                                            Advertiser, False, {})
            print 'There is %d advertisers' % len(advertisers)

            for adv in advertisers:
                # Get all of the profiles for the advertiser
                profiles = nexus_get_objects(token,

                                             {'advertiser_id': adv.id},
                                             Profile, False)
                print 'There is %d profiles' % len(profiles)
            # adv = Advertiser.objects.values_list('id', 'name','profile_id')
            foreign_ids = {i.profile_id: i.id for i in advertisers}
            adv_names = {i.id: i.name for i in advertisers}
            profiles_ids = set(Profile.objects.values_list('id', flat=True))
            missing_profiles = set(foreign_ids) - profiles_ids
            for i in missing_profiles:
                p = Profile(pk=i)
                fill_null_values(p)
                p.created_on = cd
                p.fetch_date = cd
                p.advertiser_id = foreign_ids[i]
                name = adv_names[foreign_ids[i]]
                p.name = 'Missed profile for %s' % name
                p.save()
                print 'Created profile "%s"' % p.name

        developers = nexus_get_objects(token,
                                       {},
                                       Developer, False)
        print 'There is %d developers ' % len(developers)
        buyer_groups = nexus_get_objects(token,
                                         {},
                                         BuyerGroup, False)
        print 'There is %d buyer groups ' % len(buyer_groups)

        # There is mutual dependence
        with transaction.atomic():
            ad_profiles = nexus_get_objects(token,
                                            {},
                                            AdProfile, False)
            print 'There is %d adware profiles ' % len(ad_profiles)
            members = nexus_get_objects(token,
                                        {},
                                        Member, False)
            print 'There is %d members ' % len(members)

        # Get all operating system families:
        operating_systems_families = nexus_get_objects(token,
                                                       {},
                                                       OSFamily, False)
        print 'There is %d operating system families' % len(operating_systems_families)

        # Get all operating systems:
        operating_systems = nexus_get_objects(token,
                                              {},
                                              OperatingSystemExtended, False)
        print 'There is %d operating systems ' % len(operating_systems)

        with transaction.atomic():
            date_in_db = ContentCategory.objects.aggregate(
                m=Max('fetch_date'))['m']
            if cd - date_in_db > settings.INVALIDATE_TIME:
                o1 = nexus_get_objects(token,
                                       {},  # {'type':'universal'}
                                       ContentCategory, True,
                                       {'category_type': 'universal'})
                o2 = nexus_get_objects(token,
                                       {},
                                       ContentCategory, True)
        print 'There is %d content categories ' % ContentCategory.objects.count()

        # Get all optimisation zones:
        optimisation_zones = nexus_get_objects(token,
                                               {},
                                               OptimizationZone, False)
        print 'There is %d optimisation zones ' % len(optimisation_zones)

        # Get all mobile app instances:
        mobile_app_instances = nexus_get_objects(token,
                                                 {},
                                                 MobileAppInstance, False)
        print 'There is %d mobile app instances ' % len(mobile_app_instances)

        with transaction.atomic():
            # Get all sites:
            sites = nexus_get_objects(token,
                                      {},
                                      Site, False)
            print 'There is %d sites ' % len(sites)
            # Get all publishers:
            publishers = nexus_get_objects(token,
                                           {"id__gt":0},
                                           Publisher, False,{})
            print 'There is %d publishers ' % len(publishers)
            # Get all yield management profiles:
            # loop ?
            yield_management_profiles = nexus_get_objects(token,
                                                          {},
                                                          YieldManagementProfile, False)
            print 'There is %d yield management profiles ' % len(yield_management_profiles)

            payment_rules_ids = set(x.base_payment_rule_id for x in publishers)
            for pub in publishers:
                print 'Publisher ', pub.name
            payment_rules = nexus_get_objects(token,
                                              {'id__in': payment_rules_ids},
                                              PaymentRule,
                                              True,
                                              # {'publisher_id': pub.pk, 'id': pub.base_payment_rule_id}
                                              {'id': ','.join(map(str, payment_rules_ids))}
                                              )
            print 'There is %d base payment rules ' % len(payment_rules)

        companies = nexus_get_objects(token,
                                      {},
                                      Company, False)
        print 'There is %d companies ' % len(companies)
        try:
            zero_company = Company.objects.get(pk=0)
        except:
            zero_company = Company(
                id=0,
                name='<Unknown company>',
                fetch_date=get_current_time())
            zero_company.save()

        categories = nexus_get_objects(token,
                                       {},
                                       Category, False)
        print 'There is %d categories ' % len(categories)
        unk_cat = Category(pk=0, name="Unknown category")
        try:
            unk_cat.save()
        except:
            pass

        brands = nexus_get_objects(token,
                                   {},
                                   Brand, False,
                                   {'simple': "true"})
        print 'There is %d brands ' % len(brands)

        media_types = nexus_get_objects(token,
                                        {},
                                        MediaType, False)
        print 'There is %d creative media types' % len(media_types)

        media_sub_types = nexus_get_objects(token,
                                            {},
                                            MediaSubType, False)
        print 'There is %d creative media sub types' % len(media_sub_types)

        # https://api.appnexus.com/creative-format
        creative_formats = nexus_get_objects(token,
                                             {},
                                             CreativeFormat, False)
        print 'There is %d creative media sub types' % len(creative_formats)

        creative_templates = nexus_get_objects(token,
                                               {},
                                               CreativeTemplate, False)
        print 'There is %d creative templates' % len(creative_templates)

        for adv in advertisers:
            advertiser_id = adv.id
            # Get all creative folders
            creative_folders = nexus_get_objects(
                token, {'advertiser_id': advertiser_id}, CreativeFolder, False)
            print 'There is %d  creative folders' % len(creative_folders)

        languages = nexus_get_objects(token,
                                      {},
                                      Language, False)
        print 'There is %d languages ' % len(languages)

        creatives = nexus_get_objects(token,
                                      {},
                                      Creative, False)
        print 'There is %d creatives ' % len(creatives)

        # Get all payment rules:
        for pub in []:  # publishers: There is too many publishers, disable loading depended objects
            payment_rules = nexus_get_objects(token,
                                              {'publisher': pub},
                                              PaymentRule, True,
                                              {'publisher_id': pub.pk})
            print 'There is %d payment rules for publisher %s' % (len(payment_rules), pub.name)
            print 'Ids:', ','.join(str(x.pk) for x in payment_rules)
            quality_rules = nexus_get_objects(token,
                                              {'publisher': pub},
                                              AdQualityRule, True,
                                              {'publisher_id': pub.pk})
            print 'There is %d quality rules for publisher %s' % (len(payment_rules), pub.name)
            # Placement
            # https://api.appnexus.com/placement?publisher_id=PUBLISHER_ID
            placements = nexus_get_objects(token,
                                           {'publisher': pub},
                                           Placement, True,
                                           {'publisher_id': pub.pk})
            print 'There is %d placements for publisher %s' % (len(placements), pub.name)

        # Get all users:
        users = nexus_get_objects(token,
                                  {},
                                  User, False)
        print 'There is %d users ' % len(users)
        # Get all platform members:
        platform_members = nexus_get_objects(token,
                                             {},
                                             PlatformMember, False)
        print 'There is %d platform members ' % len(platform_members)
        # Get all deals:
        deals = nexus_get_objects(token,
                                  {},
                                  Deal, False)
        print 'There is %d deals ' % len(deals)
        # Get all demographic areas:
        demographic_areas = nexus_get_objects(token,
                                              {},
                                              DemographicArea, False)
        print 'There is %d  demographic areas' % len(demographic_areas)
        # Get all countries:
        countries = nexus_get_objects(token,
                                      {},
                                      Country, False)
        print 'There is %d  countries' % len(countries)
        # Get all regions:
        regions = nexus_get_objects(token,
                                    {},
                                    Region, False)
        print 'There is %d  regions' % len(regions)

        for adv in advertisers:
            advertiser_id = adv.id
            # Get all conversion pixels:
            conversion_pixels = nexus_get_objects(
                token, {'advertiser_id': advertiser_id}, ConversionPixel, False)
            print 'There is %d  conversion pixels' % len(conversion_pixels)
            # Get all of the insertion orders for one of your advertisers:
            insert_order = nexus_get_objects(token,
                                             {'advertiser_id': advertiser_id},
                                             InsertionOrder, False)
            print 'There is %d  insertion orders' % len(insert_order)

            # Get all of an advertiser's line items:
            line_items = nexus_get_objects(token,
                                           {'advertiser_id': advertiser_id},
                                           LineItem, False)
            print 'There is %d  line items' % len(line_items)
            campaigns = nexus_get_objects(token,
                                          {'advertiser_id': advertiser_id},
                                          Campaign, False)
            print 'There is %d campaigns ' % len(campaigns)

    except Exception as e:
        print "There is error in load_depending_data:", e
        print e.message
        print traceback.print_exc()


# class fakeWith(object):
#     def __enter__(self):
#         pass
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass

# Task, executed twice in hour. Get new data from NexusApp
def dayly_task(day=None, load_objects_from_services=True, output=None):
    old_stdout, old_error = sys.stdout, sys.stderr
    file_output = None
    if not output:
        catalog_name = os.path.join(os.path.dirname(__file__), 'logs')
        clean_old_files(catalog_name)
        log_file_name = 'Dayly_Task_%s.log' % get_current_time().strftime('%Y-%m-%dT%H-%M-%S')
        log_file_name = os.path.join(catalog_name, log_file_name)
        file_output = open(log_file_name, 'w')
        output = file_output
    sys.stdout, sys.stderr = output, output
    print ('NexusApp API pooling...')
    # report.get_specifed_report('network_analytics')
    try:
        token = get_auth_token()
        if load_objects_from_services:
            load_depending_data(token)
        load_report(token, day, NetworkAnalyticsReport)
        load_report(token, day, GeoAnaliticsReport)
        load_reports_for_all_advertisers(
            token, day, SiteDomainPerformanceReport)
    except Exception as e:
        print 'Error by fetching data: %s' % e
        print traceback.print_exc(file=output)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_error
        if file_output:
            file_output.close()
    print "OK"


# load report data, which is not linked with advertiser
def load_report(token, day, ReportClass):
    if not token:
        token = get_auth_token()
    try:
        ReportClass._meta.get_field('day')
        filter_params = {"day": day}
    except:  # Hour
        filter_params = {"hour__date": day}
    q = ReportClass.objects.filter(**filter_params).count()
    if q > 0:
        print "There is %d records in %s, nothing to do." % (q, ReportClass._meta.db_table)
        return
    f_name = get_specified_report(ReportClass, {}, token, day)
    analize_csv(f_name, ReportClass, {})
    os.remove(f_name)


def load_reports_for_all_advertisers(token, day, ReportClass):
    if not token:
        token = get_auth_token()
    # 5 report service processes per user admitted
    worker_pool = ThreadPool(5)
    try:
        ReportClass._meta.get_field('day')
        filter_params = {"day": day}
    except:  # Hour
        filter_params = {"hour__date": day}

    # this prevent zero id value
    # filter_params['pk__gt'] = 0

    q = ReportClass.objects.filter(**filter_params).values('advertiser_id') \
        .annotate(cnt=Count('*')).filter(cnt__gt=0)
    # print q.query
    # select advertisers, which do not have report data
    advertisers_having_data = set(x['advertiser_id'] for x in q)
    print advertisers_having_data
    all_advertisers = dict(Advertiser.objects.all().values_list('id', 'name'))
    all_advertisers.pop(0, None)
    advertisers_need_load = set(all_advertisers) - advertisers_having_data
    campaign_dict = dict(Campaign.objects.all().values_list('id', 'name'))
    all_line_items = set(LineItem.objects.values_list("id", flat=True))

    filenames = worker_pool.map(lambda id: get_specified_report(
        ReportClass, {'advertiser_id': id}, token, day), advertisers_need_load)
    try:
        for f, advertiser_id in izip(filenames, advertisers_need_load):
            analize_csv(f, ReportClass,
                        metadata={"campaign_dict": campaign_dict,
                                  #"all_line_items": all_line_items,
                                  "advertiser_id": advertiser_id})
            print "%s for advertiser %s saved to DB" % (ReportClass, all_advertisers[advertiser_id])
    finally:
        for f in filenames:
            print "Remove file ", f
            os.remove(f)


if __name__ == '__main__':
    dayly_task()
