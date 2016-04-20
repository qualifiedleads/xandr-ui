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
        "report_interval": "<?php echo $interval;?>",
        "filters": [
            {"campaign_id":"<?php echo $campaign_id;?>"}
        ],
        "group_filters": [
            {"post_click_convs":{"value":1,"operator":">="}}
        ],
        "format": "csv"
    }
}