from models.models import Campaign, Profile, LastToken, Advertiser
from rtb.models.placement_state import CampaignRules, PlacementState
from rtb.models.placement_state_unsuspend import PlacementStateUnsuspend
from django.db import connection
from django.utils import timezone
from datetime import timedelta
import json
import datetime
import pytz


def checkRules():
    try:
        print "Start - check rules"
        allRule = list(CampaignRules.objects.all().select_related("campaign"))
        for campaignRules in allRule:
            tableType = ''
            if campaignRules.campaign.advertiser_id:
                currentAdvertiser = Advertiser.objects.get(pk=campaignRules.campaign.advertiser_id)
                rulesType = currentAdvertiser.rules_type
                adType = currentAdvertiser.ad_type
                if adType == 'ecommerceAd':
                    predType= 'predictionecomm'
                else:
                    predType = 'predictionleadgen'
                if rulesType == 'report':
                    tableType = "view_rule_type_report"
                    unsuspendTableType = "view_rule_unsuspend_type_report"
                    prediction = ''
                if rulesType == 'tracker':
                    tableType = "view_rule_type_tracker"
                    unsuspendTableType = "view_rule_unsuspend_type_tracker"
            for oneCampaignRules in campaignRules.rules:
                place = []
                queryString = ''
                if len(oneCampaignRules['if']) >= 1:
                    result = recursionParseRule(oneCampaignRules['if'], queryString, predType)
                    query = """ SELECT placement_id FROM """ + str(tableType) + """ WHERE campaign_id=""" + str(campaignRules.campaign_id) + ' and ' + result
                    cursor = connection.cursor()
                    cursor.execute(query, locals())
                    numrows = int(cursor.rowcount)
                    for x in range(0, numrows):
                        place.append(cursor.fetchone()[0])
                    print '     Campaign-{0} rule-{1}'.format(campaignRules.campaign_id, oneCampaignRules['id'])
                    if len(place) >= 1:
                        usualPlacementId = place
                        unsuspendPlacementId = []
                        unsuspendList = list(PlacementStateUnsuspend.objects.filter(placement_id__in=place, campaign_id=campaignRules.campaign_id))
                        for itemPlacement in unsuspendList:
                            if itemPlacement.placement_id in place:
                                unsuspendPlacementId.append(itemPlacement.placement_id)
                                usualPlacementId.remove(itemPlacement.placement_id)
                        if len(unsuspendPlacementId) > 0:
                            unsuspendPlacement = []
                            placementIndict = '(' + str(unsuspendPlacementId)[1:-1] + ')'
                            unsuspendQuery = """ SELECT placement_id FROM """ + str(unsuspendTableType) \
                                    + """ WHERE campaign_id=""" + str(campaignRules.campaign_id) + """ and """ \
                                    + """ placement_id in """ + placementIndict \
                                    + """ and """ + result
                            cursor = connection.cursor()
                            cursor.execute(unsuspendQuery, locals())
                            numrows = int(cursor.rowcount)
                            for x in range(0, numrows):
                                unsuspendPlacement.append(cursor.fetchone()[0])
                            changeRulesState(oneCampaignRules['then'], campaignRules.campaign_id, unsuspendPlacement)
                        if len(usualPlacementId) > 0:
                            changeRulesState(oneCampaignRules['then'], campaignRules.campaign_id, usualPlacementId)

                    else:
                        print "         Not have placement-{0}".format(place)

        print "End - check rules"
    except Exception, e:
        print 'Error: ' + str(e)


def recursionParseRule(rule, queryString, predType):
    for arrayIf in rule:
        if type(arrayIf) is list:
            queryString = queryString + '( ' + recursionParseRule(arrayIf, '', predType)
            queryString = queryString + ' )'
        if type(arrayIf) is dict and arrayIf['type'] == 'condition':
            if arrayIf['payment'] == 'prediction':
                if arrayIf['value'] == 'bad':
                    queryString = str(queryString) + predType + str(arrayIf['compare']) + 'false '
                else:
                    queryString = str(queryString) + predType + str(arrayIf['compare']) + 'true '
            else:
                queryString = str(queryString) + str(arrayIf['payment']) + str(arrayIf['compare']) + str(
                    arrayIf['value']) + ' '
        if type(arrayIf) is dict and arrayIf['type'] == 'logic':
            queryString = str(queryString) + str(arrayIf['logicOrAnd']) + ' '

    return queryString

def changeRulesState (then, campaign_id, arrayPlacement):
    try:
        if then == 'Blacklist':
            state = 2
            date = None
        if then == 'Whitelist':
            state = 4
            date = None
        if then == '0':
            state = 1
            date = None
        if then in ['1', '3', '7']:
            state = 1
            date = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) + datetime.timedelta(days=int(then))
        listForPirntCountAdd = []
        for placement in arrayPlacement:
            if date is not None:
                tempRow = list(PlacementState.objects.filter(campaign_id=campaign_id, placement_id=placement))
                if len(tempRow) > 0:
                    if tempRow[0].suspend is not None:
                        continue
            obj, created = PlacementState.objects.update_or_create(campaign_id=campaign_id,
                                                                   placement_id=placement,
                                                                   defaults=dict(
                                                                       state=state,
                                                                       suspend=date,
                                                                       change=True
                                                                   ))
            listForPirntCountAdd.append(placement)
        print "         Changed placement-{0} to state {1}-{2}".format(listForPirntCountAdd, then, state)
    except Exception, e:
        print 'Error: ' + str(e)