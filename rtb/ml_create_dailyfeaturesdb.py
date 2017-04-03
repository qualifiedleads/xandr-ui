from django.db import connection

def mlCreatePlacementDailyFeaturesDB():
    print "Database ml_placement_daily_features is filling"
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                    INSERT INTO ml_placement_daily_features(
                      placement_id,
                      day,
                      imps,
                      clicks,
                      total_convs,
                      imps_viewed,
                      view_measured_imps,
                      cost,
                      cpa,
                      ctr,
                      cvr,
                      cpc,
                      cpm,
                      view_rate,
                      view_measurement_rate,
                      adv_type)

                    SELECT
                      placement_id,
                      extract (dow from hour) "dow",
                      SUM(imps), SUM(clicks), SUM(total_convs), SUM(imps_viewed), SUM(view_measured_imps), SUM(cost),
                      case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end CPA,
                      case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end CTR,
                      case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end CVR,
                      case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end CPC,
                      case SUM(imps) when 0 then 0 else SUM(cost)::float/SUM(imps) end CPM,
                      case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)::float/SUM(view_measured_imps) end view_rate,
                      case SUM(imps) when 0 then 0 else SUM(view_measured_imps)::float/SUM(imps) end view_measurement_rate,
                      'ecommerceAd'
                    FROM
                      network_analytics_report_by_placement
                      join campaign
                        on network_analytics_report_by_placement.campaign_id = campaign.id
                        join advertiser
                          on advertiser.id=campaign.advertiser_id
                        where advertiser.ad_type='ecommerceAd'
                    group by
                      placement_id, extract (dow from hour)
                    ON CONFLICT (placement_id, day, adv_type)
                      DO UPDATE SET
                        imps = Excluded.imps,
                        clicks = Excluded.clicks,
                        total_convs = Excluded.total_convs,
                        imps_viewed = Excluded.imps_viewed,
                        view_measured_imps = Excluded.view_measured_imps,
                        cost = Excluded.cost,
                        cpa = Excluded.CPA,
                        ctr = Excluded.CTR,
                        cvr = Excluded.CVR,
                        cpc = Excluded.CPC,
                        cpm = Excluded.CPM,
                        view_rate = Excluded.view_rate,
                        view_measurement_rate = Excluded.view_measurement_rate;
                    """)

            cursor.execute("""
                    INSERT INTO ml_placement_daily_features(
                      placement_id,
                      day,
                      imps,
                      clicks,
                      total_convs,
                      imps_viewed,
                      view_measured_imps,
                      cost,
                      cpa,
                      ctr,
                      cvr,
                      cpc,
                      cpm,
                      view_rate,
                      view_measurement_rate,
                      adv_type)

                    SELECT
                      placement_id,
                      extract (dow from hour) "dow",
                      SUM(imps), SUM(clicks), SUM(total_convs), SUM(imps_viewed), SUM(view_measured_imps), SUM(cost),
                      case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end CPA,
                      case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end CTR,
                      case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end CVR,
                      case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end CPC,
                      case SUM(imps) when 0 then 0 else SUM(cost)::float/SUM(imps) end CPM,
                      case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)::float/SUM(view_measured_imps) end view_rate,
                      case SUM(imps) when 0 then 0 else SUM(view_measured_imps)::float/SUM(imps) end view_measurement_rate,
                      'leadGenerationAd'
                    FROM
                      network_analytics_report_by_placement
                      join campaign
                        on network_analytics_report_by_placement.campaign_id = campaign.id
                        join advertiser
                          on advertiser.id=campaign.advertiser_id
                        where advertiser.ad_type='leadGenerationAd'
                    group by
                      placement_id, extract (dow from hour)
                    ON CONFLICT (placement_id, day, adv_type)
                      DO UPDATE SET
                        imps = Excluded.imps,
                        clicks = Excluded.clicks,
                        total_convs = Excluded.total_convs,
                        imps_viewed = Excluded.imps_viewed,
                        view_measured_imps = Excluded.view_measured_imps,
                        cost = Excluded.cost,
                        cpa = Excluded.CPA,
                        ctr = Excluded.CTR,
                        cvr = Excluded.CVR,
                        cpc = Excluded.CPC,
                        cpm = Excluded.CPM,
                        view_rate = Excluded.view_rate,
                        view_measurement_rate = Excluded.view_measurement_rate;
                    """)

    except Exception, e:
        print "Failed to save training set " + str(e)
        return

    print "Database ml_placement_daily_features filled"