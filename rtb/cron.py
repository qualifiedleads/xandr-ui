#!/bin/env python
import csv
import datetime
import time
import decimal
import gc
import json
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
    Language, NetworkAnalyticsReport_ByPlacement, NetworkCarrierReport_Simple, NetworkDeviceReport_Simple

from pytz import utc
from utils import get_all_classes_in_models, get_current_time, clean_old_files
from rtb.crons.video_ad_cron import fillVideoAdDataCron

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
                if not data[k]:
                    data[k] = None
            except:
                data[k] = None
        for k in _create_execute_context_['nullable_keys']:
            val = str(data.get(k))
            if val[:2] == '--' or val == 'Undisclosed':
                data[k] = None
        for k in _create_execute_context_['float_keys']:
            s = str(data.get(k, ''))
            if s.endswith('%'):
                data[k] = s[:-1]
        modelClass = _create_execute_context_['modelClass']
        for k in _create_execute_context_['boolean_fields']:
            s = str(data.get(k, ''))
            if s=='no': data[k] = False
            if s == 'yes': data[k] = True
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
    return [field.attname for field in modelClass._meta.fields]


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



def has_copy_from_support():
    cursor = connection.cursor()
    return hasattr(cursor, 'copy_from')

_has_copy_from_support = has_copy_from_support()

def analize_csv_direct(filename, modelClass):
    fields = get_all_class_fields(modelClass)
    #res = modelClass.objects.raw('select * from network_analytics_report_by_placement;')
    with open(filename, 'r') as csvFile:
        fields_csv = csvFile.readline().rstrip().split(',')
        t_set = set(fields)
        t_set.discard('id')
        c_set = set(fields_csv)
        if not set(c_set).issubset(t_set) and not hasattr(modelClass,'add_api_columns'):
            raise Exception('analize_csv_direct not possibly: fields not match')
        with connection.cursor() as cursor:
            try:
                #cursor.copy_from(csvFile, modelClass._meta.db_table,',',columns = fields_csv)
                cursor.copy_expert('COPY "{}"({}) FROM STDOUT WITH CSV'\
                    .format(modelClass._meta.db_table, ','.join(fields_csv)),
                    csvFile)
            except Exception as e:
                print e

