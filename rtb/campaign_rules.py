from models.models import Campaign, Profile, LastToken
from rtb.models.placement_state import CampaignRules
from django.db import connection
from django.utils import timezone
from datetime import timedelta
import json
import datetime
import pytz


def checkRules():
    try:    #1533,

        allRule = list(CampaignRules.objects.all())
        for campaignRules in allRule:
            for oneCampaignRules in campaignRules.rules:
                queryString = ''
                if len(oneCampaignRules['if']) >= 1:
                    result = recursionParseRule(oneCampaignRules['if'], queryString)
                    result
                    query = """ SELECT * FROM view_rules_campaign_placements WHERE """ + result
                    cursor = connection.cursor()
                    cursor.execute(query, locals())
                    # place = cursor.fetchall()
                    place = [dict(zip(
                        ("campaign_id", "placement_id", "imressions", "clicks", "spent", "cpa", "ctr", "cvr", "cpc"),
                        x)) for x in cursor.fetchall()]
                    place
    except Exception, e:
        print 'Error: ' + str(e)
        return 503


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
