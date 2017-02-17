from django.db import connection
from rtb.models.placement_state import LastModified
import datetime
from django.utils import timezone
from datetime import timedelta


def mlRefreshViewFullPlacementsDataCron():
    try:
        change_state = LastModified.objects.filter(type='mlRefreshViewFullPlacementsDataCron')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[
                0].date >= timedelta(
                    minutes=15):
                LastModified.objects.filter(type='mlRefreshViewFullPlacementsDataCron').delete()
            else:
                print "mlRefreshViewFullPlacementsDataCron is busy, wait..."
                return None
        LastModified(type='mlRefreshViewFullPlacementsDataCron',
                     date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()

        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW ml_view_full_placements_data")
        LastModified.objects.filter(type='mlRefreshViewFullPlacementsDataCron').delete()
    except Exception, e:
        LastModified.objects.filter(type='mlRefreshViewFullPlacementsDataCron').delete()
        print "Can't update view" + str(e)
        return 1

