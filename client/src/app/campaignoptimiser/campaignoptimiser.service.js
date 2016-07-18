(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('CampaignOptimiser', CampaignOptimiser);

  /** @ngInject */
  function CampaignOptimiser($http) {
    var _this = this;

    function campaignDomains(id, from, to, skip, take, order, filter) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        params: {id:id, from_date: from, to_date: to, skip: skip, take: take, order: order, filter:filter}
      })
        .then(function (res) {
          return res.data;

        }).catch(function () {
          return [{
            "placement":"CNN.com",
            "NetworkPublisher":"Google Adx",
            "conv":"8",
            "imp":"5500",
            "clicks":"21",
            "cpc":"$0,31",
            "cpm":"$1,38",
            "cvr":"",
            "ctr":"",
            "state": {
              "whiteList": "true",
              "blackList": "false",
              "suspended": "false"
            }
          },
            {
              "placement":"Hidden",
              "NetworkPublisher":"PubMatic",
              "conv":"3",
              "imp":"5500",
              "clicks":"21",
              "cpc":"$0,31",
              "cpm":"$1,38",
              "cvr":"",
              "ctr":"",
              "state": {
                "whiteList": "false",
                "blackList": "true",
                "suspended": "false"
              }
            },
            {
              "placement":"BBC.com",
              "NetworkPublisher":"OpenX",
              "conv":"1",
              "imp":"5500",
              "clicks":"21",
              "cpc":"$0,31",
              "cpm":"$1,38",
              "cvr":"",
              "ctr":"",
              "state": {
                "whiteList": "false",
                "blackList": "false",
                "suspended": "true"
              }
            },
            {
              "placement":"msn.com",
              "NetworkPublisher":"Rubicon",
              "conv":"8",
              "imp":"5500",
              "clicks":"21",
              "cpc":"$0,31",
              "cpm":"$1,38",
              "cvr":"",
              "ctr":"",
              "state": {
                "whiteList": "true",
                "blackList": "false",
                "suspended": "false"
              }
            }
          ]
        });
    }

    _this.campaignDomains = campaignDomains;


  }
})();
