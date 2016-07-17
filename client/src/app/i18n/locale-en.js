(function() {
	'use strict';

	angular
		.module('pjtLayout')
		.constant('EnglishTranslations', {
			'AUTH':{
				'GO_BUTTON':'GO'
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
						"NETWORK":"Network+Publisher",
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
			},
			"CAMP": {
				"NAME":"Campaign"
			},
      "CO":{
        "NAME":"Campaign optimiser",
        "ORIGINAL": "Original",
        "OPTIMISED": "Optimised (Whitelist)",
        "RULES": "Rules for All Domains:",
        "SPENDS": "if an app/domain spends more than",
	      "CONVERSIONS1": "and conversions are 0 then",
				"APP": "if an app/domain has more than",
	      "CONVERSIONS2": "imp. and conversions are 0 then",
	      "UNDISCLOSED": "if an app/domain is marked as \"Undisclosed\"",
	      "DOMAIN-RULES": "Domain-specific rules:",
	      "CURRENT-LIST": "Current list of placements - Live now",
      }
		})

})();