def analize_csv(filename, modelClass, metadata={}):
    if _has_copy_from_support and hasattr(modelClass, 'direct_csv') and modelClass.direct_csv:
        analize_csv_direct(filename, modelClass)
        return
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
            class_fields) and not hasattr(modelClass,'api_columns')
        context['time_fields'] = [
            field.name for field in modelClass._meta.fields if date_type(field)]
        context['nullable_keys'] = [
            field.name for field in modelClass._meta.fields if field.null and not isinstance(
                field, (django_types.CharField, django_types.TextField)) and field.name in csv_fields]
        context['float_keys'] = [
            field.name for field in modelClass._meta.fields if isinstance(
                field, (django_types.FloatField, django_types.DecimalField))]
        context['boolean_fields'] = [field.attname for field in modelClass._meta.fields
                          if isinstance(field,(django_types.BooleanField, django_types.NullBooleanField))]
        foreign_fields = [field.attname for field in modelClass._meta.fields
            if isinstance(field, django_types.ForeignObject)]
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
def load_depending_data(token, force_update=False, daily_load=True):
    # nexus_get_objects\(.*?'(https://api.appnexus.com/[\w-]+)',\s*\{[^\}]*\},\s*(\w+)
    try:
        cd = get_current_time()
        with transaction.atomic():
            advertisers = nexus_get_objects(token,
                                            {"id__gt": 0},
                                            Advertiser, force_update, {})
            print 'There is %d advertisers' % len(advertisers)

            for adv in advertisers:
                # Get all of the profiles for the advertiser
                profiles = nexus_get_objects(token,
                                             {'advertiser_id': adv.id},
                                             Profile, force_update)
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

        if daily_load:
            developers = nexus_get_objects(token,
                                           {},
                                           Developer, False)
            print 'There is %d developers ' % len(developers)
            buyer_groups = nexus_get_objects(token,
                                             {},
                                             BuyerGroup, False)
            print 'There is %d buyer groups ' % len(buyer_groups)

            # There is mutual dependence
            #with transaction.atomic():
            ad_profiles = nexus_get_objects(token,
                                            {},
                                            AdProfile, False)
            print 'There is %d adware profiles ' % len(ad_profiles)
            members = nexus_get_objects(token,
                                        {},
                                        Member, False)
            print 'There is %d members ' % len(members)
            #end transaction

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

            #with transaction.atomic():
            date_in_db = ContentCategory.objects.aggregate(
                m=Max('fetch_date'))['m']
            if cd - date_in_db > settings.INVALIDATE_TIME:
                o1 = nexus_get_objects(token,
                                       {},  # {'type':'universal'}
                                       ContentCategory, force_update,
                                       {'category_type': 'universal'})
                o2 = nexus_get_objects(token,
                                       {},
                                       ContentCategory, force_update)
            # end transaction
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

            # with transaction.atomic():
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
            payment_rules_to_load=Publisher.objects.filter(base_payment_rule_id__gt=0)\
                .values_list('base_payment_rule_id','id').distinct()
            print payment_rules_to_load
            for x in payment_rules_to_load:
                payment_rule = nexus_get_objects(token,
                                                  {'id': x[0]},
                                                  PaymentRule,
                                                  True,
                                                  {'publisher_id': x[1], 'id': x[0]}
                                                )
                print payment_rule
            #end transaction
            companies = nexus_get_objects(token,
                                          {},
                                          Company, False)
            print 'There is %d companies ' % len(companies)

            categories = nexus_get_objects(token,
                                           {},
                                           Category, False)
            print 'There is %d categories ' % len(categories)

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

            # with transaction.atomic():
            nexus_get_objects(token,
                              {},
                              Creative, force_update)
            brand_ids = set(Creative.objects.filter(brand_id__isnull=False) \
                               .values_list('brand', flat=True).distinct())
            exiting_brands = set(Brand.objects.values_list('id', flat=True))

            print 'Creatives loaded'
            ids_list = map(str,brand_ids-exiting_brands)
            print 'Brand ids:', ids_list
            brands = nexus_get_objects(token,
                                       {},
                                       Brand, force_update,
                                       {'id':','.join(ids_list), 'simple':'true'})
            print 'There is %d brands ' % len(brands)
            profiles_ids = set(Creative.objects.filter(profile_id__isnull=False) \
                               .values_list('profile', flat=True).distinct())
            exiting_profiles = set(Profile.objects.values_list('id', flat=True))
            profiles = nexus_get_objects(token,
                                         {},
                                         Profile, force_update,
                                         {'id':','.join(map(str,profiles_ids-exiting_profiles))})
            print 'There is %d new profiles'%len(profiles)
            # end transaction
            # Get all payment rules:
            for pub in []:  # publishers: There is too many publishers, disable loading depended objects
                payment_rules = nexus_get_objects(token,
                                                  {'publisher': pub},
                                                  PaymentRule, force_update,
                                                  {'publisher_id': pub.pk})
                print 'There is %d payment rules for publisher %s' % (len(payment_rules), pub.name)
                print 'Ids:', ','.join(str(x.pk) for x in payment_rules)
                quality_rules = nexus_get_objects(token,
                                                  {'publisher': pub},
                                                  AdQualityRule, force_update,
                                                  {'publisher_id': pub.pk})
                print 'There is %d quality rules for publisher %s' % (len(payment_rules), pub.name)
                # Placement
                # https://api.appnexus.com/placement?publisher_id=PUBLISHER_ID
                placements = nexus_get_objects(token,
                                               {'publisher': pub},
                                               Placement, force_update,
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
                                               LineItem, daily_load)
                print 'There is %d  line items' % len(line_items)
                campaigns = nexus_get_objects(token,
                                              {'advertiser_id': advertiser_id},
                                              Campaign, daily_load)
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


