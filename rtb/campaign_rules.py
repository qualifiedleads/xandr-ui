from models.models import Campaign, Profile, LastToken
from django.utils import timezone
from datetime import timedelta
import json
import datetime
import pytz


def checkRules(campaign_id, rules):
    try:
        print "Yeeehooo"
        
    except Exception, e:
        print 'Error: ' + str(e)
        return 503


