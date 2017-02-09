import numpy as np
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from rtb.models.ml_video_ad_model import MLVideoImpsTracker, MLVideoAdCampaignsModels, MLVideoAdCampaignsModelsInfo, MLVideoAdCampaignsResults
from rtb.models.models import Advertiser, Campaign
from sklearn.externals import joblib
from os.path import isfile
from datetime import datetime, timedelta
from rtb.controllers.campaign_create import getToken, getCampaignById
import requests
import json

def getDataWindow(type, data, windowSize=3):
    allFeatures = []
    if (len(data) - windowSize < 0):
        print "Not enough data for that window size"
        return -1, -1, -1
    allResults1D = np.zeros(len(data) - windowSize)
    # data:
    # 0 - current hour from the day start
    # 1 - imps
    # 2 - ad starts
    # 3 - fill rate
    for i in range(windowSize-1, len(data)-1):
        temp = 0
        # 1
        if type == 0:
            onePlacementFeatures = np.zeros(4)
            onePlacementFeatures[0] = data[i][0]  # hour from day start
            onePlacementFeatures[1] = data[i][1]  # imps
            onePlacementFeatures[2] = data[i][2]  # ad_starts
            for j in xrange(windowSize):
                temp += data[i-j][3]
            onePlacementFeatures[3] = temp / windowSize # moving average

        emaF = 0
        a = 0.4
        # EMA(fill_rate)
        # 3
        if type == 1:
            onePlacementFeatures = np.zeros(4)
            onePlacementFeatures[0] = data[i][0]  # hour from day start
            onePlacementFeatures[1] = data[i][1]  # imps
            onePlacementFeatures[2] = data[i][2]  # ad_starts
            for j in xrange(windowSize):
                if j == 0:
                    emaF = data[i - windowSize + 1][3]
                else:
                    emaF = a * data[i - windowSize + j][3] + (1 - a) * emaF
            onePlacementFeatures[3] = emaF  # exponential moving average

        # RSI (relative strength index)
        # 6
        if type == 2:
            onePlacementFeatures = np.zeros(4)
            onePlacementFeatures[0] = calcRSI(data=data, windowSize=windowSize, i=i) # RSI
            for j in xrange(windowSize):
                if j == 0:
                    emaF = data[i-windowSize+1][3]
                else:
                    emaF = a * data[i-windowSize+j][3] + (1 - a) * emaF
            onePlacementFeatures[1] = emaF # exponential moving average
            onePlacementFeatures[2] = data[i][0]  # hour from day start
            for j in xrange(windowSize):
                temp += data[i - j][3]
            onePlacementFeatures[3] = temp / windowSize  # moving average

        allFeatures.append(onePlacementFeatures)

        allResults1D[i-windowSize+1] = data[i+1][3]

    allFeatures = np.float32(allFeatures)
    allFeatures = np.vstack(allFeatures)

    data = data[windowSize-1:]

    return data, allFeatures, allResults1D

def calcRSI(data, windowSize, i, a=0.2):
    U = []
    D = []
    for j in xrange(1, windowSize):
        if (data[i - windowSize + j][3] - data[i - windowSize + j + 1][3]) == 0:
            D.append(0.0)
            U.append(0.0)
            continue

        if (data[i - windowSize + j][3] - data[i - windowSize + j + 1][3]) > 0:
            D.append(data[i - windowSize + j][3] - data[i - windowSize + j + 1][3])
            U.append(0.0)
        else:
            U.append(data[i - windowSize + j + 1][3] - data[i - windowSize + j][3])
            D.append(0.0)
    emaU = 0
    emaD = 0
    for j in xrange(len(U)):
        if j == 0:
            emaU = U[0]
            emaD = D[0]
        else:
            emaU = a * U[j] + (1 - a) * emaU
            emaD = a * D[j] + (1 - a) * emaD

    if emaD == 0:
        return 100.0
    else:
       return (100.0 - (100.0 / (1.0 + emaU / emaD)))

