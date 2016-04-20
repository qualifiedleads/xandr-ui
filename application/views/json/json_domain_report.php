{
    "report":
    {
        "report_type": "site_domain_performance",
        "columns": [
            "site_domain",
            "cost_ecpa",
            "post_click_convs",
            "post_view_convs",
            "media_cost"
        ],
        "start_date": "<?php echo $start_date;?>",
        "end_date": "<?php echo $end_date;?>",
        "filters": [
            {"campaign_id":"<?php echo $campaign_id;?>"}
        ],
        "group_filters": [
            {"media_cost":{"value":<?php echo $media_cost['value'];?>,"operator":"<?php echo $media_cost['operator'];?>"}}
        ],
        "format": "csv"
    }
}