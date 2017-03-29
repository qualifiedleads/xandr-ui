from rtb.placement_state import PlacementState
from rtb.models.placement_state import LastModified
import datetime
from django.utils import timezone
from datetime import timedelta

def suspend_state_middleware_cron():
    try:
        change_state = LastModified.objects.filter(type='suspend_state_middleware_cron')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[
                0].date >= timedelta(
                    minutes=15):
                LastModified.objects.filter(type='suspend_state_middleware_cron').delete()
            else:
                print "suspend_state_middleware_cron is busy, wait..."
                return None
        LastModified(type='suspend_state_middleware_cron',
                     date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()

        state = PlacementState(None, None)
        state.suspend_state_middleware()

        LastModified.objects.filter(type='suspend_state_middleware_cron').delete()
    except Exception, e:
        LastModified.objects.filter(type='suspend_state_middleware_cron').delete()
        print 'Cron job - suspend_state_middleware_cron Error: ' + str(e)


def platform_placement_targets():
    try:
        change_state = LastModified.objects.filter(type='platform_placement_targets')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[
                0].date >= timedelta(
                    minutes=15):
                LastModified.objects.filter(type='platform_placement_targets').delete()
            else:
                print "platform_placement_targets is busy, wait..."
                return None
        LastModified(type='platform_placement_targets',
                     date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()

        state = PlacementState(None, None)
        state.placement_targets_list()

        LastModified.objects.filter(type='platform_placement_targets').delete()
    except Exception, e:
        LastModified.objects.filter(type='platform_placement_targets').delete()
        print 'Cron job - platform_placement_targets Error: ' + str(e)

def change_state_placement_by_cron_settings():
    try:
        change_state = LastModified.objects.filter(type='change_state_placement_by_cron_settings')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[
                0].date >= timedelta(
                    minutes=15):
                LastModified.objects.filter(type='change_state_placement_by_cron_settings').delete()
            else:
                print "change_state_placement_by_cron_settings is busy, wait..."
                return None
        LastModified(type='change_state_placement_by_cron_settings',
                     date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()

        state = PlacementState(None, None)
        state.change_state_placement_by_cron()

        LastModified.objects.filter(type='change_state_placement_by_cron_settings').delete()
    except Exception, e:
        LastModified.objects.filter(type='change_state_placement_by_cron_settings').delete()
        print 'Cron job - change_state_placement_by_cron_settings Error: ' + str(e)
