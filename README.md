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

=============================
ML commands
-----------------------------
1. Create features test set for placements on weekdays
python manage.py mlcreatetestset

2. Learn and save k-means model (create centroids for good/bad placements clusters)
python manage.py mllearnsavemodel

3. Predict clusters for all placements 
python manage.py mlpredictkmeans -1 

4. Predict clusters for one placement 
python manage.py mlpredictkmeans [placement_id] 

````