def hourlyTask(dayWithHour=None, load_objects_from_services=True, output=None):
    old_stdout, old_error = sys.stdout, sys.stderr
    file_output = None
    try:
        if not output:
            if hasattr(settings, 'LOG_DIR') and settings.LOG_DIR:
                catalog_name = settings.LOG_DIR
            else:
                catalog_name = os.path.join(os.path.dirname(__file__), 'logs')
            clean_old_files(catalog_name)
            log_file_name = 'Dayly_Task_%s.log' % get_current_time().strftime('%Y-%m-%dT%H-%M-%S')
            log_file_name = os.path.join(catalog_name, log_file_name)
            file_output = open(log_file_name, 'w', 1)  # line buffered file
            file_output.write('Begin write log file {}\n'.format(get_current_time()))
            output = file_output
    except:
        pass
    if output:
        sys.stdout, sys.stderr = output, output

    # report.get_specifed_report('network_analytics')

    one_hour = datetime.timedelta(hours=1)

    if dayWithHour:
        dayWithHour = datetime.datetime(hour=dayWithHour.hour, day=dayWithHour.day, month=dayWithHour.month, year=dayWithHour.year, tzinfo=utc)
        last_day = dayWithHour
    else:
        dayWithHour = SiteDomainPerformanceReport.objects.aggregate(m=Max('hour'))['m']
        print 'Last loaded hour', dayWithHour

        if dayWithHour:
            dayWithHour = datetime.datetime(hour=dayWithHour.hour, day=dayWithHour.day, month=dayWithHour.month,
                                            year=dayWithHour.year, tzinfo=utc)
        else:
            dayWithHour -= one_hour

    dateNow = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=utc)
    try:
        token = get_auth_token()
        if load_objects_from_services:
             load_depending_data(token, True)
        while dayWithHour <= dateNow:
            load_report(token, dayWithHour, NetworkAnalyticsReport_ByPlacement, isHour=True)
            load_reports_for_all_advertisers(token, dayWithHour, SiteDomainPerformanceReport, isHour=True)
            fillVideoAdDataCron()
            dayWithHour += one_hour
    except Exception as e:
        print 'Error by fetching data: %s' % e
        print traceback.print_exc(file=output)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_error
        if file_output:
            file_output.close()
    print "OK"


# Task, executed once in day. Get new data from NexusApp
def dayly_task(day=None, load_objects_from_services=True, output=None):
    old_stdout, old_error = sys.stdout, sys.stderr
    file_output = None
    try:
        if not output:
            if hasattr(settings,'LOG_DIR') and settings.LOG_DIR:
                catalog_name = settings.LOG_DIR
            else:
                catalog_name =  os.path.join(os.path.dirname(__file__), 'logs')
            clean_old_files(catalog_name)
            log_file_name = 'Dayly_Task_%s.log' % get_current_time().strftime('%Y-%m-%dT%H-%M-%S')
            log_file_name = os.path.join(catalog_name, log_file_name)
            file_output = open(log_file_name, 'w', 1) # line buffered file
            file_output.write('Begin write log file {}\n'.format(get_current_time()))
            output = file_output
    except:
        pass
    if output:
        sys.stdout, sys.stderr = output, output

    # report.get_specifed_report('network_analytics')

    one_day = datetime.timedelta(days=1)

    yesterday = datetime.datetime.utcnow().replace(hour=0, minute=0,second=0,microsecond=0, tzinfo=utc)-one_day
    if day:
        day = datetime.datetime(day=day.day, month=day.month, year=day.year, tzinfo=utc)
        last_day=day
    else:
        day = SiteDomainPerformanceReport.objects.aggregate(m=Max('day'))['m']
        print 'Last loaded day', day
        if day:
            day = datetime.datetime(day=day.day, month=day.month, year=day.year, tzinfo=utc)
            day+=one_day
        else:
            # empty database
            day = yesterday - 30 * one_day
        last_day=yesterday
    try:
        token = get_auth_token()
        # if load_objects_from_services:
            # load_depending_data(token, True)
        while day<=last_day:
            load_report(token, day, NetworkCarrierReport_Simple, isHour=False)        # only day
            load_report(token, day, NetworkDeviceReport_Simple, isHour=False)         # only day
            # load_report(token, day, NetworkAnalyticsReport, isHour=False            # not used
            load_report(token, day, GeoAnaliticsReport, isHour=False)                 # only day
            load_report(token, day, NetworkAnalyticsReport_ByPlacement, isHour=False)
            load_reports_for_all_advertisers(token, day, SiteDomainPerformanceReport, isHour=False)
            fillVideoAdDataCron()
            day += one_day
    except Exception as e:
        print 'Error by fetching data: %s' % e
        print traceback.print_exc(file=output)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_error
        if file_output:
            file_output.close()
    print "OK"


