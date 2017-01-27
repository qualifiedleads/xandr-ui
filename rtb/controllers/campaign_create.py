from rest_framework.decorators import api_view
from rest_framework.response import Response
from rtb.models.models import LastToken
from django.conf import settings
import datetime
import rtb.utils as utils
import json
import requests

appnexusUrl = 'https://api.appnexus.com/'


@api_view(['POST'])
# @check_user_advertiser_permissions(campaign_id_num=0)
def campaignCreateBulk(request):
    """
POST

## Url format: /api/v1/campaign/create/bulk

+ Data
    advertiserId: advertiserId,
    campaignId: campaignId,
    domain: domain textarea

    """
    try:
        if request.method == "POST":
            advertiserId = int(request.data.get("advertiserId"))
            campaignId = int(request.data.get("campaignId"))
            listDomain = request.data.get("domain").strip().split('\n')
            afterChecklistDomain = []

            for domain in listDomain:
                temp = domain.strip()
                if temp == '':
                    del domain
                    continue
                afterChecklistDomain.append(temp)

            result = applyCreateCampaign(advertiserId, campaignId, afterChecklistDomain)
            if result == 500 or result == 404:
                return Response(status=result)
            return Response(result)
    except Exception, e:
        print 'Error: ' + str(e)


def applyCreateCampaign(advertiserId, campaignId, listDomain):
    try:
        createdIdCampaign = []
        createdProfile = []
        templateCampaignDic = getCampaignById(campaignId)
        templateProfileDic = getProfileByCampaignId(templateCampaignDic['profile_id'])
        createdProfile = CreateProfileForCampaign(advertiserId, templateProfileDic, listDomain)
        campaignArray = []
        i = 0
        for domain in listDomain:
            campaignArray.append(templateCampaignDic.copy())
            campaignArray[i]['name'] = 'template_domain_' + domain
            campaignArray[i]['state'] = 'active'
            for profile in createdProfile:
                if domain == profile[1]:
                    campaignArray[i]['profile_id'] = profile[0]
            i += 1

        createdIdCampaign = createCampaign(campaignArray, advertiserId)
        return createdIdCampaign
    except Exception, e:
        print 'Error: ' + str(e)
        return 500


def getToken():
    try:
        twoHours = datetime.timedelta(hours=1, minutes=55)
        lastToken = LastToken.objects.filter(name='token')
        if len(lastToken) >= 1:
            if utils.get_current_time() - lastToken[0].date < twoHours:
                return lastToken[0].token
        else:
            tempDate = utils.get_current_time() - twoHours
            LastToken(name='token', token='', date=tempDate).save()
        try:
            authUrl = appnexusUrl + "auth"
            data = {"auth": settings.NEXUS_AUTH_DATA}
            authRequest = requests.post(authUrl, data=json.dumps(data))
            response = json.loads(authRequest.content)
            try:
                response['response']['error']
                print "get campaign by id - " + response['response']['error']
            except:
                pass
            lastToken = response['response']['token']
            lastTokenTime = utils.get_current_time()
            LastToken.objects.filter(name='token').update(token=lastToken, date=lastTokenTime)
            return lastToken
        except:
            print "get token - " + response['response']['error']
            return 503
    except Exception, e:
        print 'Error: ' + str(e)
        return 500


def getCampaignById(campId):
    try:
        url = appnexusUrl + 'campaign?id={0}'.format(campId)
        headers = {"Authorization": getToken(), 'Content-Type': 'application/json'}
        campaign = json.loads(requests.get(url, headers=headers).content)
        try:
            campaign['response']['error']
            print "get campaign by id - " + campaign['response']['error']
            return 404
        except:
            pass
        return campaign['response']['campaign']
    except Exception, e:
        print 'Error: ' + str(e)
        return 500


def createCampaign(campaignArray, advertiserId):
    try:
        url = appnexusUrl + 'campaign?advertiser_id={0}'.format(advertiserId)
        headers = {"Authorization": getToken(), 'Content-Type': 'application/json'}

        data = json.dumps({
            "campaigns": campaignArray
        })

        createdCampaign = json.loads(requests.post(url, data=data, headers=headers).content)
        try:
            createdCampaign['response']['error']
            print "createCampaign - " + createdCampaign['response']['error']
            return 404
        except:
            pass
        print 'createCampaign - ' + str(createdCampaign['response']['id'])
        return createdCampaign['response']['id']
    except Exception, e:
        print 'Error: ' + str(e)
        return 500


def getProfileByCampaignId(profileId):
    try:
        url = appnexusUrl + 'profile?id={0}'.format(profileId)
        headers = {"Authorization": getToken(), 'Content-Type': 'application/json'}
        profile = json.loads(requests.get(url, headers=headers).content)
        try:
            profile['response']['error']
            print "get campaign by id - " + profile['response']['error']
            return 404
        except:
            pass
        return profile['response']['profile']
    except Exception, e:
        print 'Error: ' + str(e)
        return 500


def CreateProfileForCampaign(advertiserId, templateProfileDic, listDomain):
    try:
        profileArray = dict
        createdProfile = []
        i = 0
        for domain in listDomain:
            profileArray = templateProfileDic.copy()
            profileArray['domain_action'] = "include"
            profileArray['domain_targets'] = [
                {
                    "domain": domain
                }
            ]
            profileArray.pop('id', None)
            url = appnexusUrl + 'profile?advertiser_id={0}'.format(advertiserId)
            headers = {"Authorization": getToken(), 'Content-Type': 'application/json'}
            data = json.dumps({
                "profile": profileArray
            })
            oneProfile = json.loads(requests.post(url, data=data, headers=headers).content)
            createdProfile.append([oneProfile['response']['id'], domain])
            try:
                oneProfile['response']['error']
                print "createdProfile - " + oneProfile['response']['error']
                return 404
            except:
                pass
            i += 1
        print 'createdProfile - ' + str(createdProfile)
        return createdProfile
    except Exception, e:
        print 'Error: ' + str(e)
        return 500
