from datetime import datetime
from datetime import timedelta

#OLD ORIGINAL
"""class Placement:
    imps = 0
    clicks = 0
    cost = 0
    conversions = 0
    imps_viewed = 0
    view_measured_imps = 0

    cpa = 0
    ctr = 0
    view_rate = 0
    view_measurement_rate = 0


connect = psycopg2.connect(database="testPlacementBase", user="postgres", host="localhost", password="pRT2q49")
cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)  # open database connection

# cursor.execute("SELECT hour FROM network_analytics_report_by_placement WHERE id=41401954;")
# currPlacement=6411742

cursor.execute(
    "SELECT MIN(placement_id) AS minplace,MAX(placement_id) AS maxplace FROM network_analytics_report_by_placement;")

row = cursor.fetchone()

minPlacement = row['minplace']

maxPlacement = row['maxplace']
# maxPlacement=minPlacement+5

dbDateFormat = "%Y-%m-%d"
nDay = 0

recognitionBaseConnect = psycopg2.connect(database="RecognitionInfo", user="postgres", host="localhost",
                                          password="pRT2q49")
recognitionBaseCursor = recognitionBaseConnect.cursor()

for i in range(minPlacement, maxPlacement):
    cursor.execute(
        "SELECT hour,imps,clicks,cost,total_convs,imps_viewed,view_measured_imps FROM network_analytics_report_by_placement WHERE placement_id=%s;",
        (i,))

    row = cursor.fetchone()
    tempTime = None

    allDays = {}
    sortedDays = []

    while row is not None:

        temp = str(row['hour']).split()
        if temp[0] not in allDays:
            allDays[temp[0]] = Placement()
            # sortedDays.append(temp[0])
            sortedDays.append(datetime.strptime(temp[0], dbDateFormat))

        allDays[temp[0]].imps += row['imps']
        allDays[temp[0]].clicks += row['clicks']
        allDays[temp[0]].cost += row['cost']
        allDays[temp[0]].conversions += row['total_convs']
        allDays[temp[0]].imps_viewed += row['imps_viewed']
        allDays[temp[0]].view_measured_imps += row['view_measured_imps']

        row = cursor.fetchone()

    if len(sortedDays) == 0:
        continue

    for time, placement in allDays.iteritems():
        try:
            placement.cpa = float(placement.cost) / float(placement.conversions)
        except ZeroDivisionError:
            placement.cpa = 0

        try:
            placement.ctr = float(placement.clicks) / float(placement.imps)
        except ZeroDivisionError:
            placement.ctr = 0

        try:
            placement.view_rate = float(placement.imps_viewed) / float(placement.view_measured_imps)
        except ZeroDivisionError:
            placement.view_rate = 0

        try:
            placement.view_measurement_rate = float(placement.view_measured_imps) / float(placement.imps)
        except ZeroDivisionError:
            placement.view_measurement_rate = 0

    sortedDays.sort()

    prevDate = None
    nowDate = None
    currDayData = allDays[sortedDays[0].strftime(dbDateFormat)]

    try:
        recognitionBaseCursor.execute(
            "INSERT INTO placement_daily_features (day,placement_id,imps,clicks,cost,total_convs,imps_viewed,view_measured_imps,view_measurement_rate,view_rate,cpa,ctr) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (1, i, currDayData.imps, currDayData.clicks, currDayData.cost, currDayData.conversions,
             currDayData.imps_viewed, currDayData.view_measured_imps, currDayData.view_measurement_rate,
             currDayData.view_rate, currDayData.cpa, currDayData.ctr))
        recognitionBaseConnect.commit()
    except:
        pass

    for j in range(1, len(sortedDays)):
        if sortedDays[j] - sortedDays[j - 1] == timedelta(days=1):
            currDayData = allDays[sortedDays[j].strftime(dbDateFormat)]
            nDay = j + 1
            try:
                recognitionBaseCursor.execute(
                    "INSERT INTO placement_daily_features (day,placement_id,imps,clicks,cost,total_convs,imps_viewed,view_measured_imps,view_measurement_rate,view_rate,cpa,ctr) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (nDay, i, currDayData.imps, currDayData.clicks, currDayData.cost, currDayData.conversions,
                     currDayData.imps_viewed, currDayData.view_measured_imps, currDayData.view_measurement_rate,
                     currDayData.view_rate, currDayData.cpa, currDayData.ctr))
                recognitionBaseConnect.commit()
            except:
                try:
                    recognitionBaseConnect.rollback()
                    recognitionBaseCursor.execute(
                        "UPDATE placement_daily_features SET day=%s,imps=%s,clicks=%s,cost=%s,total_convs=%s,imps_viewed=%s,view_measured_imps=%s,view_measurement_rate=%s,view_rate=%s,cpa=%s,ctr=%s WHERE placement_id=%s;",
                        (nDay, currDayData.imps, currDayData.clicks, currDayData.cost, currDayData.conversions,
                         currDayData.imps_viewed, currDayData.view_measured_imps, currDayData.view_measurement_rate,
                         currDayData.view_rate, currDayData.cpa, currDayData.ctr, currPlacement))
                    recognitionBaseConnect.commit()
                except:
                    recognitionBaseConnect.rollback()

        else:
            break
            print "more days"
            print str((sortedDays[j] - sortedDays[j - 1]).days)

recognitionBaseConnect.close()
connect.close()
print "DONE"
"""
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

    print "1"

    for row in queryResult:
        print "2"
        if testIter > 1:
            break

        if curPlacement == row.placement_id and dayGap:
            continue

        if curPlacement != row.placement_id and dayGap:
            dayGap = False
            curPlacement = row.placement_id
            pastHour = row.hour


        if curPlacement != row.placement_id:#adding last day of the placement to the DB
            curPlacementDailyFeatures.day = nDay
            try:
                curPlacementDailyFeatures.cpa = float(curPlacementDailyFeatures.cost) / float(curPlacementDailyFeatures.total_convs)
            except ZeroDivisionError:
                curPlacementDailyFeatures.cpa = 0

            try:
                curPlacementDailyFeatures.ctr = float(curPlacementDailyFeatures.clicks) / float(curPlacementDailyFeatures.imps)
            except ZeroDivisionError:
                curPlacementDailyFeatures.ctr = 0

            try:
                curPlacementDailyFeatures.view_rate = float(curPlacementDailyFeatures.imps_viewed) / float(curPlacementDailyFeatures.view_measured_imps)
            except ZeroDivisionError:
                curPlacementDailyFeatures.view_rate = 0

            try:
                curPlacementDailyFeatures.view_measurement_rate = float(curPlacementDailyFeatures.view_measured_imps) / float(curPlacementDailyFeatures.imps)
            except ZeroDivisionError:
                curPlacementDailyFeatures.view_measurement_rate = 0

            try:
                curPlacementDailyFeatures.save()
            except:
                print "Failed to insert data about placement"

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

            curPlacementDailyFeatures.imps = row.imps
            curPlacementDailyFeatures.clicks = row.clicks
            curPlacementDailyFeatures.total_convs = row.total_convs
            curPlacementDailyFeatures.imps_viewed = row.imps_viewed
            curPlacementDailyFeatures.view_measured_imps = row.view_measured_imps
            curPlacementDailyFeatures.cost = row.cost

            pastHour = row.hour
            nDay = 1
            curPlacement = row.placement_id

            testIter += 1
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
            try:
                curPlacementDailyFeatures.cpa = float(curPlacementDailyFeatures.cost) / float(curPlacementDailyFeatures.total_convs)
            except ZeroDivisionError:
                curPlacementDailyFeatures.cpa = 0

            try:
                curPlacementDailyFeatures.ctr = float(curPlacementDailyFeatures.clicks) / float(curPlacementDailyFeatures.imps)
            except ZeroDivisionError:
                curPlacementDailyFeatures.ctr = 0

            try:
                curPlacementDailyFeatures.view_rate = float(curPlacementDailyFeatures.imps_viewed) / float(curPlacementDailyFeatures.view_measured_imps)
            except ZeroDivisionError:
                curPlacementDailyFeatures.view_rate = 0

            try:
                curPlacementDailyFeatures.view_measurement_rate = float(curPlacementDailyFeatures.view_measured_imps) / float(curPlacementDailyFeatures.imps)
            except ZeroDivisionError:
                curPlacementDailyFeatures.view_measurement_rate = 0

            try:
                curPlacementDailyFeatures.save()#save current day
            except:
                print "Failed to insert data about placement"

            if row.hour.day - pastHour.day > 1:#day gap
                nDay = 1
                dayGap = True;
                testIter += 1
                pastHour = row.hour

            else:#next day
                nDay += 1
                pastHour = row.hour

                curPlacementDailyFeatures.imps = row.imps
                curPlacementDailyFeatures.clicks = row.clicks
                curPlacementDailyFeatures.total_convs = row.total_convs
                curPlacementDailyFeatures.imps_viewed = row.imps_viewed
                curPlacementDailyFeatures.view_measured_imps = row.view_measured_imps
                curPlacementDailyFeatures.cost = row.cost


    print "Database ml_placement_daily_features filled"

    #region test

    #endregion