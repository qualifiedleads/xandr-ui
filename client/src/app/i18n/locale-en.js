(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .constant('EnglishTranslations', {
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
          'LAST_7_DAYS': 'Last 7 days',
          'CURRENT_WEEK': 'Current week',
          'LAST_WEEK': 'Last week',
          'CURRENT_MONTH': 'Current month',
          'LAST_MONTH': 'Last month',
          'CUSTOM': 'Custom'
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
            "SPENT":"Spent",
            "CONV":"Conv",
            "IMP":"Imp",
            "CLICKS":"Clicks",
            "CPC":"CPC",
            "CPM":"CPM",
            "CVR":"CVR",
            "CTR":"CTR",
            "STATS":"Stats"
          }
        },
        'CHECKBOX':{
          "IMPRESSIONS":"Impressions",
          "CPA":"CPA",
          "CPC":"CPC",
          "CLICKS":"Clicks",
          "MEDIA_SPENT":"Media Spent",
          "CONVERSIONS":"Conversions",
          "CTR":"CTR"
        }
      }
    })

})();
