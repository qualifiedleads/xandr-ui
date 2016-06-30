from metadata import meta
import django.db.models as django_types

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
    "site_domain_performance": [
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


# Getting column list, which is possible to send to report service
def get_column_list_for_report(ReportClass):
    try:
        return column_sets_for_reports[ReportClass.api_report_name]
    except:
        pass
    all_fields = [field.name + '_id' if isinstance(field, django_types.ForeignKey) else field.name
                  for field in ReportClass._meta.fields]
    meta_fields = (column['column'] for column in meta[ReportClass.api_report_name]['columns'])
    return list(set(all_fields) & set(meta_fields))
