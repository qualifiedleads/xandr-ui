from datetime import timedelta
from django.conf import settings
from django.utils import timezone
import rtb.utils as utils
import requests
import datetime
import json

from rtb.models import LastToken
from rtb.placement_state import PlacementState


class DomainListApi(PlacementState):

    def __init__(self, domain_id):
        self.domain_id = domain_id

    def addNewDomainList(self, newDomainList):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "domain-list"
            data = {
                "domain-list": {
                    "name": newDomainList['name'],
                    "domains": newDomainList['domains']
                }
            }
            auth_request = requests.post(auth_url, data=json.dumps(data), headers=headers)
            response = json.loads(auth_request.content)
            try:
                print "addNewDomainList Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']['domain-list']
        except Exception as error:
            print "addNewDomainList ERROR - " + error
            return error

    def getDomainListById(self):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "domain-list?id=" + self.domain_id
            auth_request = requests.get(auth_url, headers=headers)
            response = json.loads(auth_request.content)
            try:
                print "GetDomainListById Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']['domain-list']
        except Exception as error:
            print "GetDomainListById ERROR - " + error
            return error

    def removeDomainListById(self):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "domain-list?id=" + self.domain_id
            auth_request = requests.delete(auth_url, headers=headers)
            response = json.loads(auth_request.content)
            try:
                print "RemoveDomainListById Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']
        except Exception as error:
            print "RemoveDomainListById ERROR - " + error
            return error

    def updateDomainListById(self, newDomainList):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "domain-list?id=" + self.domain_id
            data = {
                "domain-list": {
                    "domains": newDomainList['domains']
                }
            }
            auth_request = requests.put(auth_url, data=json.dumps(data), headers=headers)
            response = json.loads(auth_request.content)
            try:
                print "addNewDomainList Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']['domain-list']
        except Exception as error:
            print "addNewDomainList ERROR - " + error
            return error

    def applyDomainListById(self, campaign_id, advertiser_id, action):
        try:
            campaign = self.getCampaignByCampaignIdAndadvertiserId(campaign_id, advertiser_id)
            if isinstance(campaign, basestring):
                return campaign

            profile = self.getProfileById(campaign['profile_id'])
            if isinstance(profile, basestring):
                return profile

            domain_list_targets = [{"id": self.domain_id}]
            if action == 'whitelist':
                domain_list_action = 'include'
            elif action == 'blacklist':
                domain_list_action = 'exclude'
            else:
                domain_list_action = 'exclude'
                domain_list_targets = None

            config = {
                "profile": {
                    "domain_list_targets": domain_list_targets,
                    "domain_list_action": domain_list_action
                }
            }

            return self.putProfileById(profile['id'], config)
        except Exception as error:
            print "applyDomainListById ERROR - " + error
            return error

    def getCampaignByCampaignIdAndadvertiserId(self, campaign_id, advertiser_id):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "campaign?id={0}&advertiser_id={1}".format(campaign_id, advertiser_id)
            request = requests.get(auth_url, headers=headers)
            response = json.loads(request.content)
            try:
                print "getCampaignByCampaignIdAndadvertiserId get campaign Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']['campaign']
        except Exception as error:
            print "getCampaignByCampaignIdAndadvertiserId ERROR - " + error
            return error

    def getProfileById(self, profile_id):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "profile?id={0}".format(profile_id)
            request = requests.get(auth_url, headers=headers)
            response = json.loads(request.content)
            try:
                print "getProfileById get profile Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']['profile']
        except Exception as error:
            print "getProfileById ERROR - " + error
            return error

    def putProfileById(self, profile_id, config):
        try:
            headers = {"Authorization": self.get_token(), 'Content-Type': 'application/json'}
            auth_url = self._PlacementState__appnexus_url + "profile?id={0}".format(profile_id)
            request = requests.put(auth_url, data=json.dumps(config), headers=headers)
            response = json.loads(request.content)
            try:
                print "putProfileById get profile Error - " + response['response']['error']
                return response['response']['error']
            except:
                pass
            return response['response']['profile']
        except Exception as error:
            print "putProfileById ERROR - " + error
            return error