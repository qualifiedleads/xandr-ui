from models.placement_state import PlacementState as ModelPlacementState, LastModified
from django.conf import settings
from models.models import Campaign, Profile, LastToken
from django.db.models import Max, Q, F
from rtb.cron import load_depending_data
from django.utils import timezone
from datetime import timedelta
import unicodedata
import re
import json
import requests
import datetime
import pytz
import utils

change_state = None

class PlacementState:
    def __init__(self, campaign_id, placement_id):
        self.campaign_id = campaign_id
        self.placement_id = placement_id


    __appnexus_url = 'https://api.appnexus.com/'
    __last_token = None
    __last_token_time = None
    __two_hours = datetime.timedelta(hours=1, minutes=55)

    def get_token(self):
        _two_hours = datetime.timedelta(hours=1, minutes=55)
        lastToken = LastToken.objects.filter(name='token')
        if len(lastToken) >= 1:
            if utils.get_current_time() - lastToken[0].date < _two_hours:
                return lastToken[0].token
        else:
            tempDate = utils.get_current_time()-_two_hours
            LastToken(name='token', token='', date=tempDate).save()
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
            last_token = response['response']['token']
            _last_token_time = utils.get_current_time()
            LastToken.objects.filter(name='token').update(token=last_token, date=_last_token_time)
            return last_token
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

    def suspend_state_middleware(self):
        suspendState = ModelPlacementState.objects.filter(state=1)
        if len(suspendState) < 1:
            return None
        toWhitelist = []
        for oneState in suspendState:
            now = datetime.datetime.now(pytz.timezone('UTC'))
            if oneState.suspend < now:
                oneState.state = 0
                oneState.change = True
                oneState.suspend = None
                oneState.save()
                toWhitelist.append(str(oneState.placement_id) + ' - update')
            else:
                continue
        print 'Suspend state middleware: ' + str(toWhitelist)

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
        try:
            change_state = LastModified.objects.filter(type='platform_placement_targets')
            if len(change_state) >= 1:
                if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[0].date >= timedelta(minutes=45):
                    LastModified.objects.filter(type='platform_placement_targets').delete()
                else:
                    print "placement_targets_list wait..."
                    return None

            LastModified(type='platform_placement_targets', date=timezone.make_aware(datetime.datetime.now(),
                                                                                    timezone.get_default_timezone())).save()
            print 'change state by state - start'
            lasmoModified = LastModified.objects.filter(type='profile')
            if len(lasmoModified) >= 1:
                minutesAgo = LastModified.objects.filter(type='profile')[0].date
            else:
                minutesAgo = Profile.objects.all().values('last_modified').order_by('last_modified')[0]['last_modified']
            now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
            print 'from: {0} to {1}'.format(minutesAgo, now)
            print 'send to appnexus'
            try:
                self.change_state_placement_by_cron()
            except Exception as e:
                print 'Error: ' + str(e)
            print 'upload from appnexus'
            try:
                load_depending_data(self.get_token(), True, False, isLastModified=True)
            except ValueError, e:
                print "Failed to load profile platform placement targets. Error: " + str(e)
                return False
            print 'End upload from appnexus'
            allProfile = Campaign.objects.select_related("profile")\
                .filter(
                    state='active',
                    profile__last_modified__range=[minutesAgo, now]
                )\
                .values('id', 'profile_id', 'profile__platform_placement_targets', 'profile__last_modified')
            for profile in allProfile:
                LastModified.objects.filter(type='platform_placement_targets').update(date=timezone.make_aware(datetime.datetime.now(),
                                                                                    timezone.get_default_timezone()))
                string = profile['profile__platform_placement_targets']
                if string is None:
                    ModelPlacementState.objects.filter(campaign_id=profile['id'], change=False).delete()
                    print "Delete all placement for campaign - " + str(profile['id'])
                    continue
                placementTargets = unicodedata.normalize('NFKD', string).encode('utf-8', 'ignore')
                placementTargets = re.sub('\'', '"', placementTargets)
                placementTargets = re.sub('u"', '"', placementTargets)
                placementTargets = placementTargets[2:-2]
                placementTargets = placementTargets.split('}, {')
                placeTarget = []
                for items in placementTargets:
                    items = items.split(', ')
                    tempDictionary = {}
                    for item in items:
                        item = item.split(': ')
                        item[0] = re.sub('\"', '', item[0])
                        item[1] = re.sub('\"', '', item[1])
                        tempDictionary[item[0]] = item[1]
                    placeTarget.append(tempDictionary)
                newPlacementFromAppnexus = []
                for placement in placeTarget:
                    newPlacementFromAppnexus.append(int(placement['id']))
                    dbPlacement = ModelPlacementState.objects\
                        .filter(placement_id=int(placement['id']), campaign_id=profile['id'])
                    if not dbPlacement:
                        if placement['action'] == 'exclude':
                            state = 2
                        else:
                            state = 4
                        try:
                            ModelPlacementState(
                                placement_id=int(placement['id']),
                                campaign_id=profile['id'],
                                state=state,
                                suspend=None,
                                change=False
                            ).save()
                            print 'Added placement {0} and campaign {1}'.format(placement['id'], profile['id'])
                        except ValueError, e:
                            print "Can't save placement state. Error: " + str(e)
                    else:
                        try:
                            if dbPlacement[0].state == 1 and placement['action'] == 'exclude':
                                continue
                            if placement['action'] == 'exclude':
                                state = 2
                            else:
                                state = 4
                            obj, created = ModelPlacementState.objects.update_or_create(
                                placement_id=int(placement['id']),
                                campaign_id=profile['id'],
                                defaults={"state": state, "suspend": None, "change": False})
                            print (obj, created)
                        except ValueError, e:
                            print "Can't update placement state. Error: " + str(e)
                tempOldPlacement = ModelPlacementState.objects\
                        .filter(Q(campaign_id=profile['id']), Q(change=False))\
                        .values('placement_id')
                oldPlacement = []
                if len(tempOldPlacement) >= 1:
                    for item in tempOldPlacement:
                        oldPlacement.append(item['placement_id'])
                for i in newPlacementFromAppnexus:
                    if i in oldPlacement:
                        oldPlacement.remove(i)
                ModelPlacementState.objects.filter(campaign_id=profile['id'], placement_id__in=oldPlacement).delete()
                print 'Remove old state from our table: ' + str(oldPlacement)
            try:
                LastModified.objects.filter(type='platform_placement_targets').delete()
            except Exception, e:
                print 'Error: ' + str(e)
            if not lasmoModified:
                LastModified(type='profile', date=now).save()
            else:
                lastminutesAgo = Profile.objects.latest('last_modified').last_modified
                LastModified.objects.filter(type='profile').update(date=lastminutesAgo)
                print 'Last modified profile: {0} '.format(lastminutesAgo)
            print "End platform placement targets"
        except Exception, e:
            LastModified.objects.filter(type='platform_placement_targets').delete()
            print 'Error: ' + str(e)

    def change_state_by_state(self, stateGet):
        try:
            tempState = stateGet
            whiteBlackState = ModelPlacementState.objects.filter(Q(state=stateGet) & Q(change=True))
            if len(whiteBlackState) < 1:
                return None
            tempCompId = []
            for i in whiteBlackState:
                tempCompId.append(i.campaign_id)
            tempCompId = set(tempCompId)

            campaignAndPlacement = []
            for comp in tempCompId:
                nextPlacement = []
                for oneState in whiteBlackState:
                    if comp == oneState.campaign_id:
                        nextPlacement.append(oneState.placement_id)
                campaignAndPlacement.append({'campaign_id': comp, 'placement_id': nextPlacement})

            if stateGet == 1:
                tempState = 2

            for campaign in campaignAndPlacement:
                campaign_id = campaign['campaign_id']
                placement_id = campaign['placement_id']
                profile_id, advertiser_id = self.get_campaign_by_id(campaign_id)
                platform_placement_targets = self.get_profile_by_id(profile_id)
                if platform_placement_targets is None:
                    updated_profile = self.update_profile_by_id(None, placement_id, profile_id, advertiser_id, tempState)
                    if updated_profile == 'OK':
                        for placement in placement_id:
                            obj, created = ModelPlacementState.objects.update_or_create(
                                placement_id=int(placement),
                                campaign_id=int(campaign_id),
                                defaults={"state": stateGet, "change": False})
                    print 'List for '+str(placement_id) + ' to platform placement targets, profile: ' + str(updated_profile)
                else:
                    updated_profile = self.update_profile_by_id(platform_placement_targets, placement_id,
                                                                profile_id, advertiser_id, tempState)
                    if updated_profile == 'OK':
                        for placement in placement_id:
                            obj, created = ModelPlacementState.objects.update_or_create(
                                placement_id=int(placement),
                                campaign_id=int(campaign_id),
                                defaults={"state": stateGet, "change": False})
                    print 'List for ' + str(placement_id) + ' to platform placement targets, profile: ' + str(updated_profile)
            print "Sync white and black list to platform placement targets."
            return True
        except:
            print "Fail sync white list to platform placement targets."
            return False

    def remove_placement_from_targets_list_by_cron(self, stateGet):
        try:
            whiteBlackState = ModelPlacementState.objects.filter(Q(state=stateGet) & Q(change=True))
            if len(whiteBlackState) < 1:
                return None
            tempCompId = []
            for i in whiteBlackState:
                tempCompId.append(i.campaign_id)
            tempCompId = set(tempCompId)

            campaignAndPlacement = []
            for comp in tempCompId:
                nextPlacement = []
                for oneState in whiteBlackState:
                    if comp == oneState.campaign_id:
                        nextPlacement.append(oneState.placement_id)
                campaignAndPlacement.append({'campaign_id': comp, 'placement_id': nextPlacement})

            for campaign in campaignAndPlacement:
                campaign_id = campaign['campaign_id']
                placement_id = campaign['placement_id']
                profile_id, advertiser_id = self.get_campaign_by_id(campaign_id)
                platform_placement_targets = self.get_profile_by_id(profile_id)

                if platform_placement_targets is None:
                    print "remove_placement_from_targets_list - Not found target list "
                else:
                    for placement in placement_id:
                        for target in platform_placement_targets:
                            if target['id'] == placement:
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
                        ModelPlacementState.objects.filter(placement_id__in=placement_id).delete()
                    else:
                        print "remove_placement_from_targets_list - Error db"
                        return 404
                    print 'List for ' + str(placement_id) + ' to platform placement targets, profile: ' + changeState['response']['status']
            print "Sync white list to platform placement targets."
            return True
        except:
            print "Fail sync white list to platform placement targets."
            return False

    def update_placement_state_in_our_table(self, campaign_id, arrayFromAppexus):
        campaign_id = 14574547
        arrayFromAppexus = [
                   {'action': 'exclude', 'deleted': False, 'id': 5988182},
                   {'action': 'exclude', 'deleted': False, 'id': 7043081},
                   {'action': 'exclude', 'deleted': False, 'id': 7043210},
                   {'action': 'include', 'deleted': False, 'id': 7043341},
                   {'action': 'include', 'deleted': False, 'id': 7043352},
                   {'action': 'exclude', 'deleted': False, 'id': 7043429},
                   {'action': 'include', 'deleted': False, 'id': 7043440},
                   {'action': 'include', 'deleted': False, 'id': 9293941}]
        for placement in arrayFromAppexus:
            dbPlacement = ModelPlacementState.objects \
                .filter(placement_id=int(placement['id']), campaign_id=campaign_id, change=False)
            if not dbPlacement:
                if placement['action'] == 'exclude':
                    state = 2
                else:
                    state = 4
                try:
                    ModelPlacementState(
                        placement_id=int(placement['id']),
                        campaign_id=campaign_id,
                        state=state,
                        suspend=None,
                        change=False
                    ).save()
                    print 'Added placement {0} and campaign {1}'.format(placement['id'], campaign_id)
                except ValueError, e:
                    print "Can't save placement state. Error: " + str(e)
            else:
                try:
                    if dbPlacement[0].state == 1 and placement['action'] == 'exclude':
                        continue
                    if placement['action'] == 'exclude':
                        state = 2
                    else:
                        state = 4
                    obj, created = ModelPlacementState.objects.update_or_create(
                        placement_id=int(placement['id']),
                        campaign_id=campaign_id,
                        defaults={"state": state, "suspend": None, "change": False})
                    print (obj, created)
                except ValueError, e:
                    print "Can't update placement state. Error: " + str(e)

        pass

    def change_state_placement_by_cron(self):
        try:
            #self.update_placement_state_in_our_table(None, None)
            change_state = LastModified.objects.filter(type='change_state_placement_by_cron')
            if len(change_state) >= 1:
                if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[0].date >= timedelta(minutes=45):
                    LastModified.objects.filter(type='change_state_placement_by_cron').delete()
                else:
                    print "placement_targets_list wait..."
                    return None

            LastModified(type='change_state_placement_by_cron', date=timezone.make_aware(datetime.datetime.now(),
                                                                                    timezone.get_default_timezone())).save()
            unactive = self.remove_placement_from_targets_list_by_cron(0)
            white = self.change_state_by_state(4)
            black = self.change_state_by_state(2)
            suspend = self.change_state_by_state(1)
            print "Sync: white - {0}, black - {1}, suspend - {2}, Unactive - {3}".format(white, black, suspend, unactive)
            try:
                LastModified.objects.filter(type='change_state_placement_by_cron').delete()
            except ValueError, e:
                print 'Error: ' + str(e)
        except ValueError, e:
            LastModified.objects.filter(type='change_state_placement_by_cron').delete()
            print 'Error: ' + str(e)
            return 503