# load report data, which is not linked with advertiser
def load_report(token, day, ReportClass, isHour=False):
    if isHour == False:
        if not day:
            day = datetime.datetime.utcnow()-datetime.timedelta(days=1)
            day = day.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=utc)
        if not token:
            token = get_auth_token()
        try:
            ReportClass._meta.get_field('day')
            filter_params = {"day": day}
        except:  # Hour
            filter_params = {"hour__date": day}
    else:
        if not day:
            day = datetime.datetime.utcnow()-datetime.timedelta(hours=1)
            day = day.replace(minute=0, second=0, microsecond=0, tzinfo=utc)
        if not token:
            token = get_auth_token()
        try:
            ReportClass._meta.get_field('hour')
            filter_params = {"hour": day}
        except:  # Hour
            filter_params = {"day": day}
    q = ReportClass.objects.filter(**filter_params).count()
    if q % 4000 == 0 and q > 0:
        print 'Delete partially loaded data (load_report)'
        ReportClass.objects.filter(**filter_params).delete()
        q = 0
    if q > 0:
        print "There is %d records in %s, nothing to do." % (q, ReportClass._meta.db_table)
        return
    if isHour == False:
        f_name = get_specified_report(ReportClass, {}, token, day, columns=None, isHour=False)
    else:
        f_name = get_specified_report(ReportClass, {}, token, day, columns=None, isHour=True)
    analize_csv(f_name, ReportClass, {})
    os.remove(f_name)
    if hasattr(ReportClass,'post_load'):
        ReportClass.post_load(day)


def load_reports_for_all_advertisers(token, day, ReportClass, isHour=False):
    if not day:
        day = datetime.datetime.utcnow()-datetime.timedelta(days=1)
        day = day.replace(hour=0,minute=0,second=0,microsecond=0,tzinfo=utc)
    if not token:
        token = get_auth_token()
    # 5 report service processes per user admitted
    worker_pool = ThreadPool(5)
    if isHour == False:
        try:
            ReportClass._meta.get_field('day')
            filter_params = {"day": day}
        except:  # Hour
            filter_params = {"hour__date": day}
    else:
        try:
            ReportClass._meta.get_field('hour')
            filter_params = {"hour": day}
        except:  # Hour
            filter_params = {"day": day}

    # this prevent zero id value
    # filter_params['pk__gt'] = 0

    q = list(ReportClass.objects.filter(**filter_params).values('advertiser_id') \
        .annotate(cnt=Count('*')))
    for g in q:
        if g['cnt'] % 4000 == 0 and g['cnt']>0:
            print 'Delete partially loaded data (load_reports_for_all_advertisers)'
            ReportClass.objects.filter(**filter_params)\
                .filter(advertiser_id=g['advertiser_id']).delete()
            g['cnt']=0

    # print q.query
    # select advertisers, which do not have report data
    advertisers_having_data = set(x['advertiser_id'] for x in q if x['cnt']>0)
    print advertisers_having_data
    all_advertisers = dict(Advertiser.objects.all().values_list('id', 'name'))
    all_advertisers.pop(0, None)
    advertisers_need_load = set(all_advertisers) - advertisers_having_data
    campaign_dict = dict(Campaign.objects.all().values_list('id', 'name'))
    all_line_items = set(LineItem.objects.values_list("id", flat=True))

    if isHour == False:
        filenames = worker_pool.map(lambda id: get_specified_report(
        ReportClass, {'advertiser_id': id}, token, day, columns=None, isHour=False), advertisers_need_load)
    else:
        filenames = worker_pool.map(lambda id: get_specified_report(
        ReportClass, {'advertiser_id': id}, token, day, columns=None, isHour=True), advertisers_need_load)
    try:
        for f, advertiser_id in izip(filenames, advertisers_need_load):
            analize_csv(f, ReportClass,
                        metadata={"campaign_dict": campaign_dict,
                                  #"all_line_items": all_line_items,
                                  "advertiser_id": advertiser_id})
            print "%s for advertiser %s saved to DB" % (ReportClass, all_advertisers[advertiser_id])
        if hasattr(ReportClass, 'post_load'):
            ReportClass.post_load(day)
    finally:
        for f in filenames:
            print "Remove file ", f
            os.remove(f)


if __name__ == '__main__':
    dayly_task()
