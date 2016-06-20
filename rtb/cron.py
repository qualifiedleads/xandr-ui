#!/bin/python
import datetime
import common.report as reports
import threading
import csv
from django.conf import settings
#import models
import json
from models import Advertiser
from models_api import  Campaign, SiteDomainPerformanceReport
from pytz import utc
import re
import requests

def update_object_from_dict(o,d):
    error_counter=0
    for field in d:
        try:
            setattr(o,field,row[field])
        except:
            error_counter+=1
    if settings.DEBUG and error_counter>0:
        print "There is %d errors at settings fields in object %s"%(error_counter,repr(o))
    

def analize_csv(csvFile, modelClass, metadata = {}):
    reader = csv.DictReader(csvFile, delimiter=',') #  dialect='excel-tab' or excel ?
    print 'Begin analyzing csv file ...'
    result=[]
    counter=0
    fetch_date = datetime.datetime.utcnow()
    for row in reader:
        c=modelClass()
        c.fetch_date=fetch_date
        update_object_from_dict(c, row)
        if hasattr(c,'TransformFields'):
            c.TransformFields(metadata)
        result.append(c)
        fields_in_row = len(row)
        counter+=1
        if counter%1000==0:
            print '%d rows fetched'%counter
        if counter>10000:break
    print 'There is %d fields in row'%fields_in_row    
    return result


fields_for_site_domain_report=['advertiser_name', 'commissions', 
'placement_id', 'site_id', 'campaign_id', 'serving_fees', 
'campaign_name', 'cost', 'placement_name', 'site_name', 
'line_item_id', 'geo_country', 'publisher_name', 'creative_id', 
'creative_name', 'publisher_id', 'clicks', 'total_convs', 
'advertiser_id', 'insertion_order_id', 'imps', 'hour', 
'insertion_order_name', 'line_item_name'] 

#hour,advertiser_id,advertiser_name,campaign_id,campaign_name,
#creative_id,creative_name,geo_country,insertion_order_id,
#insertion_order_name,line_item_id,line_item_name,site_id,site_name,
#placement_id,placement_name,publisher_id,publisher_name,imps,clicks,
#total_convs,cost,commissions,serving_fees
unix_epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=utc)
def get_current_time():
    return datetime.datetime.utcnow().replace(tzinfo=utc)

# get all Advertisers from DB or with API. Invalidate values, stored in DB
def get_advertisers(token):
    advertisers_in_db=list(Advertiser.objects.all().order_by('fetch_date'))
    print "Advertisers succefully fetched from DB (%d records)"%len(advertisers_in_db)
    current_date=get_current_time()
    try:
        last_date = advertisers_in_db[-1].fetch_date
    except:
        last_date = unix_epoch
    print current_date, last_date
    if current_date-last_date > settings.INVALIDATE_TIME:
        json_text = reports.get_all_advertisers(token)
        advertisers = json.loads(json_text)['response']['advertisers']
        print "Advertisers succefully fetched from Nexus API"
        adv_by_code = {i.code: i for i in advertisers_in_db}
        for i in advertisers:
            object_db = adv_by_code.get(i['code'], Advertiser())
            update_object_from_dict(object_db, i)
            object_db.fetch_date=current_date
            object_db.save()
    return advertisers_in_db
    
#https://api.appnexus.com/creative?start_element=0&num_elements=50'    
def Nexus_get_objects(token, url, params, query_set, object_class, key_field):
    print "Begin of Nexus_get_objects func"
    print url
    last_word = re.search(r'/(\w+)[^/]*$', url).group(1)
    print last_word
    objects_in_db=list(query_set)
    print "Objects succefully fetched from DB (%d records)"%len(objects_in_db)    
    current_date=get_current_time()
    try:
        last_date = objects_in_db[-1].fetch_date
    except:
        last_date = unix_epoch
    if current_date-last_date > settings.INVALIDATE_TIME:
        count,cur_records=-1,-2
        objects_by_api=[]
        data_key_name=None
        while cur_records<count: 
            if cur_records>0:
                params["start_element"]=cur_records
                params["num_elements"]=min(100, count-cur_records)
            r=requests.get(url, params=params, headers = {"Authorization": token});            
            response = json.loads(r.content)['response']
            if not data_key_name:
                data_key_name=list(set(response.keys()) - \
                              set([u'status', u'count', u'dbg_info', u'num_elements', u'start_element']))
                if len(data_key_name)>1:
                    data_key_name = [x for x in data_key_name if x.startswith(last_word)]
                if len(data_key_name)>0:
                    data_key_name = data_key_name[0]
            pack_of_objects=response.get(data_key_name, [])
            if count<0: # first portion of objects
                count = response["count"]
                cur_records = 0
            objects_by_api.extend(pack_of_objects)
            cur_records += response['num_elements']

        print "Objects succefully fetched from Nexus API (%d records)"%len(objects_by_api)
        obj_by_code = {getattr(i,key_field): i for i in objects_in_db}
        for i in objects_by_api:
            object_db = obj_by_code.get(i[key_field])
            if not object_db:
                object_db = object_class()
                objects_in_db.append(object_db) 
            update_object_from_dict(object_db, i)
            if hasattr(object_db, "fetch_date"):
                object_db.fetch_date=current_date
            try:
                object_db.save()
            except Exception as e:
                print "Error by saving ",e
        if settings.DEBUG and len(objects_by_api)>0:
            #field_set_db = set(x.field_name for x in object_class._meta.get_fields())  # get_all_field_names())
            print "Calc field lists difference..."
            field_set_db = set(x.name for x in object_class._meta.fields)  
            field_set_json = set(objects_by_api[0])
            print "Uncommon fields in DB:", field_set_db - field_set_json
            print "Uncommon fields in API:", field_set_json - field_set_db 
            print "All fields in API object", objects_by_api[0].keys()
            print objects_by_api[0]
    return objects_in_db
    
# Task, executed twice in hour. Get new data from NexusApp
def hourly_task():
    print ('NexusApp API pooling...')
    #reports.get_specifed_report('network_analytics')
    try:
        token=reports.get_auth_token()
        advertisers=get_advertisers(token)        
        print 'There is %d advertisers'%len(advertisers)
        advertiser_id = 992089
        #campaigns_for_sel_adv = get_campaigns(token, advertiser_id)
        campaigns_for_sel_adv = Nexus_get_objects(token,
                                'https://api.appnexus.com/campaign',
                                {'advertiser_id':advertiser_id},
                                Campaign.objects.filter(advertiser=advertiser_id).order_by('fetch_date'), 
                                Campaign, 'code')
        print 'There is %d campaigns '%len(campaigns_for_sel_adv)
        campaign_name_to_code = {i.name: i.code for i in campaigns_for_sel_adv}
        #f=reports.get_specifed_report('site_domain_performance',{'advertiser_id':advertiser_id}, token)
        f=open('rtb/logs/2016-06-18T18:42:42.861630_report_3dbaf1cab9c5870fa023e2492028aa58.csv','r')
        r=analize_csv(f, SiteDomainPerformanceReport, 
                      metadata={"campaign_name_to_code": campaign_name_to_code})
        for i in r: i.save()
        print "Domain performance report saved to DB"
    except Exception as e:
        print 'Error by fetching data: %s'%e
    print "There is %d rows fetched "%len(r)

if __name__=='__main__':hourly_task()
