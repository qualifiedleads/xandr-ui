__author__ = 'USER'

import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
import psycopg2
from psycopg2 import extras
from datetime import datetime
from datetime import timedelta
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLClustersCentroidsKmeans, MLPlacementsClustersKmeans

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.http import JsonResponse
from utils import parse_get_params, make_sum, check_user_advertiser_permissions
from models import SiteDomainPerformanceReport, Campaign, GeoAnaliticsReport, NetworkAnalyticsReport_ByPlacement, \
    Placement, NetworkCarrierReport_Simple, NetworkDeviceReport_Simple
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField
from django.db.models.functions import Coalesce, Concat, ExtractWeekDay
from django.db import connection
from django.core.cache import cache
import itertools
import datetime
from pytz import utc
import filter_func

#from .models import PlacementDailyFearures

class Placement:#objects with features for recognition
    placement = 0

    imps = 0
    clicks = 0
    cost=0
    conversions=0
    imps_viewed=0
    view_measured_imps=0

    cpa=0
    view_rate=0
    view_measurement_rate=0

    features=np.empty(1)
    cluster=0
    importance=True

def learn (placement_id=None,featuresList=None):

    kmeansSpaces = []
    Nfeatures = 0
    queryResults= MLPlacementDailyFeatures.objects.all.aggregate(Max("day"))

    #print queryResults
    maxDay=queryResults[0]

    #len(columnsfeatures)#������ 3 ��� ��������� Nfeatures=i*3
    #maxDay=
    colNumb = 0
    for i in xrange(1, maxDay):#learning
        kmeansSpaces.append(KMeans(n_clusters=2, init='k-means++'))
        Nfeatures = i*3
        onePlacementFeatures = np.zeros(Nfeatures)
        queryResults = MLPlacementDailyFeatures.objects.all.aggregate(Max("cpa"), Max("ctr"))

        maxCPA = queryResults[0]
        maxCTR = queryResults[1]

        allFeatures = []
        allFeaturesPlacement = []

        #queryResults = PlacementDailyFeatures.objects.filter #SELECT day,cpa,ctr,view_rate,placement_id  FROM placement_daily_features WHERE placement_id IN (SELECT placement_id FROM placement_daily_features WHERE day=%s) AND day<=%s ORDER BY placement_id,day
        for row in queryResults:
            if row.cpa == 0:
                onePlacementFeatures[colNumb] = 1
            else:
                onePlacementFeatures[colNumb] = float(row.cpa)/float(maxCPA)

            onePlacementFeatures[colNumb+1] = float(row.ctr)/float(maxCTR)
            onePlacementFeatures[colNumb+2] = row.view_rate
            colNumb += 3

            if colNumb >= Nfeatures:
                #print "test"
                allFeatures.append(onePlacementFeatures)
                allFeaturesPlacement.append(row.placement_id)
                onePlacementFeatures=np.zeros(Nfeatures)
                colNumb=0

            allFeatures = np.float32(allFeatures)
            allFeaturesForRecognition = np.vstack(allFeatures)
            labels = kmeansSpaces[i-1].fit_predict(allFeaturesForRecognition)

            for j in range(len(labels)):
                if labels[j] == 0:
                    MLPlacementsClustersKmeans.objects.save()
                    #recognitionBaseCursor.execute("INSERT INTO first_cluster_cpa1 (placement_id,day) VALUES (%s,%s)",
                    #                             (allFeaturesPlacement[j],i))
                    #recognitionBaseConnect.commit();
                else:
                    MLPlacementsClustersKmeans.objects.save()
                    #recognitionBaseCursor.execute("INSERT INTO second_cluster_cpa1 (placement_id,day) VALUES (%s,%s)",
                    #                             (allFeaturesPlacement[j],i))
                    #recognitionBaseConnect.commit();

    #get info about new
    #cursor.execute("SELECT hour,imps,clicks,cost,total_convs,imps_viewed,view_measured_imps FROM network_analytics_report_by_placement WHERE placement_id=%s;",(i,))
    try:
        queryResults = NetworkAnalyticsReport_ByPlacement.objects.filter(placement_id=placement_id).order_by('hour')#get info about new placement for recognition
    except:
        print "Error in getting data about new placement"
    allDays = {}
    sortedDays = []

    dbDateFormat = "%Y-%m-%d"

    for row in queryResults:
        temp = str(row.hour.split())
        if temp[0] not in allDays:
            allDays[temp[0]] = Placement()
            sortedDays.append(datetime.strptime(temp[0], dbDateFormat))

        allDays[temp[0]].imps += row.imps
        allDays[temp[0]].clicks += row.clicks
        allDays[temp[0]].cost += row.cost
        allDays[temp[0]].conversions += row.total_convs
        allDays[temp[0]].imps_viewed += row.imps_viewed
        allDays[temp[0]].view_measured_imps += row.view_measured_imps

    for time, placement in allDays.iteritems():
        try:
            placement.cpa = float(placement.cost)/float(placement.conversions)
        except ZeroDivisionError:
            placement.cpa = 0

        try:
            placement.ctr = float(placement.clicks)/float(placement.imps)
        except ZeroDivisionError:
            placement.ctr = 0

        try:
            placement.view_rate = float(placement.imps_viewed)/float(placement.view_measured_imps)
        except ZeroDivisionError:
            placement.view_rate = 0

        try:
            placement.view_measurement_rate = float(placement.view_measured_imps)/float(placement.imps)
        except ZeroDivisionError:
            placement.view_measurement_rate = 0


    #allFeatures=[]
    #currDayData = allDays[sortedDays[0].strftime(dbDateFormat)]

    sortedDays.sort()
    nDay = 1
    for j in range(1, len(sortedDays)):#
        if sortedDays[j]-sortedDays[j-1] == timedelta(days=1):
            #currDayData=allDays[sortedDays[j].strftime(dbDateFormat)]
            #nDay=j+1
            nDay += 1
        else:
            break

    Nfeatures = 3 # len(featuresList) - in future
    onePlacementFeatures = np.zeros(nDay*3)
    colNumb = 0
    for j in xrange(nDay):
        if (allDays[sortedDays[j].strftime(dbDateFormat)].cpa == 0):
            onePlacementFeatures[j*Nfeatures] = 1
        else:
            onePlacementFeatures[j*Nfeatures] = float(allDays[sortedDays[j].strftime(dbDateFormat)].cpa) / float(maxCPA)

        onePlacementFeatures[j*Nfeatures+1] = float(allDays[sortedDays[j].strftime(dbDateFormat)].ctr) / float(maxCTR)
        onePlacementFeatures[j*Nfeatures+2] = allDays[sortedDays[j].strftime(dbDateFormat)]

    #allFeatures.append(onePlacementFeatures)
    #allFeatures = np.float32(allFeatures)
    #allFeaturesForRecognition = np.vstack(allFeatures)
    onePlacementFeatures = np.float32(onePlacementFeatures)
    labels = kmeansSpaces[nDay-1].predict(onePlacementFeatures)#send on recognition
    #labels = kmeansSpaces[nDay-1].predict(allFeaturesForRecognition)#send on recognition

    print "Placement " + str(placement_id) + " belongs to " + str(labels[[0]+1]) + " cluster"
