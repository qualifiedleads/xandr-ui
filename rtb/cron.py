#!/bin/python
import csv
import datetime
import gc
import json
import os
import sys
import traceback
from itertools import imap, izip, islice
from multiprocessing.pool import ThreadPool
from django.db.models import Avg, Count, Sum
import django.db.models as django_types
import re
import requests
import report
from django.conf import settings
from models import Advertiser, Campaign, SiteDomainPerformanceReport, Profile, LineItem, InsertionOrder, \
    OSFamily, OperatingSystemExtended, NetworkAnalyticsReport
from pytz import utc


def date_type(t):
    return isinstance(t, (django_types.DateField, django_types.TimeField, django_types.DateField))


def replace_tzinfo(o, time_fields=None):
    if time_fields is None:
        time_fields = [field.name for field in o._meta.fields if date_type(field)]
    for name in time_fields:
        try:
            attr = getattr(o, name)
            if type(attr) == unicode:
                attr += '+00:00'
            else:
                attr = attr.replace(tzinfo=utc)
            setattr(o, name, attr)
        except Exception as e:
            pass
            # print "Error setting timezone for field %s in object %s (%s)"%(name, o, e)


def update_object_from_dict(o, d, time_fields=None):
    for field in d:
        try:
            setattr(o, field, d[field])
        except:pass
    replace_tzinfo(o, time_fields)

def analize_csv(csvFile, modelClass, metadata={}):
    reader = csv.DictReader(csvFile, delimiter=',')  # dialect='excel-tab' or excel ?
    print 'Begin analyzing csv file ...'
    #result = []
    metadata['counter'] = 0
    fetch_date = get_current_time()
    time_fields = [field.name for field in modelClass._meta.fields if date_type(field)]
    def create_object_from_dict(data):
        try:
            c = modelClass(**data)
            # replace_tzinfo(c, time_fields)
        except:
            c = modelClass()
            update_object_from_dict(c, data, time_fields)
        c.fetch_date = fetch_date
        #replace_tzinfo(c, time_fields)
        if hasattr(c, 'TransformFields'):
            c.TransformFields(data, metadata)
        metadata['counter']+=1
        return c

    it = imap(create_object_from_dict, reader)
    while True:
        res = modelClass.objects.bulk_create(islice(it, 0, 1000))
        print '%d rows fetched' % metadata['counter']
        if not res: break


unix_epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=utc)


def get_current_time():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


# https://api.appnexus.com/creative?start_element=0&num_elements=50'
def nexus_get_objects(token, url, params, query_set, object_class, key_field, force_update=False):
    print "Begin of Nexus_get_objects func"
    last_word = re.search(r'/(\w+)[^/]*$', url).group(1)
    #print last_word
    objects_in_db = list(query_set)
    #print "Objects succefully fetched from DB (%d records)" % len(objects_in_db)
    current_date = get_current_time()
    try:
        last_date = objects_in_db[-1].fetch_date
    except:
        last_date = unix_epoch
    if force_update or current_date - last_date > settings.INVALIDATE_TIME:
        count, cur_records = -1, -2
        objects_by_api = []
        data_key_name = None
        while cur_records < count:
            if cur_records > 0:
                params["start_element"] = cur_records
                params["num_elements"] = min(100, count - cur_records)
            r = requests.get(url, params=params, headers={"Authorization": token})
            response = json.loads(r.content)['response']
            if not data_key_name:
                data_key_name = list(set(response.keys()) - \
                                     set([u'status', u'count', u'dbg_info', u'num_elements', u'start_element']))
                if len(data_key_name) > 1:
                    data_key_name = [x for x in data_key_name if x.startswith(last_word)]
                if len(data_key_name) > 0:
                    data_key_name = data_key_name[0]
            print data_key_name
            pack_of_objects = response.get(data_key_name, [])
            if count < 0:  # first portion of objects
                count = response["count"]
                cur_records = 0
            objects_by_api.extend(pack_of_objects)
            cur_records += response['num_elements']

        print "Objects succefully fetched from Nexus API (%d records)" % len(objects_by_api)
        obj_by_code = {getattr(i, key_field): i for i in objects_in_db}
        for i in objects_by_api:
            object_db = obj_by_code.get(i[key_field])
            if not object_db:
                object_db = object_class()
                objects_in_db.append(object_db)
            update_object_from_dict(object_db, i)
            if hasattr(object_db, "fetch_date"):
                object_db.fetch_date = current_date
            if hasattr(object_db, "TransformFields"):
                object_db.TransformFields(i)
            try:
                object_db.save()
            except Exception as e:
                print "Error by saving ", e
        if settings.DEBUG and len(objects_by_api) > 0:
            # field_set_db = set(x.field_name for x in object_class._meta.get_fields())  # get_all_field_names())
            print "Calc field lists difference..."
            field_set_db = set(x.name for x in object_class._meta.fields)
            field_set_json = set(objects_by_api[0])
            print "Uncommon fields in DB:", field_set_db - field_set_json
            print "Uncommon fields in API:", field_set_json - field_set_db
            #print objects_by_api
    return objects_in_db

