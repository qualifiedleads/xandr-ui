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
