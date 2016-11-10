from django.db import connection

def mlRefreshViewFullPlacementsDataCron():
    try:
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW ml_view_full_placements_data")
    except Exception, e:
        print "Can't update view" + str(e)
        return 1