def getMLCpmData(campaignId, fromDate=None, toDate=None, windowSize=None):
    if toDate is None:
        toDate = datetime.now()
        fromDate = toDate - timedelta(hours=1)

    if windowSize is not None:
        toDate = datetime.now()
        fromDate = toDate - timedelta(hours=windowSize)

    queryRes = MLVideoImpsTracker.objects.raw("""
    SELECT
      date_trunc('hour', "Date") id,
      count(id) filter (where is_imp = true) imps,
      count(id) filter (where is_imp = false) ad_starts,
      case (count(id) filter (where is_imp = true)) when 0 then 0 else SUM("PricePaid")/(count(id) filter (where is_imp = true))*1000.0 end cpm,
      coalesce(SUM(cpvm) - SUM("PricePaid"),-SUM("PricePaid"),SUM(cpvm),0) profit_loss,
      case (count(id) filter (where is_imp = false)) when 0 then 0 else SUM(cpvm) / (count(id) filter (where is_imp = false)) end rpm,
      case count(id) filter (where is_imp = true) when 0 then 0 else (count(id) filter (where is_imp = false))::float / (count(id) filter (where is_imp = true))*100 end fill_rate
    FROM ml_video_imps_tracker
    WHERE
      "CpId" = """ + str(campaignId) + """
    AND
      "Date" >= '""" + str(fromDate) + """'
    AND
      "Date" <= '""" + str(toDate) + """'
    GROUP BY
    date_trunc('hour', "Date")
    order by date_trunc('hour', "Date");
                """)
    data = []
    # data:
    # 0 - current hour from the day start
    # 1 - imps
    # 2 - ad starts
    # 3 - fill rate
    # 4 - cpm
    # 5 - profit/loss
    # 6 - date
    # 7 - rpm
    first = True
    for row in queryRes:
        if first:
            data.append([])
            data[len(data) - 1].append(row.id.hour)
            data[len(data) - 1].append(row.imps)
            data[len(data) - 1].append(row.ad_starts)
            data[len(data) - 1].append(row.fill_rate)
            data[len(data) - 1].append(row.cpm)
            data[len(data) - 1].append(row.profit_loss)
            data[len(data) - 1].append(row.id)
            data[len(data) - 1].append(row.rpm)
            first = False
            continue
        if (row.id - data[len(data) - 1][6]) != timedelta(hours=1):
            temp = data[len(data) - 1][6] + timedelta(hours=1)
            while (row.id - temp) >= timedelta(hours=1):
                data.append([])
                data[len(data) - 1].append(temp.hour)
                data[len(data) - 1].append(0)
                data[len(data) - 1].append(0)
                data[len(data) - 1].append(0)
                data[len(data) - 1].append(0)
                data[len(data) - 1].append(0)
                data[len(data) - 1].append(temp)
                data[len(data) - 1].append(0)
                temp += timedelta(hours=1)
        data.append([])
        data[len(data) - 1].append(row.id.hour)
        data[len(data) - 1].append(row.imps)
        data[len(data) - 1].append(row.ad_starts)
        data[len(data) - 1].append(row.fill_rate)
        data[len(data) - 1].append(row.cpm)
        data[len(data) - 1].append(row.profit_loss)
        data[len(data) - 1].append(row.id)
        data[len(data) - 1].append(row.rpm)

    if len(data) != 0:
        if data[len(data) - 1][0] != toDate.hour:
            data.append([])
            data[len(data) - 1].append(toDate.hour)
            data[len(data) - 1].append(0)
            data[len(data) - 1].append(0)
            data[len(data) - 1].append(0)
            data[len(data) - 1].append(0)
            data[len(data) - 1].append(0)
            data[len(data) - 1].append(data[len(data) - 2][6]+timedelta(hours=1))
            data[len(data) - 1].append(0)
    return data

