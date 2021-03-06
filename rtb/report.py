import csv
import re
import json
import datetime
import time
import requests
import os,sys
import utils
from django.conf import settings
import django.db.models as django_types
from django.db.models import Max
from django.db import IntegrityError
from pytz import utc
import itertools

# log_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs')
log_path = settings.LOG_DIR if hasattr(settings,'LOG_DIR') else os.path.expanduser('~')

if not os.path.isdir(log_path):
    log_path = '/tmp'

appnexus_url = settings.__dict__.get(
    'APPNEXUS_URL', 'https://api.appnexus.com/')

# Value in dict - is error critical or not
error_classes = {
    'INTEGRITY': True,
    'LIMIT': True,
    'NOAUTH': False,
    'NOAUTH_DISABLED': True,
    'NOAUTH_EXPIRED': True,
    'SYNTAX': True,
    'SYSTEM': False,
    'UNAUTH': True,
    'NODATA': False,
}


def get_str_time():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')


def get_report(rid, token):
    print "Downloading report..."
    url = appnexus_url + "report-download?id={0}".format(rid)
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers, stream=True)

    # Data saved to file to prevent using extra RAM (and debugging)
    fd = open('%s/%s_report_%s.csv' % (log_path, get_str_time(), rid), 'wb')
    for chunk in response.iter_content(4096):
        fd.write(chunk)
    response.close()
    fd.close()
    return fd.name


def get_report_status(rid, token):
    print "Getting report status for rid %s with token %s" % (rid, token)

    url = appnexus_url + "report?id={0}".format(rid)
    headers = {"Authorization": token}
    start_time = datetime.datetime.utcnow()
    sleep_time = 1
    exec_stat = None
    while True:
        current_time = datetime.datetime.utcnow()
        if current_time - start_time > settings.MAX_REPORT_WAIT:
            break
        # Continue making this GET call until the execution_status is "ready"
        response = requests.get(url, headers=headers)
        content = json.loads(response.content)
        exec_stat = content['response'].get('execution_status')
        if exec_stat == "ready":
            break
        time.sleep(sleep_time)
        sleep_time = min(120, sleep_time * 2)
    if exec_stat != "ready":
        return ""
    data = get_report(rid, token)
    return data


# no_hours_reports = set(["site_domain_performance"])

_last_token = None
_last_token_time = None
_two_hours= datetime.timedelta(hours=1,minutes=55)
def get_auth_token():
    global _last_token,_last_token_time
    if _last_token and utils.get_current_time()-_last_token_time<_two_hours:
        return _last_token
    try:
        auth_url = appnexus_url + "auth"
        data = {"auth": settings.NEXUS_AUTH_DATA}
        auth_request = requests.post(auth_url, data=json.dumps(data))
        response = json.loads(auth_request.content)
        _last_token = response['response']['token']
        _last_token_time = utils.get_current_time()
        return _last_token
    except:
        return None


one_day = datetime.timedelta(days=1)
one_hour = datetime.timedelta(hours=1)


def get_specified_report(ReportClass, query_data=None, token=None, day=None, columns=None, isHour=False):
    if not query_data: query_data={}
    report_type = ReportClass.api_report_name
    if not token:
        token = get_auth_token()
    url = appnexus_url + "report"
    if columns is None:
        columns = utils.get_column_list_for_report(ReportClass)
    report_data = {
        'report': {
            "report_type": report_type,
            "columns": columns,
            "timezone": "UTC",
            "format": "csv"
        }
    }
    if isHour == False:
        if not day:
            # report_data['report']['report_interval'] = "last_hour" if report_type not in no_hours_reports else "yesterday"
            report_data['report']['report_interval'] = "yesterday"
        else:
            report_data['report']["start_date"] = day.strftime("%Y-%m-%d")
            report_data['report']["end_date"] = (
                day + one_day).strftime("%Y-%m-%d")
    else:
        if not day:
            report_data['report']['report_interval'] = "last_hour"
        else:
            report_data['report']["start_date"] = day.strftime("%Y-%m-%d %H:%M:%S")
            report_data['report']["end_date"] = (
                day + one_hour).strftime("%Y-%m-%d %H:%M:%S")


    report_data['report'].update(query_data)

    headers = {"Authorization": token, 'Content-Type': 'application/json'}
    data = json.dumps(report_data)
    report_id = 'Unassigned'
    start_time = datetime.datetime.utcnow()
    while report_id == 'Unassigned':
        current_time = datetime.datetime.utcnow()
        if current_time - start_time > settings.MAX_REPORT_WAIT:
            break
        r = requests.post(
            url,
            params=query_data,
            data=data,
            headers=headers)
        response = json.loads(r.content)['response']
        try:
            if response['status'] == 'error':
                if response['error_id'] == 'NOAUTH':
                    token = get_auth_token()
                    time.sleep(10)
                elif response['error_id'] == 'LIMIT':
                    print "Max report count limit reached, waiting..."
                    time.sleep(30)
                else:
                    print 'Other error:', response['error']
                    time.sleep(10)
                continue
        except Exception as e:
            print 'Error by getting response status: %s' % e
        try:
            report_id = response['report_id']
        except Exception as e:
            print 'Error by getting report_id: %s' % e
            print response
            time.sleep(5)
            # if settings.DEBUG:
            # with open('%s/%s_report_response_%s.json'%(log_path, get_str_time(), report_id), 'wb') as f:
            # f.write(r.content)
    if report_id != 'Unassigned':
        return get_report_status(report_id, token)
    else:
        return ''


