from datetime import datetime
from datetime import timedelta

#NEW TRY
from models.ml_kmeans_model import MLPlacementDailyFeatures
from models.network_analitics_models import NetworkAnalyticsReport_ByPlacement
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField

def mlCreatePlacementDailyFeaturesDB():
    queryResult = NetworkAnalyticsReport_ByPlacement.objects.order_by('placement_id', 'hour')
    curPlacement = queryResult[0].placement_id #get first placement for the loop
    pastHour = queryResult[0].hour  # to see day changing

    curPlacementDailyFeatures = MLPlacementDailyFeatures()
    curPlacementDailyFeatures.imps = 0
    curPlacementDailyFeatures.clicks = 0
    curPlacementDailyFeatures.total_convs = 0
    curPlacementDailyFeatures.imps_viewed = 0
    curPlacementDailyFeatures.view_measured_imps = 0
    curPlacementDailyFeatures.cost = 0
    nDay = 1

    testIter = 0;
    dayGap = False

    #print "1"

    #SQL fast
    try:
        trainingSet = MLPlacementDailyFeatures.objects.raw("""
        INSERT INTO ml_placement_daily_features (placement_id,day,imps,clicks,total_convs,imps_viewed,view_measured_imps,cost,cpa,ctr,view_rate,view_measurement_rate)
        SELECT placement_id, extract (DAY from hour) "day", SUM(imps),SUM(clicks),SUM(total_convs),SUM(imps_viewed),SUM(view_measured_imps),SUM(cost),
        case SUM(total_convs) when 0 then 0 else SUM(cost)/SUM(total_convs) end CPA,
        case SUM(imps) when 0 then 0 else SUM(clicks)/SUM(imps) end CTR,
        case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)/SUM(view_measured_imps) end view_rate,
        case SUM(imps) when 0 then 0 else SUM(view_measured_imps)/SUM(imps) end view_measurement_rate
        FROM network_analytics_report_by_placement
        group by placement_id, extract (DAY from hour);"""
        )
        #print trainingSet[0]


    except Exception, e:
        print "Failed to save training set " + str(e)
    #/SQL fast


    """for row in queryResult.iterator():
        #print "2"
        if testIter > 1000:
            break

        if curPlacement == row.placement_id and dayGap:
            continue

        if curPlacement != row.placement_id and dayGap:
            dayGap = False
            curPlacement = row.placement_id
            pastHour = row.hour


        if curPlacement != row.placement_id:#adding last day of the placement to the DB
            curPlacementDailyFeatures.day = nDay
            if curPlacementDailyFeatures.total_convs != 0:
                curPlacementDailyFeatures.cpa = float(curPlacementDailyFeatures.cost) / float(curPlacementDailyFeatures.total_convs)
            else:
                curPlacementDailyFeatures.cpa = 0

            if curPlacementDailyFeatures != 0:
                curPlacementDailyFeatures.ctr = float(curPlacementDailyFeatures.clicks) / float(curPlacementDailyFeatures.imps)
            else:
                curPlacementDailyFeatures.ctr = 0

            if curPlacementDailyFeatures.view_measured_imps != 0:
                curPlacementDailyFeatures.view_rate = float(curPlacementDailyFeatures.imps_viewed) / float(curPlacementDailyFeatures.view_measured_imps)
            else:
                curPlacementDailyFeatures.view_rate = 0

            if curPlacementDailyFeatures.imps != 0:
                curPlacementDailyFeatures.view_measurement_rate = float(curPlacementDailyFeatures.view_measured_imps) / float(curPlacementDailyFeatures.imps)
            else:
                curPlacementDailyFeatures.view_measurement_rate = 0

            curPlacementDailyFeatures.placement_id = curPlacement

            if nDay > 2:

                try:
                    curPlacementDailyFeatures.save()
                except Exception, e:
                    print "Failed to insert data about placement: " + str(e)


            #TEST
            testQuery = NetworkAnalyticsReport_ByPlacement.objects.filter(placement_id=curPlacement)
            print "Placement " + str(curPlacement)
            for tt in testQuery:
                print str(tt.hour) + " " + str(tt.imps)

            testQuery = MLPlacementDailyFeatures.objects.filter(placement_id=curPlacement)
            print "In our DB"
            for tt in testQuery:
                print str(tt.day) + " " + str(tt.imps)
            #TEST
            curPlacementDailyFeatures = MLPlacementDailyFeatures()

            curPlacementDailyFeatures.imps = row.imps
            curPlacementDailyFeatures.clicks = row.clicks
            curPlacementDailyFeatures.total_convs = row.total_convs
            curPlacementDailyFeatures.imps_viewed = row.imps_viewed
            curPlacementDailyFeatures.view_measured_imps = row.view_measured_imps
            curPlacementDailyFeatures.cost = row.cost

            if nDay > 2:
                testIter += 1

            pastHour = row.hour
            nDay = 1
            curPlacement = row.placement_id


            continue


        if row.hour.day - pastHour.day == 0:#
            curPlacementDailyFeatures.imps += row.imps
            curPlacementDailyFeatures.clicks += row.clicks
            curPlacementDailyFeatures.total_convs += row.total_convs
            curPlacementDailyFeatures.imps_viewed += row.imps_viewed
            curPlacementDailyFeatures.view_measured_imps += row.view_measured_imps
            curPlacementDailyFeatures.cost += row.cost
            pastHour = row.hour

        if row.hour.day - pastHour.day > 0: #adding a current day, go to the next
            curPlacementDailyFeatures.day = nDay
            if curPlacementDailyFeatures.total_convs != 0:
                curPlacementDailyFeatures.cpa = float(curPlacementDailyFeatures.cost) / float(curPlacementDailyFeatures.total_convs)
            else:
                curPlacementDailyFeatures.cpa = 0

            if curPlacementDailyFeatures != 0:
                curPlacementDailyFeatures.ctr = float(curPlacementDailyFeatures.clicks) / float(curPlacementDailyFeatures.imps)
            else:
                curPlacementDailyFeatures.ctr = 0

            if curPlacementDailyFeatures.view_measured_imps != 0:
                curPlacementDailyFeatures.view_rate = float(curPlacementDailyFeatures.imps_viewed) / float(curPlacementDailyFeatures.view_measured_imps)
            else:
                curPlacementDailyFeatures.view_rate = 0

            if curPlacementDailyFeatures.imps != 0:
                curPlacementDailyFeatures.view_measurement_rate = float(curPlacementDailyFeatures.view_measured_imps) / float(curPlacementDailyFeatures.imps)
            else:
                curPlacementDailyFeatures.view_measurement_rate = 0

            curPlacementDailyFeatures.placement_id = curPlacement

            if nDay > 2:
                try:
                    curPlacementDailyFeatures.save()#save current day
                except:
                    print "Failed to insert data about placement: " + str(e)

            if row.hour.day - pastHour.day > 1:#day gap
                nDay = 1
                dayGap = True;
                if nDay > 2:
                    testIter += 1
                pastHour = row.hour

            else:#next day
                curPlacementDailyFeatures = MLPlacementDailyFeatures()

                nDay += 1
                pastHour = row.hour

                curPlacementDailyFeatures.imps = row.imps
                curPlacementDailyFeatures.clicks = row.clicks
                curPlacementDailyFeatures.total_convs = row.total_convs
                curPlacementDailyFeatures.imps_viewed = row.imps_viewed
                curPlacementDailyFeatures.view_measured_imps = row.view_measured_imps
                curPlacementDailyFeatures.cost = row.cost

"""
    print "Database ml_placement_daily_features filled"