from models.placement_state import PlacementState as ModelPlacementState
from django.conf import settings
from models.models import Campaign, Profile
from rtb.cron import load_depending_data
import json
import requests
import datetime
import pytz
import utils

_last_token = None
_last_token_time = None

class PlacementState:
    def __init__(self, campaign_id, placement_id):
        self.__last_token =self.get_token()
        self.campaign_id = campaign_id
        self.placement_id = placement_id


    __appnexus_url = 'https://api.appnexus.com/'
    __last_token = None
    __last_token_time = None
    __two_hours = datetime.timedelta(hours=1, minutes=55)

    def get_token(self):
        global _last_token, _last_token_time
        _two_hours = datetime.timedelta(hours=1, minutes=55)
        if _last_token and utils.get_current_time() - _last_token_time < _two_hours:
            return _last_token
        try:
            auth_url = self.__appnexus_url + "auth"
            data = {"auth": settings.NEXUS_AUTH_DATA}
            auth_request = requests.post(auth_url, data=json.dumps(data))
            response = json.loads(auth_request.content)
            try:
                response['response']['error']
                print "get campaign by id - " + response['response']['error']
            except:
                pass
            _last_token = response['response']['token']
            _last_token_time = utils.get_current_time()
            return _last_token
        except:
            print "get token - " + response['response']['error']
            return 503

    def get_campaign_by_id(self, camp_id):
        url = self.__appnexus_url+'campaign?id={0}'.format(camp_id)
        headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
        try:
            campaign = json.loads(requests.get(url, headers=headers).content)
            try:
                campaign['response']['error']
                print "get campaign by id - " + campaign['response']['error']
                return 404
            except:
                pass
            print 'Campaign_id = '+str(campaign['response']['campaign']['profile_id'])
            return campaign['response']['campaign']['profile_id'], campaign['response']['campaign']['advertiser_id']
        except:
            print "get campaign by id - Not connect to appnexus server "
            return 503

    def get_profile_by_id(self, profile_id):
        url = self.__appnexus_url+'profile?id={0}'.format(profile_id)
        headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
        try:
            profile = json.loads(requests.get(url, headers=headers).content)
            try:
                profile['response']['error']
                print "get profile by id - " + profile['response']['error']
                return 404
            except:
                pass
            print 'platform_placement_targets = '+str(profile['response']['profile']['platform_placement_targets'])
            return profile['response']['profile']['platform_placement_targets']
        except:
            print "get profile by id - Not connect to appnexus server "
            return 503

    # 4 - white / 2 - black / 1 - suspend
    def update_profile_by_id(self, platform_placement_targets, placement_id, profile_id, advertiser_id, stateRtb):
        if platform_placement_targets is None:
            platform_placement_targets = []
        try:
            url = self.__appnexus_url + 'profile?id={0}&advertiser_id={1}'.format(profile_id, advertiser_id)
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            for one_placement in placement_id:
                if stateRtb == 1 or stateRtb == 2:
                    state = "exclude"
                elif stateRtb == 4:
                    state = "include"
                platform_placement_targets.append({
                    "id": one_placement,
                    "action": state,
                    "deleted": False
                })

            data = json.dumps({
                "profile":
                    {
                        "platform_placement_targets": platform_placement_targets
                    }
            })

            changeState = json.loads(requests.put(url, data=data, headers=headers).content)
            try:
                changeState['response']['error']
                print "get profile by id - " + changeState['response']['error']
                return 404
            except:
                pass
            print 'update_profile_by_id - ' + changeState['response']['status']
            return changeState['response']['status']
        except:
            print "update_profile_by_id - Not connect to appnexus server "
            return 503

    def change_state_placement(self, state):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            profile_id, advertiser_id = self.get_campaign_by_id(self.campaign_id)
            platform_placement_targets = self.get_profile_by_id(profile_id)
            if platform_placement_targets is None:
                updated_profile = self.update_profile_by_id(None, self.placement_id, profile_id, advertiser_id, state)
            else:
                updated_profile = self.update_profile_by_id(platform_placement_targets, self.placement_id, profile_id, advertiser_id, state)
            print updated_profile
            return updated_profile
        except:
            print "change state placement - Not connect to appnexus server "
            return 503

    # 4 - white / 2 - black / 1 - suspend
    def suspend_state_middleware(self):
        suspendState = ModelPlacementState.objects.filter(state=1)
        if len(suspendState) < 1:
            return None
        toWhitelist = []
        for oneState in suspendState:
            now = datetime.datetime.now(pytz.timezone('UTC'))
            if oneState.suspend < now:
                oneState.state = 4
                oneState.save()
                headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
                profile_id, advertiser_id = self.get_campaign_by_id(oneState.campaign_id)
                platform_placement_targets = self.get_profile_by_id(profile_id)
                if platform_placement_targets is None:
                    updated_profile = self.update_profile_by_id(None, [oneState.placement_id],
                                                                profile_id, advertiser_id, 4)
                else:
                    updated_profile = self.update_profile_by_id(platform_placement_targets, [oneState.placement_id],
                                                                profile_id, advertiser_id, 4)
                toWhitelist.append(str(oneState.placement_id) + ' to white ' + updated_profile)
                print str(oneState.placement_id) + ' to white ' + updated_profile
            else:
                continue
        return toWhitelist

    def remove_placement_from_targets_list(self):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            profile_id, advertiser_id = self.get_campaign_by_id(self.campaign_id)
            platform_placement_targets = self.get_profile_by_id(profile_id)
            if platform_placement_targets is None:
                print "remove_placement_from_targets_list - Not found target list "
                return 'OK'
            else:
                for target in platform_placement_targets:
                    if target['id'] == self.placement_id[0]:
                        platform_placement_targets.remove(target)
                url = self.__appnexus_url + 'profile?id={0}&advertiser_id={1}'.format(profile_id, advertiser_id)
                headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
                data = json.dumps({
                    "profile":
                        {
                            "platform_placement_targets": platform_placement_targets
                        }
                })
                changeState = json.loads(requests.put(url, data=data, headers=headers).content)
                try:
                    changeState['response']['error']
                    print "get profile by id - " + changeState['response']['error']
                    return 404
                except:
                    pass
                if changeState['response']['status'] == 'OK':
                    ModelPlacementState.objects.filter(placement_id=self.placement_id[0]).delete()
                else:
                    print "remove_placement_from_targets_list - Error db"
                    return 404
            if changeState['response']['status'] == 'OK':
                return changeState['response']['status']
            else:
                return 404
        except:
            print "remove_placement_from_targets_list - Not connect to appnexus server "
            return 503


    def placement_targets_list(self):
        # if load_depending_data(self.get_token(), True, False):
        #     print "ssss"
        #
        # else:
        #     return None
        allProfile = Campaign.objects.select_related("profile").filter(state='active', profile__platform_placement_targets__isnull=False).values('id', 'profile_id', 'profile__platform_placement_targets')
        for profile in allProfile:
            string = profile['profile__platform_placement_targets']
            #k = json.loads('{'+profile['profile__platform_placement_targets']+'}')
            print string.decode('utf-8', 'ignore')
            print string