def get_report_metadata(token, report_type=''):
    url = appnexus_url + 'report?meta'
    if report_type:
        url += '=' + report_type
    r = requests.get(url, headers={"Authorization": token})
    return r.content


def date_type(t):
    return isinstance(
        t,
        (django_types.DateField,
         django_types.TimeField,
         django_types.DateField))


def replace_tzinfo(o, time_fields=None):
    if time_fields is None:
        time_fields = [
            field.name for field in o._meta.fields if date_type(field)]
    for name in time_fields:
        try:
            attr = getattr(o, name)
            if isinstance(attr, unicode):
                attr += '+00:00'
            else:
                attr = attr.replace(tzinfo=utc)
            setattr(o, name, attr)
        except Exception as e:
            pass
            # print "Error setting timezone for field %s in object %s
            # (%s)"%(name, o, e)


def update_object_from_dict(o, d, time_fields=None):
    for field in d:
        try:
            setattr(o, field, d[field])
        except:
            pass
    replace_tzinfo(o, time_fields)


unix_epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=utc)

def nexus_get_objects_by_id(token, object_class, ids):
    it = iter(ids)
    res = set()
    while True:
        ids_list = ','.join(itertools.imap(str, itertools.islice(it,0,100)))
        if not ids_list:break
        lst = nexus_get_objects(token, {'pk':None},object_class,True,{'id':ids_list})
        res = res | set(x.pk for x in lst)
    return res

