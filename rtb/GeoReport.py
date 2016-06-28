from cron import analize_csv, get_current_time
from pytz import utc

def load_geo_report(day=None):
    today = get_current_time().date().replace(tzinfo=utc)
    print today


class GeoAnaliticsReport(models.Model):
    month = date  # Yes	The year and month in which the auction took place.
    day = date  # Yes	The year, month, and day in which the auction took place.
    member_id = int  # Yes	The ID of the member.
    advertiser_currency = string  # Yes	The type of currency used by the advertiser.
    insertion_order_id = int  # Yes	The insertion order ID.
    campaign_id = int  # Yes	The campaign ID.
    campaign_name = string  # No	The name of the campaign associated with the auction.
    campaign = string  # No	The campaign name and ID associated with the auction, in the format "South Texas Ford Drivers (123)"
    advertiser_id = int  # Yes	The advertiser ID. If the value is 0, either the impression was purchased by an external buyer, or a default or PSA was shown. For more information on defaults and PSAs, see Network Reporting.
    line_item_id = int  # Yes	The line item ID.
    advertiser_name = string  # No	The name of the advertiser.
    advertiser = string  # No	The advertiser name and ID, in the format "Great Advertiser (456)".
    campaign_code = string  # No	The user-assigned code used to identify the campaign.
    advertiser_code = string  # No	The user-assigned code associated with the advertiser.
    geo_country_code = string  # Yes	The country code of the user's location as defined by the Country Service.
    geo_country_id = int  # Yes	The country ID of the user's location as defined by the Country Service. 250 is shown in cases where we don't know the country or if the country doesn't map correctly to a location in our database.
    geo_region_code = string  # No	The region code of the user's location as defined by the Region Service.
    geo_region_id = int  # Yes	The region ID of the user's location as defined by the Region Service. 4291 is shown in cases where we don't know the region or if the region doesn't map correctly to a location in our database.
    geo_dma_id = int  # Yes	"The ID of the user's demographic area location as defined by the Demographic Area Service.
    # Why am I seeing a DMA ID of 1?
    # Our reporting derives DMA from the city logged for the auction. However, our geo provider is sometimes unable to determine a city from the IP address associated with the impression, even when DMA is determined. Therefore, there are cases where a campaign targeting a specific DMA has impressions in reporting showing a DMA of 1."
    geo_dma_name = string  # No	The name of the user's demographic area location as defined by the Demographic Area Service.
    insertion_order_name = string  # No	The name of the insertion order.
    insertion_order_code = string  # No	The user-defined code associated with the insertion order.
    line_item_name = string  # No	The name of the line item.
    line_item_code = string  # No	The user-defined code associated with the line item.
    geo_country_name = string  # No	The name of the user's country, as defined by the Country Service.
    geo_region_name = string  # No	The name of the region of the user's location as defined by the Region Service.
    insertion_order = string  # No	The insertion order name and ID, in the format "Midwest Winter Getaways (789)".
    line_item = string  # No	The line item name and ID, in the format "Kansas City Winter Commuters (314)".
    geo_country = string  # No	The country name and code where the user is located, in the format "France (FR)". The string "250" can appear in cases where we don't know the country or if the country doesn't map correctly to a location in our database.
    geo_region = string  # No	The region name and country code of the user's location , in the format "Bremen (DE)". The string  "4192"  can appear in cases where we don't know the region/state or if the region/state doesn't map correctly to a location in our database.
    geo_dma = string  # No	The name and ID of the demographic area where the user is located, in the format "New York NY (501)". The string "unknown values (-1)" can appear in cases where we don't know the demographic area or if the demographic area doesn't map correctly to a location in our database.
    pixel_id = int  # Yes	"The unique identification number of the conversion pixel.
    # Note: This dimension will return a maximum of 10 conversion pixels. Also, you can filter by no more than 10 conversion pixels. Although pixel_id is groupable, we do not recommend that you group by this dimension since doing so will cause conversion events to then be shown in separate rows from impression and click events. We generally assume you want to view all of these events in a single row so as to be able to retrieve accurate and aggregated values for conversion rate and cost-per-conversion calculations. As a result, we instead recommend that you filter by pixel_id so you can retrieve conversion counts and related metrics for your most relevant pixel ids."


    imps = int  # imps	The total number of impressions (served and resold).
    clicks = int  # clicks	The total number of clicks across all impressions.
    cost = money  # cost	The total cost of the inventory purchased.
    booked_revenue = money  # booked_revenue	The total revenue booked through direct advertisers (line item).
    cpm = money  # cpm	The cost per one thousand impressions.
    total_convs = int  # total_convs	The total number of post-view and post-click conversions.
    convs_rate = double  # total_convs / imps	The ratio of conversions to impressions.
    post_view_convs = int  # post_view_convs	The total number of recorded post-view conversions.
    post_click_convs = int  # post_click_convs	The total number of recorded post-click conversions.
    profit = money  # booked_revenue - media_cost	The total revenue minus the cost.
    click_thru_pct = double  # (clicks / imps) x 100	The rate of clicks to impressions, expressed as a percentage.
    external_imps = int  # external_imps	The number of external (non-network) impressions.
    external_clicks = int  # external_clicks	The number of external (non-network) clicks.
    booked_revenue_adv_curr = money  # booked_revenue_adv_curr	The total revenue booked through a direct advertiser, expressed in the currency of that advertiser.