#load data, needed for filling SiteDomainPerformanceReport
#Data saved to local DB
def load_depending_data(token):
    try:
        advertisers = nexus_get_objects(token,
                                        'https://api.appnexus.com/advertiser',
                                        {},
                                        Advertiser.objects.all().order_by('fetch_date'),
                                        Advertiser, 'id')
        print 'There is %d advertisers' % len(advertisers)

        for adv in advertisers:
            advertiser_id = adv.id
            # Get all of the profiles for the advertiser
            profiles = nexus_get_objects(token,
                                         'https://api.appnexus.com/profile',
                                         {'advertiser_id': advertiser_id},
                                         Profile.objects.filter(advertiser=advertiser_id).order_by('fetch_date'),
                                         Profile, 'id', False)
            print 'There is %d profiles' % len(profiles)
            # Get all of the insertion orders for one of your advertisers:
            insert_order = nexus_get_objects(token,
                                             'https://api.appnexus.com/insertion-order',
                                             {'advertiser_id': advertiser_id},
                                             InsertionOrder.objects.filter(advertiser=advertiser_id).order_by('fetch_date'),
                                             InsertionOrder, 'id', False)
            print 'There is %d  insertion orders' % len(insert_order)
            if len(insert_order) > 0:
                print 'First insertion order:'
                print insert_order[0]
                print '-' * 80
            # Get all of an advertiser's line items:
            line_items = nexus_get_objects(token,
                                           'https://api.appnexus.com/line-item',
                                           {'advertiser_id': advertiser_id},
                                           LineItem.objects.filter(advertiser=advertiser_id).order_by('fetch_date'),
                                           LineItem, 'id', False)
            print 'There is %d  line items' % len(line_items)
            if len(insert_order) > 0:
                print 'First insertion order:'
                print insert_order[0]
                print '-' * 80
            campaigns = nexus_get_objects(token,
                                          'https://api.appnexus.com/campaign',
                                          {'advertiser_id': advertiser_id},
                                          Campaign.objects.filter(advertiser=advertiser_id).order_by('fetch_date'),
                                          Campaign, 'id', False)
            print 'There is %d campaigns ' % len(campaigns)
            # Get all operating system families:
            operating_systems_families = nexus_get_objects(token,
                                                           'https://api.appnexus.com/operating-system-family',
                                                           {},
                                                           OSFamily.objects.all().order_by('fetch_date'),
                                                           OSFamily, 'id', False)
            print 'There is %d operating system families' % len(operating_systems_families)
            # Get all operating systems:
            operating_systems = nexus_get_objects(token,
                                                  'https://api.appnexus.com/operating-system-extended',
                                                  {},
                                                  OperatingSystemExtended.objects.all().order_by('fetch_date'),
                                                  OperatingSystemExtended, 'id', False)
            print 'There is %d operating systems ' % len(operating_systems)
    except Exception as e:
        print "There is error in load_depending_data:",e
        print e.message
        print traceback.print_exc()


class fakeWith(object):
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Task, executed twice in hour. Get new data from NexusApp
def dayly_task(day=None, load_objects_from_services=True, output=None):
    old_stdout, old_error = sys.stdout, sys.stderr
    file_output = None
    if not output:
        log_file_name = 'rtb/logs/Dayly_Task_%s.log' % get_current_time().strftime('%Y-%m-%dT%H-%M-%S')
        file_output = open(log_file_name, 'w')
        output=file_output
    sys.stdout, sys.stderr = output, output
    print ('NexusApp API pooling...')
    # report.get_specifed_report('network_analytics')
    try:
        token = report.get_auth_token()
        if load_objects_from_services:
            pass
            # load_depending_data(token)
        load_reports_for_all_advertisers(token, day, SiteDomainPerformanceReport)
        # load_reports_for_all_advertisers(token, day, NetworkAnalyticsReport)
    except Exception as e:
        print 'Error by fetching data: %s' % e
        print traceback.print_exc(file=output)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_error
        if file_output: file_output.close()
    print "OK"
    gc.collect()
    print "There is %d items of garbage"%len(gc.garbage)


def load_reports_for_all_advertisers(token, day, ReportClass):
    if not token:
        token = report.get_auth_token()
    # 5 report service processes per user admitted
    worker_pool = ThreadPool(4)  # one thread reserved
    # select advertisers, which do not have report data
    try:
        ReportClass._meta.get_field('day')
        filter_params = {"day": day}
    except:  # Hour
        filter_params = {"hour__date": day}

    q = ReportClass.objects.filter(**filter_params).values('advertiser_id') \
        .annotate(cnt=Count('*')).filter(cnt__gt=0)
    print q.query
    advertisers_having_data = set(x['advertiser_id'] for x in q)
    print advertisers_having_data
    all_advertisers = dict(Advertiser.objects.all().values_list('id', 'name'))
    advertisers_need_load = set(all_advertisers) - advertisers_having_data
    campaign_dict = dict(Campaign.objects.all().values_list('id', 'name'))
    all_line_items = set(LineItem.objects.values_list("id", flat=True))
    # Multithreading map
    files = []
    try:
        files = worker_pool.map(lambda id:
                                report.get_specifed_report(ReportClass.api_report_name, {'advertiser_id': id}, token,
                                                           day),
                                advertisers_need_load)
        for f, advertiser_id in izip(files, advertisers_need_load):
            analize_csv(f, ReportClass,
                        metadata={"campaign_dict": campaign_dict,
                                  "all_line_items": all_line_items,
                                  "advertiser_id": advertiser_id})
            print "Domain performance report for advertiser %s saved to DB" % all_advertisers[advertiser_id]
    finally:
        for f in files:
            f.close()
            os.remove(f.name)


if __name__ == '__main__': dayly_task()
