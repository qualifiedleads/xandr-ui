(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .constant('EnglishTranslations', {
      'COMMON': {
        'GO-TO-ADMIN-PANEL': 'Admin panel',
        'LOGOUT': 'Log out',
        'TO-MAIN-PAGE': 'Home',
        'CANCEL': 'Cancel'
      },
      'AUTH': {
        'EMAIL-OR-PASSWORD-EMPTY': 'Email or Password is empty',
        'GO_BUTTON': 'GO',
        'MAIL-REQUIRED': 'Your email is required',
        'MAIL-VALID': 'Your email is not valid.',
        'PASSWORD-REQUIRED': 'Your password is required.',
        'MAIL-PLACEHOLDER': 'Enter your email',
        'MAIL-PASSWORD': 'Enter your password',
        'MAIL-SUBMIT': 'Submit'
      },
      "ADMIN": {
        "ANU": {
          'ADD-NEW-USER': 'Add new user',
          'EMAIL': 'Email',
          'PASSWORD': 'Password',
          'CONFIRM-PASSWORD': 'Confirm password',
          'USER-NAME': 'User name',
          'FIRST-NAME': 'First name',
          'LAST-NAME': 'Last name',
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
        "LIST-USER": {
          "TITLE": "List of users",
          'EMAIL': 'Email',
          'PASSWORD': 'Password',
          'CONFIRM-PASSWORD': 'Confirm password',
          'USER-NAME': 'User name',
          'FIRST-NAME': 'First name',
          'LAST-NAME': 'Last name',
          'APNEXUS-ID': 'AppNexus user id',
          'APNEXUS-NAME': 'AppNexus user name',
          'PERMISSION': 'Permission'
        },
        'TECHNICAL-WORK': {
          'EDIT-USERS': 'Edit users',
          'TECH-WORK': 'Technical works',
          'ADVERTISER-LIST': 'Advertiser list',
          'TECH-WORK-SWITCHER': 'carrying out technical works on the site',
          'TECH-JOURNAL': 'Journal of carrying out technical works Journal',
          'TECH-DATE': 'Date',
          'TECH-STATUS': 'Status',
          'TECH-STATUS-BANNER': 'BANNER STATUS',
          'APNEXUS-ID': 'Id пользователя AppNexus',
          'APNEXUS-NAME': 'Имя польeзователя AppNexus',
          'PERMISSION': 'Разрешение'
        },
        "ADVERTISER-LIST": {
          'NAME': 'Name',
          'ID': 'Id',
          'AD-TYPE': 'Type of the advertiser',
          'DATA_SOURCE': 'Data source',
          'DATA-FOR-RULES': 'Data for rules'
        }
      },
      'INDEX': {
        'ADVERTISER_TITLE': 'Stats for',
        'LEFT_NAV': {
          'HOME': 'Home',
          'CAMPAIGN': "Campaign",
          'CPA': "CPA",
          'BILLING': "Billing",
          'OPTIMIZER': "Optimizer",
          'BCC': "Bulk campaigns creation",
          'ACPMC': "Automatic CPM control",
          'Rules': "Rules",
          'EXPERT': "Expert"
        }
      },
      'MAIN': {
        'HOME': "Home",
        'ADVERTISER_UPDATED': 'Advertiser updated',
        'UPDATE_CAMPAIGN': 'Update campaign',
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
          'COLUMNS': {
            "TOTALS": "TOTALS",
            "SPENT": "Spent",
            "CONV": "Conv",
            "IMP": "Imp",
            "CLICKS": "Clicks",
            "CPC": "CPC",
            "CPM": "CPM",
            "CVR": "CVR",
            "CTR": "CTR"
          }
        },
        'CAMPAIGN': {
          'COLUMNS': {
            "CAMPAIGN": "Campaign",
            "PLACEMENT": "Placement",
            "NETWORK": "Network + Publisher",
            "SPENT": "Spent",
            "CONV": "Conv",
            "IMP": "Imp",
            "CPA": "CPA",
            "CLICKS": "Clicks",
            "CPC": "CPC",
            "CPM": "CPM",
            "CVR": "CVR",
            "CTR": "CTR",
            "IMPS_VIEWED": "Visible imp",
            "VIEW_MEASURED_IMPS": "Measured imp",
            "VIEW_MEASUREMENT_RATE": "Viewed measurement rate",
            "VIEW_RATE": "Viewed rate",
            "STATS": "Stats",
            "AD-STARTS": "Ad starts",
            "FILL-RATE": "Fill rate",
            "PROFIT-LOSS": "Profit/loss",
            "FILL-RATE-HOUR": "Delta Fill Rate",
            "PROFIT-LOSS-HOUR": "Delta profit/loss",
          }
        },
        'CHECKBOX': {
          "ad_starts": "ad_starts",
          "fill_rate": "fill_rate",
          "profit_loss": "profit_loss",
          "IMPRESSIONS": "Impressions",
          "CVR": "CVR",
          "CPC": "CPC",
          "CLICKS": "Clicks",
          "COST": "$ Cost",
          "CONVERSIONS": "Conversions",
          "CTR": "CTR"
        }
      },
      "CAMP": {
        "NAME": "Campaign:",
        "LINE_ITEM": "Line item:",
        "GO-OPTIMISER": "Go to the Optimiser",
        'CHECKBOX': {
          "IMPRESSIONS": "Impressions",
          "CPA": "CPA",
          "CPC": "CPC",
          "CLICKS": "Clicks",
          "COST": "$ Cost",
          "CONVERSIONS": "Conversions",
          "CTR": "CTR"
        },
        'CAMPAIGN': {
          'COLUMNS': {
            "CAMPAIGN": "Campaign",
            "PLACEMENT": "Placement",
            'DOMAIN': 'Domain',
            "NETWORK": "Network + Seller",
            "SPENT": "Spent",
            "CONV": "Conv",
            "COST": "Cost",
            "IMP": "Imp",
            "CPA": "CPA",
            "CLICKS": "Clicks",
            "CPC": "CPC",
            "CPM": "CPM",
            "CVR": "CVR",
            "CTR": "CTR",
            "IMPS_VIEWED": "Visible imp",
            "VIEW_MEASURED_IMPS": "Measured imp",
            "VIEW_MEASUREMENT_RATE": "Viewed measurement rate",
            "VIEW_RATE": "Viewed rate",
            "STATS": "Stats",
            "STATE": "State",
            "PREDICTION_1": "Prediction №1",
            "PREDICTION_2": "Prediction №2"
          }
        }
      },
      'CO': {
        'NO-ITEMS-CHOSEN': 'No items chosen. Please, choose at least 1 item',
        'SEND-TO-SUSPEND-LIST': 'Send to "Suspend list" until I get to it',
        'SPECIFIC-DATE': 'Specific date',
        '7-DAYS': '7 days',
        '3-DAYS': '3 days',
        '24-HRS': '24 hrs',
        'TEMP-SUSPEND': 'Temp. Suspend',
        'BLACKLISTED': 'Blacklisted',
        'WHITELIST': 'Whitelist',
        'SUSPEND': 'Suspend',
        'OPTIMIZER': 'Optimizer',
        'BLOCKING': 'Blocking',
        'DEVICE-AND-SUPPLY-TYPE': 'Device and Supply Type',
        'GEO': 'Geo',
        'DOMAIN': 'Domain',
        'DOMAIN-LISTS': 'Domain Lists',
        'DOMAINS': 'Domains',
        'RULES': 'Rules for All Domains:',
        'OPTIMISER-FOR': 'Optimiser for:',
        'CAMPAIGN-HOME': 'back to Campaign Home'
      },
      "RULESC": {
        'OPTIMISER-FOR': 'Rules for:',
        'RULES': 'Rules for All Domains:',
        'ADD-RULE': 'Add rule',
        'SAVE-RULE': 'Save rule',
        'RULE-DELETE': 'RULE DELETE'
      },
      'VBE': {
        'PAGE-NAME': 'Valuation by expert:',
        'CALCULATE-AUC': 'Calculate AUC',
        'CREATE-TEST-SET': 'Create test set'
      },
      "BCC": {
        "SELECT-CAMPAIGN": "Select Campaign:",
        "ADD-DOMAIN": "Put domain:",
        "PLACEHOLDER-DOMAIN": "Put single domain in one line",
        "CREATE": "Create"
      },
      "ACPMC": {
        "CHOICE-LIST": "Select method:",
        "SEND": 'Save'
      },
    })
})();
