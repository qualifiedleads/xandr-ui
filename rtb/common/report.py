import csv
import json
import datetime
import requests
import time


def get_str_time(): 
    return datetime.datetime.utcnow().isoformat()
    
def import_to_db(csv):
    pass


def get_report(rid, token):
    print "Downloading report..."
    url = "https://api.appnexus.com/report-download?id={0}".format(rid)
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)

    print response

    data = response.text

    print data
    with open('logs/%s_network_analytics.csv'%(get_str_time()), 'wb') as fd:
        for chunk in response.iter_content(1024):
            fd.write(chunk)

    return data


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


def get_network_analytics():
    auth_url = "https://api.appnexus.com/auth"
    data = {"auth": {"username": "stats_api", "password": "API?1nsid3!"}}
    auth_request = requests.post(auth_url, data=json.dumps(data))
    response = json.loads(auth_request.content)

    try:
        token = response['response']['token']
    except:
        token = ''

    url = "https://api.appnexus.com/report"
    report_type = "network_analytics"
    report_data = {}

    columns = [
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
    ]

    report_data['report'] = {
        "report_type": report_type,
        "columns": columns,
        "timezone": "UTC",
        "report_interval": "last_hour",
        "format": "csv"
    }

    headers = {"Authorization": token, 'Content-Type': 'application/json'}

    r = requests.post(url, data=json.dumps(report_data), headers=headers)

    out = json.loads(r.content)
    
    with open('logs/%s_report_response.json'%(get_str_time()), 'wb') as f:
        f.write(r.content)

    report_id = out['response']['report_id']

    reports = get_report_status(report_id, token)

    print reports

get_network_analytics()