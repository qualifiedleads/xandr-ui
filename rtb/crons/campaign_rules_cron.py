from rtb.campaign_rules import checkRules
from rtb.models.placement_state import LastModified
import datetime
from django.utils import timezone
from datetime import timedelta


def checkRulesByCron():
    try:
        change_state = LastModified.objects.filter(type='checkRulesByCron')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[
                0].date >= timedelta(
                    minutes=15):
                LastModified.objects.filter(type='checkRulesByCron').delete()
            else:
                print "checkRulesByCron is busy, wait..."
                return None
        LastModified(type='checkRulesByCron',
                     date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()

        checkRules()

        LastModified.objects.filter(type='checkRulesByCron').delete()
    except Exception, e:
        LastModified.objects.filter(type='checkRulesByCron').delete()
        print 'Cron job - suspend_state_middleware_cron Error: ' + str(e)
