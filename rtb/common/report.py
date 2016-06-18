import csv
import json
import datetime
import requests
import time
import os
import sets
from django.conf import settings

log_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs')

def get_str_time(): 
    return datetime.datetime.utcnow().isoformat()
    
def import_to_db(csv):
    pass


def get_report(rid, token):
    print "Downloading report..."
    url = "https://api.appnexus.com/report-download?id={0}".format(rid)
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)

    with open('%s/%s_report_%s.csv'%(log_path, get_str_time(),rid), 'wb') as fd:
        for chunk in response.iter_content(1024):
            fd.write(chunk)

    #file-like object
    return response


def get_report_status(rid, token):
    print "Getting report status for rid %s with token %s" % (rid, token)

    exec_stat = ""
    url = "https://api.appnexus.com/report?id={0}".format(rid)
    headers = {"Authorization": token}

    while exec_stat != "ready":
        # Continue making this GET call until the execution_status is "ready"
        response = requests.get(url, headers=headers)
        content = json.loads(response.content)
        exec_stat = content['response']['execution_status']
        time.sleep(1000)

    data = get_report(rid, token)

    return data
    
column_sets_for_reports ={
    "network_analytics":[
        "hour",
        "advertiser_id",
        "advertiser_name",
        "campaign_id",
        "campaign_name",
        "creative_id",
        "creative_name",
        "geo_country",
        "insertion_order_id",
        "insertion_order_name",
        "line_item_id",
        "line_item_name",
        "site_id",
        "site_name",
        "placement_id",
        "placement_name",
        "publisher_id",
        "publisher_name",
        "imps",
        "clicks",
        "total_convs",
        "cost",
        "commissions",
        "serving_fees"
    ],
    "site_domain_performance_":[
        "day",
        "campaign",
        "booked_revenue",
        "imps",
        "clicks",
        "click_thru_pct",
        "site_domain"
    ],
    "site_domain_performance":[
        "day" ,
        "site_domain" ,
        "campaign" ,
        "line_item_id" ,
        "top_level_category" ,
        "second_level_category" ,
        "deal_id" ,
        "advertiser" ,
        "buyer_member_id" ,
        "operating_system" ,
        "supply_type" ,
        "mobile_application_id" ,
        "mobile_application_name" ,
        "mobile_application" ,
        "fold_position" ,
        "age_bucket" ,
        "gender" ,
        "is_remarketing" ,
        #"conversion_pixel_id" , probary pixel_id
        "booked_revenue" ,
        "clicks" ,
        "click_thru_pct" ,
        "convs_per_mm" ,
        "convs_rate" ,
        "cost_ecpa" ,
        "cost_ecpc" ,
        "cpm" ,
        "ctr" ,
        "imps" ,
        "media_cost" ,
        "post_click_convs" ,
        "post_click_convs_rate" ,
        "post_view_convs" ,
        "post_view_convs_rate" ,
        "profit" ,
        "profit_ecpm" ,
        "imps_viewed" ,
        "view_measured_imps" ,
        "view_rate" ,
        "view_measurement_rate" ,
    ]
}
no_hours_reports=sets.Set(["site_domain_performance"])


def get_auth_token():
    try:
        auth_url = "https://api.appnexus.com/auth"
        data = {"auth": settings.NEXUS_AUTH_DATA}
        auth_request = requests.post(auth_url, data=json.dumps(data))
        response = json.loads(auth_request.content)
        return response['response']['token']
    except:
        return None

def get_specifed_report(report_type,query_data={}, token=None):
    if not token:
        token=get_auth_token()
    url = "https://api.appnexus.com/report"
    report_data = {}
    report_data['report'] = {
        "report_type": report_type,
        "columns": column_sets_for_reports[report_type],
        "timezone": "UTC",
        "report_interval": "last_hour" if report_type not in no_hours_reports else "yesterday",
        "format": "csv"
    }
    #report_data['report'].update(query_data)
    #report_data.update(query_data)

    headers = {"Authorization": token, 'Content-Type': 'application/json'}

    r = requests.post(url, params=query_data, data=json.dumps(report_data), headers=headers)

    out = json.loads(r.content)
    
    report_id='Unassigned'
    
    try:
        report_id = out['response']['report_id']
    except Exception as e:
        print 'Error by analizing response: %s'%e
        print out

    with open('%s/%s_report_response_%s.json'%(log_path, get_str_time(), report_id), 'wb') as f:
        f.write(r.content)
    

    return get_report_status(report_id, token)
    
#function to get all advertisers
def get_all_advertisers(token):    
    url='https://api.appnexus.com/advertiser'    
    r=requests.get(url,headers = {"Authorization": token});
    print r.content

try:
    os.makedirs(log_path)
except: pass

#get_specifed_report('network_analytics')
#get_specifed_report('site_domain_performance')