def nexus_get_objects(
        token,
        params,
        object_class,
        force_update=False,
        get_params=None,
        new_objects=None,
        isLastModified=None):
    if not token:
        token = get_auth_token()
    if not get_params:
        get_params = params
    url = appnexus_url + object_class.api_endpoint
    last_word = re.search(r'/(\w+)[^/]*$', url).group(1)
    current_date = utils.get_current_time()
    if params:
        query_set = object_class.objects.filter(**params)
    else:
        query_set = object_class.objects.all()
    for k in params.keys():
        if k.endswith('__in'):
            params[k[:-4]] = ','.join(str(x) for x in params[k])
            del params[k]
    last_date = None
    if not force_update:
        if object_class._meta.get_field('fetch_date'):
            last_date = object_class.objects.aggregate(
                m=Max('fetch_date'))['m']
        elif object_class._meta.get_field('last_modified'):
            last_date = query_set.aggregate(m=Max('last_modified'))['m']

    if not last_date:
        last_date = unix_epoch

    if isLastModified:
        LastModified = datetime.datetime(second=last_date.second,  minute=last_date.minute, hour=last_date.hour, day=last_date.day, month=last_date.month,
                                        year=last_date.year, tzinfo=utc) + datetime.timedelta(seconds=1)
        LastModified = LastModified.strftime("%Y-%m-%d+%H:%M:%S")
        get_params['nmin_last_modified'] = LastModified
        # get_params['nmin_last_modified'] = '2017-01-26+08:53:03'

    objects_in_db = list(query_set)
    if force_update or current_date - last_date > settings.INVALIDATE_TIME and get_params.get('nmin_last_modified') == None:
        count, cur_records = -1, -2
        objects_by_api = []
        data_key_name = None
        start_time = datetime.datetime.utcnow()
        while cur_records < count:
            current_time = datetime.datetime.utcnow()
            if current_time - start_time > settings.MAX_REPORT_WAIT:
                break
            if cur_records > 0:
                params["start_element"] = cur_records
                params["num_elements"] = min(100, count - cur_records)
            try:
                r = requests.get(
                    url, params=get_params, headers={
                        "Authorization": token})
                response = json.loads(r.content)['response']
            except Exception as e:
                response = {'error': e.message, 'error_id': 'NODATA'}
            if response.get('error'):
                print response['error']
                if error_classes[response['error_id']]:
                    break
                if response['error_id'] == 'NOAUTH':
                    token = get_auth_token()
                time.sleep(10)
                continue
            try:
                dbg_info = response['dbg_info']
                try:
                    dbg_reads = dbg_info['reads']
                    dbg_limit = dbg_info['read_limit']
                except:
                    dbg_reads = dbg_info['parent_dbg_info']['reads']
                    dbg_limit = dbg_info['parent_dbg_info']['read_limit']
                    pass
                limit = dbg_reads * 1.0 / dbg_limit
                if limit > 0.9:
                    time.sleep((limit - 0.9) * 300)
            except:
                pass

            if not data_key_name:
                data_key_name = list(set(response.keys()) - \
                                     set([u'status', u'count', u'dbg_info', u'num_elements', u'start_element']))
                if len(data_key_name) > 1:
                    data_key_name = [
                        x for x in data_key_name if x.startswith(last_word)]
                if len(data_key_name) > 0:
                    data_key_name = data_key_name[0]
            print data_key_name
            pack_of_objects = response.get(data_key_name, [])

            if count < 0:  # first portion of objects
                count = response["count"]
                if count > 10000:
                    print "There is too many records (%d)" % count
                    print "Entries will be uploaded later, on report loading"
                    return objects_in_db
                cur_records = 0
            if isinstance(pack_of_objects, list):
                objects_by_api.extend(pack_of_objects)
            else:
                objects_by_api.append(pack_of_objects)
            cur_records += response['num_elements']

        print "Objects succefully fetched from Nexus API (%d records)" % len(objects_by_api)
        obj_by_code = {i.pk: i for i in objects_in_db}
        primary_key_name = object_class._meta.pk.name
        foreign_keys = {x.related_model._meta.db_table:x for x in object_class._meta.fields if isinstance(x, django_types.ForeignKey)}
        for i in objects_by_api:
            object_db = obj_by_code.get(i[primary_key_name])
            if not object_db:
                object_db = object_class()
                objects_in_db.append(object_db)
                if new_objects and hasattr(new_objects,'append'):
                    new_objects.append(object_db)
            update_object_from_dict(object_db, i)
            if hasattr(object_db, "fetch_date"):
                object_db.fetch_date = current_date
            if hasattr(object_db, "TransformFields"):
                object_db.TransformFields(i)
            is_saved = False
            tries = 0
            while not is_saved and tries<len(foreign_keys)+1:
                try:
                    tries += 1
                    object_db.save()
                    is_saved = True
                except IntegrityError as e:
                    if e.message.find('foreign key constraint') < 0:
                        print 'finded seeking error'
                        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                        print e
                        raise
                    m = re.search(
                        r'Key \((\w+)\)=\(([^\)]+)\) is not present in table "([^\"]+)"',
                        e.message)
                    if not m:
                        return False
                    key_field, key_value, table_name = m.groups()
                    if key_field=='id':
                        print '-' * 79
                        print '!' * 79
                        print 'Try of null-ing id! Previos error was ', e
                        print '-' * 79
                        time.sleep(15)
                        continue

                    fk = foreign_keys[table_name] # TODO what on multiple foreign keys to same table - ???
                    val = getattr(object_db, key_field)
                    t = type(val)
                    # simple control - field is right
                    if t(key_value) == val:
                        setattr(object_db, key_field, None)
                        print 'Nulling field %s on object %s (was %s)'%(fk.name, object_db, val)
                except Exception as e:
                    print "Error by saving ", e
                    print sys.exc_info()
                    print i
                    break
        if settings.DEBUG and len(objects_by_api) > 0:
            # field_set_db = set(x.field_name for x in
            # object_class._meta.get_fields())  # get_all_field_names())
            print "Calc field lists difference..."
            field_set_db = set(x.name for x in object_class._meta.fields)
            field_set_json = set(objects_by_api[0])
            print "Uncommon fields in DB:", field_set_db - field_set_json
            print "Uncommon fields in API:", field_set_json - field_set_db
            # print objects_by_api

    if force_update == False and get_params.get('nmin_last_modified') and isLastModified:
        count, cur_records = -1, -2
        objects_by_api = []
        data_key_name = None
        start_time = datetime.datetime.utcnow()
        while cur_records < count:
            current_time = datetime.datetime.utcnow()
            if current_time - start_time > settings.MAX_REPORT_WAIT:
                break
            if cur_records > 0:
                params["start_element"] = cur_records
                params["num_elements"] = min(100, count - cur_records)
            try:
                r = requests.get(
                    url, params=get_params, headers={
                        "Authorization": token})
                response = json.loads(r.content)['response']
            except Exception as e:
                response = {'error': e.message, 'error_id': 'NODATA'}
            if response.get('error'):
                print response['error']
                if error_classes[response['error_id']]:
                    break
                if response['error_id'] == 'NOAUTH':
                    token = get_auth_token()
                time.sleep(10)
                continue
            try:
                dbg_info = response['dbg_info']
                try:
                    dbg_reads = dbg_info['reads']
                    dbg_limit = dbg_info['read_limit']
                except:
                    dbg_reads = dbg_info['parent_dbg_info']['reads']
                    dbg_limit = dbg_info['parent_dbg_info']['read_limit']
                    pass
                limit = dbg_reads * 1.0 / dbg_limit
                if limit > 0.9:
                    time.sleep((limit - 0.9) * 300)
            except:
                pass
            if not data_key_name:
                data_key_name = list(set(response.keys()) - \
                                     set([u'status', u'count', u'dbg_info', u'num_elements', u'start_element']))
                if len(data_key_name) > 1:
                    data_key_name = [
                        x for x in data_key_name if x.startswith(last_word)]
                if len(data_key_name) > 0:
                    data_key_name = data_key_name[0]
            print data_key_name
            pack_of_objects = response.get(data_key_name, [])

            if isinstance(pack_of_objects, list):
                objects_by_api.extend(pack_of_objects)
            else:
                objects_by_api.append(pack_of_objects)
            cur_records += response['num_elements']

        print "Objects successfully fetched from Nexus API (%d records)" % len(objects_by_api)
        obj_by_code = {i.pk: i for i in objects_in_db}
        primary_key_name = object_class._meta.pk.name
        foreign_keys = {x.related_model._meta.db_table:x for x in object_class._meta.fields if isinstance(x, django_types.ForeignKey)}
        for i in objects_by_api:
            object_db = obj_by_code.get(i[primary_key_name])
            if not object_db:
                object_db = object_class()
                objects_in_db.append(object_db)
                if new_objects and hasattr(new_objects,'append'):
                    new_objects.append(object_db)
            update_object_from_dict(object_db, i)
            if hasattr(object_db, "fetch_date"):
                object_db.fetch_date = current_date
            if hasattr(object_db, "TransformFields"):
                object_db.TransformFields(i)
            is_saved = False
            tries = 0
            while not is_saved and tries<len(foreign_keys)+1:
                try:
                    tries += 1
                    object_db.save()
                    is_saved = True
                except IntegrityError as e:
                    if e.message.find('foreign key constraint') < 0:
                        print 'finded seeking error'
                        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                        print e
                        raise
                    m = re.search(
                        r'Key \((\w+)\)=\(([^\)]+)\) is not present in table "([^\"]+)"',
                        e.message)
                    if not m:
                        return False
                    key_field, key_value, table_name = m.groups()
                    if key_field=='id':
                        print '-' * 79
                        print '!' * 79
                        print 'Try of null-ing id! Previos error was ', e
                        print '-' * 79
                        time.sleep(15)
                        continue

                    fk = foreign_keys[table_name] # TODO what on multiple foreign keys to same table - ???
                    val = getattr(object_db, key_field)
                    t = type(val)
                    # simple control - field is right
                    if t(key_value) == val:
                        setattr(object_db, key_field, None)
                        print 'Nulling field %s on object %s (was %s)'%(fk.name, object_db, val)
                except Exception as e:
                    print "Error by saving ", e
                    print sys.exc_info()
                    print i
                    break
        if settings.DEBUG and len(objects_by_api) > 0:
            # field_set_db = set(x.field_name for x in
            # object_class._meta.get_fields())  # get_all_field_names())
            print "Calc field lists difference..."
            field_set_db = set(x.name for x in object_class._meta.fields)
            field_set_json = set(objects_by_api[0])
            print "Uncommon fields in DB:", field_set_db - field_set_json
            print "Uncommon fields in API:", field_set_json - field_set_db
            # print objects_by_api
    return objects_in_db

# get_specifed_report('network_analytics')
# get_specifed_report('site_domain_performance')
