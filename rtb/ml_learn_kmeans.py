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
from models.ML_kmeans_model import PlacementDailyFeatures, ClustersCentroids

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

def learn (placement_id,featuresList=None):
    #tt = PlacementDailyFeatures
    kmeansSpaces = []
    Nfeatures = 0
    queryResults= PlacementDailyFeatures.objects.all.aggregate(Max("day"))

    #print queryResults
    maxDay=queryResults[0]

    #len(columnsfeatures)#вместо 3 при умножении Nfeatures=i*3
    #maxDay=
    colNumb = 0
    for i in xrange(1, maxDay):#learning
        kmeansSpaces.append(KMeans(n_clusters=2, init='k-means++'))
        Nfeatures = i*3
        onePlacementFeatures = np.zeros(Nfeatures)
        queryResults = PlacementDailyFeatures.objects.all.aggregate(Max("cpa"), Max("ctr"))

        maxCPA = queryResults[0]
        maxCTR = queryResults[1]

        allFeatures = []
        allFeaturesPlacement = []

        #queryResults = PlacementDailyFeatures.objects.filter #SELECT day,cpa,ctr,view_rate,placement_id  FROM placement_daily_features WHERE placement_id IN (SELECT placement_id FROM placement_daily_features WHERE day=%s) AND day<=%s ORDER BY placement_id,day
        for row in xrange(len(queryResults)):
            #if row['cpa'] == 0:
            if queryResults['cpa'] == 0:
                onePlacementFeatures[colNumb] = 1
            else:
                onePlacementFeatures[colNumb] = float(row['cpa'])/float(maxCPA)

            onePlacementFeatures[colNumb+1] = float(row['ctr'])/float(maxCTR)
            onePlacementFeatures[colNumb+2] = row['view_rate']
            colNumb += 3

            if colNumb >= Nfeatures:
                #print "test"
                allFeatures.append(onePlacementFeatures)
                allFeaturesPlacement.append(row['placement_id'])
                onePlacementFeatures=np.zeros(Nfeatures)
                colNumb=0

            allFeatures = np.float32(allFeatures)
            allFeaturesForRecognition = np.vstack(allFeatures)
            labels = kmeansSpaces[i-1].fit_predict(allFeaturesForRecognition)

            for j in range(len(labels)):
                if labels[j] == 0:
                    PlacementDailyFeatures.objects.save()
                    #recognitionBaseCursor.execute("INSERT INTO first_cluster_cpa1 (placement_id,day) VALUES (%s,%s)",
                    #                             (allFeaturesPlacement[j],i))
                    #recognitionBaseConnect.commit();
                else:
                    PlacementDailyFeatures.objects.save()
                    #recognitionBaseCursor.execute("INSERT INTO second_cluster_cpa1 (placement_id,day) VALUES (%s,%s)",
                    #                             (allFeaturesPlacement[j],i))
                    #recognitionBaseConnect.commit();

    #get info about new
    #cursor.execute("SELECT hour,imps,clicks,cost,total_convs,imps_viewed,view_measured_imps FROM network_analytics_report_by_placement WHERE placement_id=%s;",(i,))
    queryResults = NetworkAnalyticsReport_ByPlacement.objects.filter(placement_id=placement_id).order_by('hour')#get info about new placement for recognition

    allDays={}
    sortedDays=[]

    dbDateFormat="%Y-%m-%d"
    nDay=0


    for i in xrange(len(queryResults)):
        temp = str(queryResults[i]['hour']).split()
        if temp[0] not in allDays:
            allDays[temp[0]] = Placement()
            sortedDays.append(datetime.strptime(temp[0],dbDateFormat))

        """allDays[temp[0]].imps+=row['imps']
        allDays[temp[0]].clicks+=row['clicks']
        allDays[temp[0]].cost+=row['cost']
        allDays[temp[0]].conversions+=row['total_convs']
        allDays[temp[0]].imps_viewed+=row['imps_viewed']
        allDays[temp[0]].view_measured_imps+=row['view_measured_imps']"""
        allDays[temp[0]].imps += queryResults[i]['imps']
        allDays[temp[0]].clicks += queryResults[i]['clicks']
        allDays[temp[0]].cost += queryResults[i]['cost']
        allDays[temp[0]].conversions += queryResults[i]['total_convs']
        allDays[temp[0]].imps_viewed += queryResults[i]['imps_viewed']
        allDays[temp[0]].view_measured_imps += queryResults[i]['view_measured_imps']

    for time, placement in allDays.iteritems():
        try:
            placement.cpa=float(placement.cost)/float(placement.conversions)
        except ZeroDivisionError:
            placement.cpa=0

        try:
            placement.ctr=float(placement.clicks)/float(placement.imps)
        except ZeroDivisionError:
            placement.ctr=0

        try:
            placement.view_rate=float(placement.imps_viewed)/float(placement.view_measured_imps)
        except ZeroDivisionError:
            placement.view_rate=0

        try:
            placement.view_measurement_rate=float(placement.view_measured_imps)/float(placement.imps)
        except ZeroDivisionError:
            placement.view_measurement_rate=0


    allFeatures=[]
    sortedDays.sort()
    currDayData=allDays[sortedDays[0].strftime(dbDateFormat)]

    for j in range(1,len(sortedDays)):#
        if sortedDays[j]-sortedDays[j-1] == timedelta(days=1):
            currDayData=allDays[sortedDays[j].strftime(dbDateFormat)]
            nDay=j+1
            #SAVE IN ARRAY FOR RECOGNITION

        else:
            break

    Nfeatures = (nDay-1)*3
    onePlacementFeatures=np.zeros(Nfeatures)

    for j in xrange(Nfeatures):
        onePlacementFeatures

    allFeatures = np.float32(allFeatures)
    allFeaturesForRecognition = np.vstack(allFeatures)
    labels = kmeansSpaces[nDay-1].predict(allFeaturesForRecognition)#send on recognition


