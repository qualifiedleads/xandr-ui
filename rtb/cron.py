#!/bin/python
import datetime
import common.report as reports
import threading
import csv
from django.conf import settings
import models

def analize_csv(csvFile, modelClass, fieldNames):
    reader = csv.DictReader(csvFile, dialect='excel') # or excel-tab ?
    print 'Begin analyzing csv file ...'
    result=[]
    for row in reader:
        # if first: 
            # first=False
            # continue
        c=modelClass()
        for field in row:
            #if field == 'day': print row[field]
            setattr(c,field,row[field])
        if hasattr(c,'TransformFields'):
            c.TransformFields()
        all_keys = row.keys()
        result.append(c)
        fields_in_row = len(row)
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
        f=reports.get_specifed_report('site_domain_performance',{'advertiser_id':992089}, token)
        #f=open('/home/alex/rtbstats/rtb/logs/2016-06-18T15:58:22.612795_report_fcdb362c76664babc1a973da2c91a946.csv','r')
        r=analize_csv(f, models.StgSiteDomainPerformanceReport, reports.column_sets_for_reports['site_domain_performance'])
    except Exception as e:
        print 'Error by fetching data: %s'%e
    print "There is %d rows fetched "%len(r)
    print r[0].day, r[0].site_domain
    print r[1].day

if __name__=='__main__':hourly_task()
