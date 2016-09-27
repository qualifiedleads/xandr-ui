(function() {
  'use strict';

  angular
  .module('pjtLayout')
  .constant('EnglishTranslations', {
    'COMMON': {
      'GO-TO-ADMIN-PANEL': 'Admin panel',
      'LOGOUT': 'Log out',
      'TO-MAIN-PAGE': 'Main page',
      'CANCEL': 'Cancel'
    },
    'AUTH':{
      'EMAIL-OR-PASSWORD-EMPTY':'Email or Password is empty',
      'GO_BUTTON':'GO',
      'MAIL-REQUIRED': 'Your email is required',
      'MAIL-VALID': 'Your email is not valid.',
      'PASSWORD-REQUIRED': 'Your password is required.',
      'MAIL-PLACEHOLDER': 'Enter your email',
      'MAIL-PASSWORD': 'Enter your password',
      'MAIL-SUBMIT': 'Submit'
    },
    "ADMIN":{
      "ANU":{
        'ADD-NEW-USER':'Add new user',
        'EMAIL':'Email',
        'PASSWORD':'Password',
        'CONFIRM-PASSWORD':'Confirm password',
        'USER-NAME':'User name',
        'FIRST-NAME':'First name',
        'LAST-NAME':'Last name',
        'MAIL-REQUIRED': 'Your email is required',
        'MAIL-VALID': 'Your email is not valid',
        'PASSWORD-REQUIRED': 'Your password is required',
        'CONFIRM-PASSWORD-REQUIRED': 'Password confirmation is required',
        'CONFIRM-PASSWORD-INCORRECT': 'Incorrect password',
        'USER-NAME-REQUIRED': 'User name is required',
        'FIRST-NAME-REQUIRED': 'First name is required',
        'LAST-NAME-REQUIRED': 'Last name is required',
        'SELECT-PERMISSION': 'Select the type of permission',
        'SELECT-NEXUS-USER': 'Select the appnexus user',
        'SUBMIT': 'Create'
      },
      "LIST-USER" : {
        "TITLE" : "List of users",
        'EMAIL':'Email',
        'PASSWORD':'Password',
        'CONFIRM-PASSWORD':'Confirm password',
        'USER-NAME':'User name',
        'FIRST-NAME':'First name',
        'LAST-NAME':'Last name',
        'APNEXUS-ID':'AppNexus user id',
        'APNEXUS-NAME':'AppNexus user name',
        'PERMISSION':'Permission'
      }
    },
    'INDEX':{
      'ADVERTISER_TITLE':'Stats for',
      'LEFT_NAV':{
        'HOME':"Home",
        'CAMPAIGN':"Campaign",
        'BILLING':"Billing",
        'OPTIMIZER':"Optimizer"
      }
    },
    'MAIN': {
      'HOME':"Home",

      'DATE_PICKER': {
        'YESTERDAY': 'Yesterday',
        'LAST_3_DAYS': 'Last 3 days',
        'LAST_7_DAYS': 'Last 7 days',
        'LAST_14_DAYS': 'Last 14 days',
        'LAST_21_DAYS': 'Last 21 days',
        'CURRENT_MONTH': 'Current month',
        'LAST_MONTH': 'Last month',
        'LAST_90_DAYS': 'Last 90 days',
        'ALL_TIME': 'All times'
      },
      'TOTALS': {
        'COLUMNS':{
          "TOTALS":"TOTALS",
          "SPENT":"Spent",
          "CONV":"Conv",
          "IMP":"Imp",
          "CLICKS":"Clicks",
          "CPC":"CPC",
          "CPM":"CPM",
          "CVR":"CVR",
          "CTR":"CTR"
        }
      },
      'CAMPAIGN': {
        'COLUMNS':{
          "CAMPAIGN":"Campaign",
          "PLACEMENT": "Placement",
          "NETWORK":"Network + Publisher",
          "SPENT":"Spent",
          "CONV":"Conv",
          "IMP":"Imp",
          "CPA":"CPA",
          "CLICKS":"Clicks",
          "CPC":"CPC",
          "CPM":"CPM",
          "CVR":"CVR",
          "CTR":"CTR",
          "IMPS_VIEWED":"Visible imp",
          "VIEW_MEASURED_IMPS":"Measured imp",
          "VIEW_MEASUREMENT_RATE":"Viewed measurement rate",
          "VIEW_RATE":"Viewed rate",
          "STATS":"Stats"
        }
      },
      'CHECKBOX':{
        "IMPRESSIONS":"Impressions",
        "CVR":"CVR",
        "CPC":"CPC",
        "CLICKS":"Clicks",
        "COST":"$ Cost",
        "CONVERSIONS":"Conversions",
        "CTR":"CTR"
      }
    },
    "CAMP": {
      "NAME":"Campaign",
      "GO-OPTIMISER": "Go to the Optimiser",
      'CHECKBOX':{
        "IMPRESSIONS":"Impressions",
        "CPA":"CPA",
        "CPC":"CPC",
        "CLICKS":"Clicks",
        "COST":"$ Cost",
        "CONVERSIONS":"Conversions",
        "CTR":"CTR"
      },
      'CAMPAIGN': {
        'COLUMNS':{
          "CAMPAIGN":"Campaign",
          "PLACEMENT": "Placement",
          "NETWORK":"Network + Seller",
          "SPENT":"Spent",
          "CONV":"Conv",
          "COST":"Cost",
          "IMP":"Imp",
          "CPA":"CPA",
          "CLICKS":"Clicks",
          "CPC":"CPC",
          "CPM":"CPM",
          "CVR":"CVR",
          "CTR":"CTR",
          "IMPS_VIEWED":"Visible imp",
          "VIEW_MEASURED_IMPS":"Measured imp",
          "VIEW_MEASUREMENT_RATE":"Viewed measurement rate",
          "VIEW_RATE":"Viewed rate",
          "STATS":"Stats"
        }
      }
    },
    'CO':{
      'NO-ITEMS-CHOSEN' : 'No items chosen. Please, choose at least 1 item',
      'SEND-TO-SUSPEND-LIST' : 'Send to "Suspend list" until I get to it',
      'SPECIFIC-DATE' : 'Specific date',
      '7-DAYS' : '7 days',
      '3-DAYS' : '3 days',
      '24-HRS' : '24 hrs',
      'TEMP-SUSPEND' : 'Temp. Suspend',
      'BLACKLISTED' : 'Blacklisted',
      'WHITELIST' : 'Whitelist',
      'SUSPEND' : 'Suspend',
      'OPTIMIZER' : 'Optimizer',
      'BLOCKING' : 'Blocking',
      'DEVICE-AND-SUPPLY-TYPE' : 'Device and Supply Type',
      'GEO' : 'Geo',
      'DOMAIN' : 'Domain',
      'DOMAIN-LISTS' : 'Domain Lists',
      'DOMAINS' : 'Domains',
      'RULES': 'Rules for All Domains:',
      'OPTIMISER-FOR':'Optimiser for',
      'CAMPAIGN-HOME': 'back to Campaign Home'
    }
  })
})();