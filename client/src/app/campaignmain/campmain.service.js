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
        url:'/api/v1/campaigns/' + encodeURI(id) + '/graphinfo',
        params: {from_date: from, to_date: to, by: by}
      })
        .then(function (res) {
          //return res.data;
          res.data = [
            { date: "2016-06-27T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: -5, mediaspent: 5, conversions: 40, ctr: 15  },
            { date: "2016-06-28T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 1, mediaspent: 15, conversions: 23, ctr: -10 },
            { date: "2016-06-29T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 2, mediaspent: 5, conversions: 33, ctr: 10 },
            { date: "2016-06-30T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: 6, mediaspent: 55, conversions: 87, ctr: -42 },
            { date: "2016-07-01T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: 9, mediaspent: 44, conversions: -20, ctr: -57 },
            { date: "2016-07-02T00:00:00Z", impression: 10, cpa: 10, cpc: 15, clicks: 8, mediaspent: 77, conversions: 23, ctr: 99 },
            { date: "2016-07-03T00:00:00Z", impression: 30, cpa: 50, cpc: 13, clicks: 23, mediaspent: 66, conversions: -10, ctr: 110 },
            { date: "2016-07-04T00:00:00Z", impression: 40, cpa: 50, cpc: 14, clicks: 12, mediaspent: 11, conversions: 37, ctr: 56 },
            { date: "2016-07-05T00:00:00Z", impression: 50, cpa: 90, cpc: 90, clicks: -10, mediaspent: 99, conversions: 50, ctr: 67 },
            { date: "2016-07-06T00:00:00Z", impression: 40, cpa: 175, cpc: 120, clicks: 31, mediaspent: -11, conversions: 23, ctr: 67 },
            { date: "2016-07-07T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 70, mediaspent: -2, conversions: 58, ctr: -20 },
            { date: "2016-07-08T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 26, mediaspent: 5, conversions: 21, ctr: -10 },
            { date: "2016-07-09T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 52, mediaspent: 76, conversions: 10, ctr: 70 },
            { date: "2016-07-10T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 1, mediaspent: 32, conversions: 49, ctr: 90 },
            { date: "2016-07-11T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 38, mediaspent: 11, conversions: 99, ctr: 10 },
            { date: "2016-07-12T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: -16, mediaspent: 15, conversions: 60, ctr: 58 },
            { date: "2016-07-13T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: -40, mediaspent: 46, conversions: 23, ctr: 78 },
            { date: "2016-07-14T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: 24, mediaspent: 68, conversions: -20, ctr: 80 },
            { date: "2016-07-15T00:00:00Z", impression: 10, cpa: 10, cpc: 15, clicks: 12, mediaspent: 49, conversions: -37, ctr:22 },
            { date: "2016-07-16T00:00:00Z", impression: 30, cpa: 100, cpc: 13, clicks: 83, mediaspent: 36, conversions: -1, ctr: 67 },
            { date: "2016-07-17T00:00:00Z", impression: 40, cpa: 110, cpc: 14, clicks: 41, mediaspent: 28, conversions: 65, ctr: -10 },
            { date: "2016-07-18T00:00:00Z", impression: 50, cpa: 90, cpc: 90, clicks: 27, mediaspent: 95, conversions: 23, ctr: 88 },
            { date: "2016-07-19T00:00:00Z", impression: 40, cpa: 95, cpc: 120, clicks: 83, mediaspent: 92, conversions: 10, ctr: 77 },
            { date: "2016-07-20T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: -20, mediaspent: 15, conversions: 7, ctr: 66 },
            { date: "2016-07-21T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 56, mediaspent: 54, conversions: 34, ctr: -10 },
            { date: "2016-07-22T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 17, mediaspent: 22, conversions: 65, ctr: -40 },
            { date: "2016-07-23T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 22, mediaspent: 77, conversions: 52, ctr: -70 },
            { date: "2016-07-24T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 29, mediaspent: 90, conversions: 23, ctr: -54 },
            { date: "2016-07-25T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 90, mediaspent: 17, conversions: 59, ctr: 28 },
            { date: "2016-07-26T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: 45, mediaspent: 47, conversions: 82, ctr: 65 },
            { date: "2016-07-27T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: -30, mediaspent: 32, conversions: 33, ctr: 58 }
          ];

          var loc = $translateLocalStorage.get('TRANSLATE_LANG_KEY');
          for(var index in res.data) {
            res.data[index].ctr = +parseFloat(res.data[index].ctr).toFixed(4);
            res.data[index].conversions = +parseFloat(res.data[index].conversions).toFixed(4);
            res.data[index].impression = +parseFloat(res.data[index].impression).toFixed(4);
            res.data[index].cpa = +parseFloat(res.data[index].cpa).toFixed(4);
            res.data[index].cpc = +parseFloat(res.data[index].cpc).toFixed(4);
            res.data[index].clicks = +parseFloat(res.data[index].clicks).toFixed(4);
            res.data[index].mediaspent = +parseFloat(res.data[index].mediaspent).toFixed(4);
            res.data[index].date = $window.moment(res.data[index].date).locale(loc).format('L');
          }
          return res.data;


        });
    }



    function cpaReport(id, from, to) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/cpareport',
        params: {id:id, from_date: from, to_date: to}
      })
        .then(function (res) {
          return res.data;
/*
          return [{ date: new Date(1994, 2, 1), low: 24.00, high: 25.00, open: 25.00, close: 24.875, avg: 24.5 },
            { date: new Date(1994, 2, 2), low: 23.625, high: 25.125, open: 24.00, close: 24.875, avg: 24.375 },
            { date: new Date(1994, 2, 3), low: 26.25, high: 28.25, open: 26.75, close: 27.00, avg: 27.25 },
            { date: new Date(1994, 2, 4), low: 26.50, high: 27.875, open: 26.875, close: 27.25, avg: 27.1875 },
            { date: new Date(1994, 2, 7), low: 26.375, high: 27.50, open: 27.375, close: 26.75, avg: 26.9375 },
            { date: new Date(1994, 2, 8), low: 25.75, high: 26.875, open: 26.75, close: 26.00, avg: 26.3125 },
            { date: new Date(1994, 2, 9), low: 25.75, high: 26.75, open: 26.125, close: 26.25, avg: 25.9375 },
            { date: new Date(1994, 2, 10), low: 25.75, high: 26.375, open: 26.375, close: 25.875, avg: 26.0625 },
            { date: new Date(1994, 2, 11), low: 24.875, high: 26.125, open: 26.00, close: 25.375, avg: 25.5 },
            { date: new Date(1994, 2, 14), low: 25.125, high: 26.00, open: 25.625, close: 25.75, avg: 25.5625 },
            { date: new Date(1994, 2, 15), low: 25.875, high: 26.625, open: 26.125, close: 26.375, avg: 26.25 }];*/
        })
        .catch(function () {
          return [{ date: new Date(1994, 2, 1), low: 24.00, high: 25.00, open: 25.00, close: 24.875, avg: 24.5 },
            { date: new Date(1994, 2, 2), low: 23.625, high: 25.125, open: 24.00, close: 24.875, avg: 24.375 },
            { date: new Date(1994, 2, 3), low: 26.25, high: 28.25, open: 26.75, close: 27.00, avg: 27.25 },
            { date: new Date(1994, 2, 4), low: 26.50, high: 27.875, open: 26.875, close: 27.25, avg: 27.1875 },
            { date: new Date(1994, 2, 7), low: 26.375, high: 27.50, open: 27.375, close: 26.75, avg: 26.9375 },
            { date: new Date(1994, 2, 8), low: 25.75, high: 26.875, open: 26.75, close: 26.00, avg: 26.3125 },
            { date: new Date(1994, 2, 9), low: 25.75, high: 26.75, open: 26.125, close: 26.25, avg: 25.9375 },
            { date: new Date(1994, 2, 10), low: 25.75, high: 26.375, open: 26.375, close: 25.875, avg: 26.0625 },
            { date: new Date(1994, 2, 11), low: 24.875, high: 26.125, open: 26.00, close: 25.375, avg: 25.5 },
            { date: new Date(1994, 2, 14), low: 25.125, high: 26.00, open: 25.625, close: 25.75, avg: 25.5625 },
            { date: new Date(1994, 2, 15), low: 25.875, high: 26.625, open: 26.125, close: 26.375, avg: 26.25 }];
        });
    }


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


    function statsCampaigns(from, to, skip, take,sort,order,stat_by,filter) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
        params: {from_date: from, to_date: to,  skip: skip, take: take, sort: sort, order: order, stat_by: stat_by, filter: filter}
      })
        .then(function (res) {
          return res.data;
        });
    }
    //
    // function cpaBuckets(min, max) {
    //
    //   var arrayOfCpa = {
    //     "cnn.com": "34.12",
    //     "lion.com": "3.76",
    //     "tiger.com": "7.97",
    //     "cat.com": "1.23",
    //     "dog.com": "16.11",
    //     "mouse.com": "6.53",
    //     "rabbit.com": "0.91",
    //     "bear.com": "1.9",
    //     "snake.com": "3.7",
    //     "squirrel.com": "4.78",
    //     "hamster.com": "0.62"
    //   };
    //   var a = [];
    //   for (var i in arrayOfCpa) {
    //     if ((Number(arrayOfCpa[i])>=Number(min)) && (arrayOfCpa[i]<Number(max))) {
    //       a.push(i);
    //     }
    //   }
    //   return a;
    // }



    _this.cpaReport = cpaReport;
    _this.nameCampaigns = nameCampaigns;
    _this.statsCampaigns = statsCampaigns;
    _this.statsChart = statsChart;

    _this.campaignDetails = campaignDetails;
    _this.campaignDomains = campaignDomains

  }
})();
