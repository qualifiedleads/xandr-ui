#!/bin/python
import datetime
import common.report as reports
import threading
import csv
from django.conf import settings
import models
import json

def analize_csv(csvFile, modelClass, fieldNames):
    reader = csv.DictReader(csvFile, delimiter=',') #  dialect='excel-tab' or excel ?
    print 'Begin analyzing csv file ...'
    result=[]
    counter=0
    fetch_date = datetime.datetime.utcnow()
    for row in reader:
        # if first: 
            # first=False
            # continue
        c=modelClass()
        c.fetch_date=fetch_date
        for field in row:
            if field: 
                setattr(c,field,row[field])
            else:
                print 'Somewhat imposible: null field name'
        if hasattr(c,'TransformFields'):
            c.TransformFields()
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

# Task, executed twice in hour. Get new data from NexusApp
def hourly_task():
    print ('NexusApp API pooling...')
    #reports.get_specifed_report('network_analytics')
    try:
        token=reports.get_auth_token()
        advertisers = json.loads(reports.get_all_advertisers(token))['response']['advertisers']
        print 'There is %d advertisers'%len(advertisers)
        #f=reports.get_specifed_report('site_domain_performance',{'advertiser_id':992089}, token)
        f=open('rtb/logs/2016-06-18T18:42:42.861630_report_3dbaf1cab9c5870fa023e2492028aa58.csv','r')
        r=analize_csv(f, models.StgSiteDomainPerformanceReport, reports.column_sets_for_reports['site_domain_performance'])
        for i in r: i.save()
        print "Domain performance report saved to DB"
    except Exception as e:
        print 'Error by fetching data: %s'%e
    print "There is %d rows fetched "%len(r)

if __name__=='__main__':hourly_task()
