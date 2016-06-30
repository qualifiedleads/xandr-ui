import csv
import json
import datetime
import requests
import time
import os
from django.conf import settings
import utils
#log_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs')
log_path='rtb/logs'

def get_str_time():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
    
def get_report(rid, token):
    print "Downloading report..."
    url = "https://api.appnexus.com/report-download?id={0}".format(rid)
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)

    #Data saved to file to prevent using extra RAM (and debugging)
    fd = open('%s/%s_report_%s.csv'%(log_path, get_str_time(),rid), 'wb+')
    for chunk in response.iter_content(1024):
        fd.write(chunk)
    fd.flush()
    fd.seek(0)
    #file-like object
    return fd


def get_report_status(rid, token):
    print "Getting report status for rid %s with token %s" % (rid, token)

    url = "https://api.appnexus.com/report?id={0}".format(rid)
    headers = {"Authorization": token}
    start_time = datetime.datetime.utcnow()
    while True:
        current_time = datetime.datetime.utcnow()
        if current_time-start_time>settings.MAX_REPORT_WAIT : break
        # Continue making this GET call until the execution_status is "ready"
        response = requests.get(url, headers=headers)
        content = json.loads(response.content)
        exec_stat = content['response']['execution_status']
        if exec_stat == "ready": break
        time.sleep(1)
    if exec_stat!="ready" : return ""
    data = get_report(rid, token)

    return data
    
no_hours_reports=set(["site_domain_performance"])

def get_auth_token():
    try:
        auth_url = "https://api.appnexus.com/auth"
        data = {"auth": settings.NEXUS_AUTH_DATA}
        auth_request = requests.post(auth_url, data=json.dumps(data))
        response = json.loads(auth_request.content)
        return response['response']['token']
    except:
        return None

one_day = datetime.timedelta(days=1)


def get_specifed_report(ReportClass, query_data={}, token=None, day=None):
    report_type = ReportClass.api_report_name
    if not token:
        token=get_auth_token()
    url = "https://api.appnexus.com/report"
    report_data = {}
    report_data['report'] = {
        "report_type": report_type,
        "columns": utils.get_column_list_for_report(ReportClass),
        "timezone": "UTC",
        "format": "csv"
    }
    if not day:
        report_data['report']['report_interval'] = "last_hour" if report_type not in no_hours_reports else "yesterday"
    else:
        report_data['report']["start_date"] = day.strftime("%Y-%m-%d")
        report_data['report']["end_date"] = (day + one_day).strftime("%Y-%m-%d")
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

    #if settings.DEBUG:
        #with open('%s/%s_report_response_%s.json'%(log_path, get_str_time(), report_id), 'wb') as f:
            #f.write(r.content)
    
    return get_report_status(report_id, token)
    
#function to get all advertisers with API
def get_all_advertisers(token):    
    url='https://api.appnexus.com/advertiser'    
    r=requests.get(url,headers = {"Authorization": token});
    return r.content

#function to get all campaigns with API
def get_all_campaigns(token, advertiser_id):    
    url='https://api.appnexus.com/campaign'    
    #url='https://api.appnexus.com/campaign?advertiser_code=ADVERTISER_CODE'
    r=requests.get(url,params={"advertiser_id":advertiser_id}, headers = {"Authorization": token});
    return r.content

def get_report_metadata(token, report_type=''):
    url='https://api.appnexus.com/report?meta'
    if report_type:
        url+='='+report_type
    r=requests.get(url,headers = {"Authorization": token});
    return r.content

try:
    os.makedirs(log_path)
except: pass

#get_specifed_report('network_analytics')
#get_specifed_report('site_domain_performance')
