from models.models import Campaign, Profile, LastToken
from rtb.models.placement_state import CampaignRules, PlacementState
from django.db import connection
from django.utils import timezone
from datetime import timedelta
import json
import datetime
import pytz


def checkRules():
    try:    # update table
        print "Start - check rules"
        query = """ REFRESH MATERIALIZED VIEW view_rules_campaign_placements """
        cursor = connection.cursor()
        cursor.execute(query, locals())
        print "     REFRESHED VIEW view_rules_campaign_placements"
        allRule = list(CampaignRules.objects.all())
        for campaignRules in allRule:
            for oneCampaignRules in campaignRules.rules:
                place = []
                queryString = ''
                if len(oneCampaignRules['if']) >= 1:
                    result = recursionParseRule(oneCampaignRules['if'], queryString)
                    query = """ SELECT placement_id FROM view_rules_campaign_placements WHERE campaign_id=""" + str(campaignRules.campaign_id) + ' and ' + result
                    cursor = connection.cursor()
                    cursor.execute(query, locals())
                    numrows = int(cursor.rowcount)
                    for x in range(0, numrows):
                        place.append(cursor.fetchone()[0])
                    print '     Campaign-{0} rule-{1}'.format(campaignRules.campaign_id, oneCampaignRules['id'])
                    if len(place) >= 1:
                        changed = changeRulesState(oneCampaignRules['then'], campaignRules.campaign_id, place)
                    else:
                        print "         Not have placement-{0}".format(place)

        print "End - check rules"
    except Exception, e:
        print 'Error: ' + str(e)


def recursionParseRule(rule, queryString):
    for arrayIf in rule:
        if type(arrayIf) is list:
            queryString = queryString + '( ' + recursionParseRule(arrayIf, '')
            queryString = queryString + ' )'
        if type(arrayIf) is dict and arrayIf['type'] == 'condition':
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
        for placement in arrayPlacement:
            obj, created = PlacementState.objects.update_or_create(campaign_id=campaign_id,
                                                                   placement_id=placement,
                                                                   defaults=dict(
                                                                       state=state,
                                                                       suspend=date,
                                                                       change=True
                                                                   ))
        print "         Changed placement-{0} to state {1}-{2}".format(arrayPlacement, then, state)
    except Exception, e:
        print 'Error: ' + str(e)