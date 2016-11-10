from metadata import meta
import django.db.models as django_types
import datetime
from pytz import utc
import re
import os, time
from functools import wraps
from django.http import HttpResponseForbidden
from models import FrameworkUser,MembershipUserToAdvertiser, Advertiser, Campaign, UserAdvertiserAccess

def clean_old_files(path):
    now = time.time()
    for f in os.listdir(path):
        fname = os.path.join(path, f)
        if os.stat(fname).st_mtime < now - 7 * 86400:
            os.remove(fname)

def get_current_time():
    return datetime.datetime.utcnow().replace(tzinfo=utc)

def get_all_classes_in_models(module):
    return [module.__dict__[k]
            for k in module.__dict__
            if isinstance(module.__dict__[k], django_types.base.ModelBase)]

# Getting column list, which is possible to send to report service
def get_column_list_for_report(ReportClass):
    if hasattr(ReportClass, 'api_columns'):
        return ReportClass.api_columns
    all_fields = [field.attname for field in ReportClass._meta.fields]
    name_fields = [field.name + '_name' for field in ReportClass._meta.fields if isinstance(field, django_types.ForeignObject)]
    meta_fields = [column['column'] for column in meta[ReportClass.api_report_name]['columns']]
    if hasattr(ReportClass, 'add_api_columns'):
        all_fields.extend(ReportClass.add_api_columns)
    return list((set(all_fields)|set(name_fields)) & set(meta_fields))


def not_none(o):
    return o or 0

def make_sum(dict1, dict2):
    res = {}
    # keys = set(dict1)|set(dict2)
    for k in dict1.keys():
        try:
            res[k] = not_none(dict1.get(k)) + not_none(dict2.get(k))
        except:
            pass
    return res

one_day = datetime.timedelta(days=1)

def parse_get_params(params,
                     field_list=['campaign', 'spend', 'conv', 'imp', 'clicks', 'cpc', 'cpm', 'cvr', 'ctr','view_measured_imps', 'view_rate', 'view_measurement_rate']):
    res = {}
    field_list_re = '|'.join(field_list)
    try:
        # res['from_date'] = datetime.date.fromtimestamp(int(params.get("from_date", params.get("from"))))
        res['from_date'] = datetime.date.fromtimestamp(int(params.get("from_date")))
    except:
        res['from_date'] = datetime.date.today() - one_day * 8
    try:
        # res['to_date'] = datetime.date.fromtimestamp(int(params.get("to_date", params.get("to"))))
        res['to_date'] = datetime.date.fromtimestamp(int(params.get("to_date")))
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
    res['section']=params.get('section','Placement')
    res['category']=params.get('category','Placement')
    return res

def check_user_advertiser_permissions(**field_names):
    def actual_decorator(func):
        @wraps(func)
        def new_func(request, *args, **kwargs):
            try:
                check_write = field_names.get('check_write')
                user = request.user
                assert user.is_authenticated()
                if user.is_superuser or user.is_staff:
                    assert not(user.is_staff and check_write)
                else:
                    advertiser_id = request.GET.get('advertiser_id') or \
                                    ('advertiser_id_num' in field_names and args[field_names['advertiser_id_num']]) or \
                                    ('advertiser_id_name' in field_names and kwargs[field_names['advertiser_id_name']])
                    if not advertiser_id:
                        campaign_id = request.GET.get('campaign_id') or \
                                      ('campaign_id_num' in field_names and args[field_names['campaign_id_num']]) or \
                                      ('campaign_id_name' in field_names and kwargs[field_names['campaign_id_name']])
                        camp = Campaign.objects.get(pk=campaign_id)
                        advertiser_id = camp.advertiser_id
                    if user.frameworkuser \
                            and user.frameworkuser.apnexus_user_id \
                            and user.frameworkuser.use_appnexus_rights:
                        assert not check_write or user.frameworkuser.appnexus_can_write
                        filter_param = {'user_id':user.frameworkuser.apnexus_user_id,'advertiser_id':advertiser_id}
                        membership_info = UserAdvertiserAccess.objects.filter(**filter_param)
                    else:
                        filter_param={'frameworkuser_id':user.pk, 'advertiser_id':advertiser_id}
                        if check_write:
                            filter_param['can_write']=True;
                        membership_info = MembershipUserToAdvertiser.objects.filter(filter_param)
                    assert membership_info.exists()
            except:
                return HttpResponseForbidden()
            return func(request, *args, **kwargs)
        return new_func
    return actual_decorator
