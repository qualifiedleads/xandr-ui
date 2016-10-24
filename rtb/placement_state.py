from models.placement_state import PlacementState as ModelPlacementState
from django.conf import settings
import json
import requests
import datetime
import utils


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
        if self.__last_token and utils.get_current_time() - self.__last_token_time < self.__two_hours:
            return self.__last_token
        try:
            auth_url = self.__appnexus_url + "auth"
            data = {"auth": settings.NEXUS_AUTH_DATA}
            auth_request = requests.post(auth_url, data=json.dumps(data))
            response = json.loads(auth_request.content)
            self.__last_token = response['response']['token']
            self.__last_token_time = utils.get_current_time()
            return self.__last_token
        except:
            return None

    def get_campaign_by_id(self,camp_id):
        url = self.__appnexus_url+'campaign?id={0}'.format(camp_id)
        headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
        try:
            campaign = json.loads(requests.get(url, headers=headers).content)
            print 'Campaign_id = '+str(campaign['response']['campaign']['profile_id'])
            return campaign['response']['campaign']['profile_id'], campaign['response']['campaign']['advertiser_id']
        except:
            print None

    def get_profile_by_id(self, profile_id):
        url = self.__appnexus_url+'profile?id={0}'.format(profile_id)
        headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
        try:
            profile = json.loads(requests.get(url, headers=headers).content)
            print 'platform_placement_targets = '+str(profile['response']['profile']['platform_placement_targets'])
            return profile['response']['profile']['platform_placement_targets']
        except:
            print None

    # 4 - white / 2 - black / 1 - suspend
    def update_profile_by_id(self, platform_placement_targets, placement_id, profile_id, advertiser_id):
        if platform_placement_targets is None:
            platform_placement_targets = []
        try:
            url = self.__appnexus_url + 'profile?id={0}&advertiser_id={1}'.format(profile_id, advertiser_id)
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            for one_placement in placement_id:
                localState = ModelPlacementState.objects.get(placement_id=one_placement)
                if localState.state == 1 or localState.state == 2:
                    state = "exclude"
                elif localState.state == 4:
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
            try:
                changeState = json.loads(requests.put(url, data=data, headers=headers).content)
            except:
                return None
            try:
                for one_placement in placement_id:
                    ModelPlacementState.objects.filter(placement_id=one_placement).update(change=False)
            except:
                return None
            print changeState['response']['status']
            return changeState['response']['status']
        except:
            return None


    def change_state_placement(self):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            profile_id, advertiser_id = self.get_campaign_by_id(self.campaign_id)
            platform_placement_targets = self.get_profile_by_id(profile_id)
            if platform_placement_targets is None:
                updated_profile = self.update_profile_by_id(None, self.placement_id, profile_id, advertiser_id)
            else:
                updated_profile = self.update_profile_by_id(platform_placement_targets, self.placement_id, profile_id, advertiser_id)
            print updated_profile
            return updated_profile
        except:
            return None