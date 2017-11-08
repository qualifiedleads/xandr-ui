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