def mlRefreshAlgoListCron():
    print "Start of the campaigns CPM prediction learning"
    algoVocabl = []
    algoVocabl.append("gradient")
    algoVocabl.append("random_forest")
    algoVocabl.append("abtree")
    algoList = []
    algoList.append(GradientBoostingRegressor())
    algoList.append(RandomForestRegressor(
        n_estimators=200,
        max_depth=10
    ))
    algoList.append(AdaBoostRegressor(
        DecisionTreeRegressor(max_depth=10),
        n_estimators=500,
        random_state=np.random.RandomState(1)
    ))
    allAdvertisers = Advertiser.objects.filter(ad_type="videoAds")
    for advertiser in allAdvertisers:
        allCampaigns = Campaign.objects.filter(advertiser_id=advertiser.id)
        for campaign in allCampaigns:
            # filling campaign data
            data = getMLCpmData(
                campaignId=campaign.id,
                fromDate=datetime.now() - timedelta(days=30),
                toDate=datetime.now()
            )

            # check of the data for learning amount
            if len(data) < 264:
                print "Not enough data for the campaign " + str(campaign.id)
                continue
            # models learning
            for i in xrange(len(algoList)):
                if isfile("rtb/res/prediction_models_cpm/" + str(campaign.id) + "_" + str(algoVocabl[i]) + ".pkl"):
                    continue
                tempData, allFeaturesForLearning, allResultsLearning = getDataWindow(
                    i, data, 12)
                algoList[i].fit(allFeaturesForLearning, allResultsLearning)
                # TODO: make a check for getting a better algo
                joblib.dump(algoList[i], "rtb/res/prediction_models_cpm/" + str(campaign.id) + "_" + str(algoVocabl[i]) + ".pkl", compress=1)
                MLVideoAdCampaignsModelsInfo.objects.update_or_create(
                    campaign_id=campaign.id,
                    type=algoVocabl[i],
                    defaults={
                        "path": "rtb/res/prediction_models_cpm/" + str(campaign.id) + "_" + str(algoVocabl[i]) + ".pkl",
                        "start": data[0][6],
                        "finish": data[len(data)-1][6],
                        "evaluation_date": datetime.now()
                    }
                )

    print "Campaigns cpm prediction learning finished"

def mlChangeCampaignCpmCron():
    algoVocabl = []
    algoVocabl.append("gradient")
    algoVocabl.append("random_forest")
    algoVocabl.append("abtree")
    queryRes = MLVideoAdCampaignsModels.objects.all()
    for row in queryRes:
        if isfile(row.path):
            predictor = joblib.load(row.path)
        else:
            print "File " + str(row.path) + " is not exist"
            continue
        # loading data
        data = getMLCpmData(campaignId=row.campaign_id, windowSize=12)
        data, features, _ = getDataWindow(
            type=algoVocabl.index(row.type),
            data=data,
            windowSize=12,
        )
        if data == -1:
            print "Can not predict CPM with that amount of the data for the campaign " + str(row.campaign_id)
            continue
        # getting answer from the predictor
        ans = predictor.predict(features)[0]
        if ans < 0:
            ans = 0
        cpm = (ans / 100.0) * float(data[0][7])
        # send to appnexus
        campInfo = getCampaignById(row.campaign_id)
        campInfo["base_bid"] = float(cpm)
        campInfo["cpm_bid_type"] = "base"
        url = 'https://api.appnexus.com/campaign?id=' + str(row.campaign_id)+"&advertiser_id="+str(campInfo["advertiser_id"])
        headers = {"Authorization": getToken(), 'Content-Type': 'application/json'}
        data = json.dumps({
            "campaign": campInfo
        })
        apnxResponse = json.loads(requests.put(url=url, headers=headers, data=data).content)
        try:
            apnxResponse['response']['error']
            print "Appnexus error on the changing of CPM for campaign " + str(row.campaign_id)
            continue
        except:
            pass
        # save in db
        MLVideoAdCampaignsResults(
            advertiser_id=row.advertiser_id,
            campaign_id=row.campaign_id,
            res_date=datetime.now(),
            type=row.type,
            fill_rate=ans,
            cpm=cpm,
            profit_loss=None
        ).save()
