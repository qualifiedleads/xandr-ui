from models.models import Campaign, Profile, LastToken, Advertiser
from rtb.models.placement_state import CampaignRules, PlacementState
from rtb.models.placement_state_unsuspend import PlacementStateUnsuspend, PlacementStateHistory
from django.db import connection
from django.utils import timezone
from models.placement_state_unsuspend import PlacementStateUnsuspend
from models.ui_data_models import UIUsualPlacementsGridDataAll, UIUsualPlacementsGridDataAllTracker
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
                    parentTable = UIUsualPlacementsGridDataAll
                if rulesType == 'tracker':
                    tableType = "view_rule_type_tracker"
                    unsuspendTableType = "view_rule_unsuspend_type_tracker"
                    parentTable = UIUsualPlacementsGridDataAllTracker
            for oneCampaignRules in campaignRules.rules:
                indexRule = oneCampaignRules['id']
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
                        unsuspendList = list(PlacementStateUnsuspend.objects.filter(placement_id__in=place,
                                                                                    campaign_id=campaignRules.campaign_id,
                                                                                    rule_id=campaignRules.id,
                                                                                    rule_index=indexRule))
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
                                    + """ and rule_id=""" + str(campaignRules.id) \
                                    + """ and rule_index=""" + '\'' + str(indexRule) + '\'' \
                                    + """ and """ + result
                            cursor = connection.cursor()
                            cursor.execute(unsuspendQuery, locals())
                            numrows = int(cursor.rowcount)
                            for x in range(0, numrows):
                                unsuspendPlacement.append(cursor.fetchone()[0])
                            appliedRuleForPlacement = changeRulesState(oneCampaignRules['then'], campaignRules.campaign_id, unsuspendPlacement)
                            saveToUnsupendTable(appliedRuleForPlacement, campaignRules.id, indexRule, parentTable)
                            saveHistoryForPlacementState(appliedRuleForPlacement, campaignRules.id, indexRule, unsuspendQuery, parentTable)
                        if len(usualPlacementId) > 0:
                            appliedRuleForPlacement = changeRulesState(oneCampaignRules['then'], campaignRules.campaign_id, usualPlacementId)
                            saveToUnsupendTable(appliedRuleForPlacement, campaignRules.id, indexRule, parentTable)
                            saveHistoryForPlacementState(appliedRuleForPlacement, campaignRules.id, indexRule, query, parentTable)
                    else:
                        print "         Not have placement-{0}".format(place)
        print "End - check rules"
    except Exception, e:
        print 'Error: ' + str(e)


def saveHistoryForPlacementState(appliedRuleForPlacement, ruleId, indexRule, query, parentTable):
    try:
        for itemObj in appliedRuleForPlacement:
            placementData = list(parentTable.objects.filter(campaign_id=itemObj['campaign_id'],
                                                            placement_id=itemObj['placement_id']))[0]
            if placementData:
                PlacementStateHistory(
                    placement_id=placementData.placement_id,
                    campaign_id=placementData.campaign_id,
                    rule_id=ruleId,
                    rule_index=indexRule,
                    spent=placementData.spent,
                    conversions=placementData.conversions,
                    imps=placementData.imps,
                    clicks=placementData.clicks,
                    cpa=placementData.cpa,
                    cpc=placementData.cpc,
                    cpm=placementData.cpm,
                    cvr=placementData.cvr,
                    ctr=placementData.ctr,
                    imps_viewed=placementData.imps_viewed,
                    view_measured_imps=placementData.view_measured_imps,
                    view_measurement_rate=placementData.view_measurement_rate,
                    view_rate=placementData.view_rate,
                    date=timezone.make_aware(datetime.datetime.utcnow(), timezone.get_default_timezone()),
                    then=itemObj['then'],
                    select=query,
                ).save()

    except Exception, e:
        print "Can't save to PlacementStateHistory. Error: " + str(e)


def saveToUnsupendTable(appliedRuleForPlacement, ruleId, indexRule, parentTable):
    try:
        for itemObj in appliedRuleForPlacement:
            placementData = list(parentTable.objects.filter(campaign_id=itemObj['campaign_id'],
                                                            placement_id=itemObj['placement_id']))[0]
            if placementData:
                obj, created = PlacementStateUnsuspend.objects.update_or_create(
                    placement_id=placementData.placement_id,
                    campaign_id=placementData.campaign_id,
                    rule_id=ruleId,
                    rule_index=indexRule,
                    defaults={
                        'spent': placementData.spent,
                        'conversions': placementData.conversions,
                        'imps': placementData.imps,
                        'clicks': placementData.clicks,
                        'cpa': placementData.cpa,
                        'cpc': placementData.cpc,
                        'cpm': placementData.cpm,
                        'cvr': placementData.cvr,
                        'ctr': placementData.ctr,
                        'imps_viewed': placementData.imps_viewed,
                        'view_measured_imps': placementData.view_measured_imps,
                        'view_measurement_rate': placementData.view_measurement_rate,
                        'view_rate': placementData.view_rate
                    }
                )
    except Exception, e:
        print "Can't save table of the PlacementStateUnsuspend. Error: " + str(e)


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
        listForCheckRule = []
        for placement in arrayPlacement:
            obj, created = PlacementState.objects.update_or_create(campaign_id=campaign_id,
                                                                   placement_id=placement,
                                                                   defaults=dict(
                                                                       state=state,
                                                                       suspend=date,
                                                                       change=True
                                                                   ))
            listForCheckRule.append({
                'placement_id': placement,
                'then': then,
                'campaign_id': campaign_id
            })
        print "         Changed placement-{0} to state {1}-{2}".format(arrayPlacement, then, state)
        return listForCheckRule
    except Exception, e:
        print 'Error: ' + str(e)

