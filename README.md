# AppNexus 'rainmaker' is a Co-Pilot for your (buy) campaigns running on AppNexus's DSP

This platform is an *additional* UI to the Appnexus console. It's built on top of the Appnexus buy-side API.

It helps media-buyers optimise campaigns based on [CPA](https://en.wikipedia.org/wiki/Cost_per_action) by automatically collecting the data via API and displays it in a Pivottable.

![Optimise your AppNexus campaigns rapidly based on CVR](https://i.imgur.com/NLEiv6f.png)
_See Conversions, CPA, CTR, etc per placement from your Appnexus campaigns. Blacklist under-performing campaigns with one click._


## Background

The current Appnexus UI (or "console" as they call it) is built _by_ engineers, _for_ engineers. 
To a media-buyer, who is responsible for performance results (eg: conversions, leads, ecomm sales) this is very poor UX. 
It drains hours and patience.
The purpose of this UI is to be a simple "co-pilot" so you don't need to use excel so much and can quickly:

   a) see what's converting, at what cost
   b) white-list or black-list placements,
   c) pause (blacklist for a set time, then reactivate) placements
   d) drill-down on **what is converting** and see: creative, carrier, device-type, OS, etc.

## Accuracy

The system uses the AppNexus reporting API to collect it's data by default. The data is pulled via API and stored in a PostGreSQL DB.
Reporting sometimes comes after 6 hours from Appnexus. This delay can kill your campaign.
For this we additionally built :
1. impression tracker
2. click tracker
3. conversion tracker
We will roll-out the release of the trackers shortly.

You will need to set this up on top of your own domain and get it approved by appnexus support.
1 and 2 above need to be submitted at least 48 hrs before going live.

## Features
- Automatic Pivot-tables: CPA's are automatically calculated on yesterday's perfomance. 
- "CPA-buckets" are generated per: placement/domain, creative, creative size, Carrier, Seller/network/Exchange
- Create your own Rules to manage AppNexus' traffic, auto-blacklist based on CPM, CTR, CPA, CPC

## Data set

Optimisation is **per placement**, not per domain.

## Reciprocity

As soon as you set a state in the co-pilot, it will be reflected in the Appnexus console (give or take a minute. And vice-versa: if you blacklist a specific placement in console, it will get displayed as such in the Co-Pilot.

# Owner's manual
Please see the wiki.

# License
[GPL v3](https://github.com/qualifiedleads/appnexus-co-pilot/blob/master/LICENSE)

# How to install - Technical


### Django-angular application

#### Setup locally

1. Create virtutalenv and install requirements
pip install -r requirements.txt
python manage.py runserver

2. Migrating tables

python manage.py migrate

3. Shedule jobs
python manage.py crontab add
On Windows run  Job_install.bat

4. To run export data proc manually:
python manage.py crontab show

look at task hash code (now there is exact one task)

python manage.py crontab run <task_id>

5. To load all data for the last month, type:
python manage.py loadreportdata
To load data for specifed day (date format <Year>-<Month>-<Day>):
python manage.py loadreportdata 2016-05-31

6. Create service table for cache:
python manage.py createcachetable rtb_cache_table

7. For create superuser, run
python manage.py createsuperuser
======================================

## ML 

Kmeans modeling has been started, but **is not complete**. The intention is to predict whether or not any particular placement will stand a good chance of getting a click and conversion.

### ML commands

1. Create test set for learning
python manage.py mlcreatetestset
2. Learn k-means model
python manage.py mllearnsavemodel <test_type> <test_name> <advertiser_type>
valid test types:
  1) kmeans
  2) log - logistic regression
valid test names:
  1) ctr_viewrate (kmeans)
  2) ctr_cvr_cpc_cpm_cpa (kmeans, log)
valid advertiser type:
  1) ecommerceAd (kmeans)
  2) leadGenerationAd (kmeans)
3. Predict placement and save to database
python manage.py mlpredictkmeans <placement_id> <test_type> <test_name>
Example for one placement: python manage.py mlpredictkmeans 3898 kmeans ctr_cvr_cpc_cpm_cpa
Example for all placements: python manage.py mlpredictkmeans -1 log ctr_cvr_cpc_cpm_cpa
Valid test types:
  1) kmeans;
  2) log;
  3) tree - classifier decision tree
4. Create csv-file with prediction results
python manage.py mlcreatecsvresult
5. Check if placement good or bad
python manage.py mlcheckplacement <placement_id> <test_type> <test_name>
======================================

## imp_tracker
1. Add new shedule jobs
python manage.py crontab add
python manage.py crontab show
2. To get the data manually
python manage.py imp_tracker '2016-10-10 22:00' '2016-10-21 23:00' Impression/Click/Conversion
                    
####  Tables in database
rtb_impression_tracker — table for impressions from imp_tracker.

rtb_impression_tracker_placement — table for placement and domain from table  rtb_impression_tracker.

rtb_impression_tracker_placement_domain — table for placement and domain from table rtb_impression_tracker_placement . Every one placement have your domain or parts domain's level 

rtb_click_tracker — table for clicks from imp_tracker. With fields:
CpId - ${ADV_ID} 
AdvId - ${CP_ID} 
CreativeId - ${CREATIVE_ID} 
AuctionId - ${AUCTION_ID}

rtb_conversion_tracker — table for conversions from imp_tracker. With fields
CpId - ${ADV_ID} 
AdvId - ${CP_ID} 
CreativeId - ${CREATIVE_ID} 
AuctionId - ${AUCTION_ID}
========================================

cron jobs
('* * * * *', 'rtb.crons.placement_state_cron.change_state_placement_by_cron_settings')
This task checks placement state in our base every minute and sends all changes to appnexus.

('*/15 * * * *', 'rtb.crons.placement_state_cron.platform_placement_targets')
This task updates our placements states (white/black) in datatable with changes of platform_placement_targets value, which we are getting from appnexus. 
This task runs every 15 minutes.

('* * * * *', 'rtb.crons.placement_state_cron.suspend_state_middleware_cron')
Cronjob finds placements with suspend state and changes their state in appnexus to exclude. 
This task runs every minute.

('0 */4 * * *', 'rtb.crons.imp_tracker_cron.get')
This task loadsdata from our impression tracker.

('5 0 * * *', 'rtb.cron.dayly_task')
This task loads reports and entities fromAppnexus.

('0 */1 * * *', 'rtb.crons.ml_predict_new_placements_cron.mlPredictNewPlacementsCron')
This task predicts GOO/BAD clustersfor new placements.

('0 6 * * 7', 'rtb.crons.ml_refresh_view_full_placements_data_cron.mlRefreshViewFullPlacementsDataCron')
This task updates materialized view for ML purposes.

('0 */1 * * *', 'rtb.crons.campaign_rules_cron.checkRulesByCron')
Those rules check condition and change placements states
