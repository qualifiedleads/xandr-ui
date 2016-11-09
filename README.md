## Django-angular application

#### Setup locally
````
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
ML commands
1. Create test set for learning
python manage.py mlcreatetestset
2. Learn k-means model
python manage.py mllearnsavemodel <test_type> <test_name>
valid test types:
  1) kmeans
  2) log - logistic regression
valid test names:
  1) ctr_viewrate (kmeans)
  2) ctr_cvr_cpc_cpm_cpa (kmeans, log)
3. Predict placement and save to database
python manage.py mlpredictkmeans <placement_id> <test_type> <test_name>
Example for one placement: python manage.py mlpredictkmeans 3898 kmeans ctr_cvr_cpc_cpm_cpa
Example for all placements: python manage.py mlpredictkmeans -1 log ctr_cvr_cpc_cpm_cpa
4. Create csv-file with prediction results
python manage.py mlcreatecsvresult
5. Check if placement good or bad
python manage.py mlcheckplacement <placement_id> <test_type> <test_name>
======================================
imp_tracker
1. Add new shedule jobs
python manage.py crontab add
python manage.py crontab show
2. To get the data manually
python manage.py imp_tracker '2016-10-10 22:00' '2016-10-21 23:00'
========================================
cron job
('* * * * *', 'rtb.crons.placement_state_cron.change_state_placement_by_cron_settings')
This task checks placement state in our base every minute and sends all changes to appnexus.

('*/15 * * * *', 'rtb.crons.placement_state_cron.platform_placement_targets')
This task updates our placements states (white/black) in datatable with changes of platform_placement_targets value, which we are getting from appnexus. 
This task runs every 15 minutes.

('* * * * *', 'rtb.crons.placement_state_cron.suspend_state_middleware_cron')
Cronjob finds placements with suspend state and changes their state in appnexus to exclude. 
This task runs every minute.

````