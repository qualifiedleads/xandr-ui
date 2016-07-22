(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('CampMain', CampMain);

  /** @ngInject */
  function CampMain($http, $translateLocalStorage, $window) {
    var _this = this;


    function nameCampaigns(id) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + ''
      })
      .then(function (res) {
        return res.data;
      });
    }

    function campaignDetails(id, from, to, section) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/details',
        params: {from_date: from, to_date: to, section: section}
      })
      .then(function (res) {
        return res.data;
      });
    }

    function statsChart(id, from, to, by) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/graphinfo',
        params: {from_date: from, to_date: to, by: by}
      })
      .then(function (res) {
        var loc = $translateLocalStorage.get('TRANSLATE_LANG_KEY');
        for (var index in res.data) {
          res.data[index].ctr = +parseFloat(res.data[index].ctr).toFixed(4);
          res.data[index].conversions = +parseFloat(res.data[index].conversions).toFixed(4);
          res.data[index].impression = +parseFloat(res.data[index].impression).toFixed(4);
          res.data[index].cpa = +parseFloat(res.data[index].cpa).toFixed(4);
          res.data[index].cpc = +parseFloat(res.data[index].cpc).toFixed(4);
          res.data[index].clicks = +parseFloat(res.data[index].clicks).toFixed(4);
          res.data[index].mediaspent = +parseFloat(res.data[index].mediaspent).toFixed(4);
          res.data[index].day = $window.moment(res.data[index].day).locale(loc).format('L');
        }
        return res.data;
      });
    }


    function cpaReport(id, from, to) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/cpareport',
        params: {id: id, from_date: from, to_date: to}
      })
      .then(function (res) {
        return res.data;
      });
    }


    function campaignDomains(id, from, to, skip, take, order, filter) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        params: {id: id, from_date: from, to_date: to, skip: skip, take: take, order: order, filter: filter}
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




    _this.cpaReport = cpaReport;
    _this.nameCampaigns = nameCampaigns;
    _this.statsChart = statsChart;

    _this.campaignDetails = campaignDetails;
    _this.campaignDomains = campaignDomains

  }
})();
