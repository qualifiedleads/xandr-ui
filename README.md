# Xandr 'rainmaker' is a Co-Pilot for your (buy) campaigns running on Xandr DSP

This platform is an *additional* UI to the ~~Appnexus~~ Xandr console. It's built on top of the ~~Appnexus~~ Xandr buy-side API.

It helps media-buyers optimise campaigns based on [CPA](https://en.wikipedia.org/wiki/Cost_per_action) by automatically collecting the data via API and displays it in a Pivottable.

![Optimise your AppNexus campaigns rapidly based on CVR](https://i.imgur.com/NLEiv6f.png)
_fig. 1 See Conversions, CPA, CTR, etc per placement from your Appnexus campaigns. Blacklist under-performing campaigns with one click._


## Background

The Xandr UI (or "console" as they call it) is built _by_ engineers, _for_ engineers. Even the latest attempts to pretty it up have not changed it into a Buyers platform
To a media-buyer, who is responsible for performance results (eg: conversions, leads, ecomm sales) this is very poor UX. 
It drains hours and patience.
The purpose of this UI is to be a simple "co-pilot" so you don't need to use excel so much and can quickly:

   * see what's converting, at what cost
   * white-list or black-list placements,
   * pause (blacklist for a set time, then reactivate) placements
   * drill-down on **what is converting** and see: creative, carrier, device-type, OS, etc.

## Accuracy

The system uses the AppNexus reporting API to collect it's data by default. The data is pulled via API and stored in a PostGreSQL DB.
Reporting sometimes comes after 6 hours from Xandr. This delay can kill your campaign.
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
- Placement ID' matching
Placement ID's are core to optimising campaigs in AppNexus. They are the ID's of individual placements, either on a page or site-section. When you run an "Analytics Report" in AppNexus you can retrieve "placement ID", but not domain, eg:
![in AppNexus you can retrieve "placement ID", but not domain, eg:](https://i.imgur.com/WKddSc8.jpg)
_Appnexus Analytics Report_

Then if you run a "Site Domain Performance" report you can pull the Seller and Domain/App, but not the placement ID, eg: ![if you run a "Site Domain Performance" report you can pull the Seller and Domain/App, but not the placement ID, eg:](https://i.imgur.com/p0jr7OD.jpg)
_Appnexus Site Domain Performance report_

However you can't pull a report to see both Domain and placement ID together.
When it comes to CPA, this can make a huge difference. Some specific placements on a site are never profitable. But that doesn't mean the entire domain is not profitable.

![](https://i.imgur.com/uqvsNxt.jpg)
_The APNX Rainmaker combines the two reports pulled via API into one as much as possible, based on the data compiled via the API's, and separate impression tracker, click tracker and conversion tracker, like this_


## Data set

Optimisation is **per placement**, not per domain.

## Reciprocity

As soon as you set a state in the co-pilot, it will be reflected in the Appnexus console (give or take a minute. And vice-versa) if you blacklist a specific placement in console, it will get displayed as such in the UI.

Click "blacklist" inside the Rainmaker UI like this ![Click "blacklist" inside the Rainmaker UI](https://i.imgur.com/JGNx963.jpg)
And a few seconds later it is reflected in APNX Console ![As shown in APNX Console](https://i.imgur.com/eKSbg17.jpg)
Vice-versa, also works.
Note: that AppNexus doesn't recognise its own placement ID's when you import it. Hence it always marks it as "unknown" or "Undisclosed Placement". This doesn't affect your campaign though. The setting is still obeyed.

## Optimisation
The optimisation that you do remains in the scope of that Campaign, ie: 
 - Blacklist = block that placement ID _in this campaign_ . Blacklisting one publisher doesn't mean it gets blacklisted across other campaigns.
 - Whitelist = No matter what you do, this placement is immune, ie: Always advertise on this placement ID _in this campaign_ .
 - Suspend = *Temporarily* block this placement ![Suspend = *Temporarily* block this placement ](https://i.imgur.com/nyLeRug.jpg)

## Auto-Rules
Building rules that autimatically edit your campaign settings is support. To have this work accurately you can not rely on the APNX Reporting API, as it has delays of 6 hours. You must use the impression tracker module and conversion tracker module.
Building a rule example:
![IF impressions reach 1000, AND clicks are 0, THEN blacklist](https://i.imgur.com/VNtEFSo.jpg)
_This Rule says: IF impressions reach 1000, AND clicks are 0, THEN blacklist._

How to generate this example Rule
- set a benchmark such as '>= 1000 impressions'
![auto rule setup](https://i.imgur.com/s2AGU3T.jpg)
- click the 'F+' button to add a field
- set AND
- set '<= 0 clicks'
- THEN Blacklist
- Save Rule

You can also add a *Group of Fields*, which will create a bracket that will get calculated first, following standard arithmetic [Orders of Operation](https://en.wikipedia.org/wiki/Order_of_operations)

![Group of fields example](https://i.imgur.com/UvCITwU.jpg)_Group of fields example_

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


Known peculiarities:
============================

### After "Advertiser account" has been selected in the Home page, the `Go` button fails
![](https://i.imgur.com/QFELHy7.jpg)
The 'Advertiser must first be configured in the Admin panel. Assign an `ad_type` field equals to `leadGenerationAd` or `videoAds` in database, like so:
!['Advertiser must be configured in the Admin panel first](https://i.imgur.com/VsNMhiu.jpg)
