from metadata import meta
import django.db.models as django_types
import datetime
from pytz import utc
import re

column_sets_for_reports = {
    "network_analytics": [
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
    "site_domain_performance_": [
        "day",
        "site_domain",
        "campaign",
        "line_item_id",
        "top_level_category",
        "second_level_category",
        "deal_id",
        "advertiser",
        "buyer_member_id",
        "operating_system",
        "supply_type",
        "mobile_application_id",
        "mobile_application_name",
        "mobile_application",
        "fold_position",
        "age_bucket",
        "gender",
        "is_remarketing",
        # "conversion_pixel_id" , probary pixel_id
        "booked_revenue",
        "clicks",
        "click_thru_pct",
        "convs_per_mm",
        "convs_rate",
        "cost_ecpa",
        "cost_ecpc",
        "cpm",
        "ctr",
        "imps",
        "media_cost",
        "post_click_convs",
        "post_click_convs_rate",
        "post_view_convs",
        "post_view_convs_rate",
        "profit",
        "profit_ecpm",
        "imps_viewed",
        "view_measured_imps",
        "view_rate",
        "view_measurement_rate",
    ]
}

def get_current_time():
    return datetime.datetime.utcnow().replace(tzinfo=utc)

def get_all_classes_in_models(module):
    return [module.__dict__[k]
            for k in module.__dict__
            if isinstance(module.__dict__[k], django_types.base.ModelBase)]

# Getting column list, which is possible to send to report service
def get_column_list_for_report(ReportClass):
    try:
        return column_sets_for_reports[ReportClass.api_report_name]
    except:
        pass
    all_fields = [field.name + '_id' if isinstance(field, django_types.ForeignObject) else field.name
                  for field in ReportClass._meta.fields]
    name_fields = [field.name + '_name' for field in ReportClass._meta.fields if isinstance(field, django_types.ForeignObject)]
    meta_fields = [column['column'] for column in meta[ReportClass.api_report_name]['columns']]

    return list((set(all_fields)|set(name_fields)) & set(meta_fields))


one_day = datetime.timedelta(days=1)


def parse_get_params(params, field_list=['campaign', 'spend', 'conv', 'imp', 'clicks', 'cpc', 'cpm', 'cvr', 'ctr']):
    res = {}
    field_list_re = '|'.join(field_list)
    try:
        res['from_date'] = datetime.date.fromtimestamp(int(params["from_date"]))
    except:
        res['from_date'] = datetime.date.today() - one_day * 8
    try:
        res['to_date'] = datetime.date.fromtimestamp(int(params["to_date"]))
    except:
        res['to_date'] = datetime.date.today() - one_day * 1
    try:
        res['advertiser_id'] = int(params['advertiser_id'])
    except:
        res['advertiser_id'] = 992089
    try:
        res['skip'] = int(params['skip'])
    except:
        res['skip'] = 0
    try:
        res['take'] = int(params['take'])
    except:
        res['take'] = 20
    try:
        res['order'] = re.match(r"^(desc|asc)$", params['order']).group(1)
    except:
        res['order'] = 'desc'
    try:
        res['sort'] = re.match(r"^({0})$".format(field_list_re), params['sort']).group(1)
    except:
        res['sort'] = 'campaign'
    try:
        fields = params.get('stat_by', params.get('by', ''))
        m = re.match(r"^({0})(?:,({0}))*$".format(field_list_re), fields)
        res['stat_by'] = m.group(0).split(',')
    except:
        res['stat_by'] = ''
    try:
        res['filter'] = ' '.join(params.getlist('filter'))
    except:
        res['filter'] = ''
    return res
