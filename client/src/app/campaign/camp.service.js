(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('Camp', Camp);

  /** @ngInject */
  function Camp($http) {
    var _this = this;


    function nameCampaigns() {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns'
      })
        .then(function (res) {
          return res.data.campaigns;
        });
    }

    function statsChart(from, to, by) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/statistics',
        params: {from: from, to: to, by: by}
      })
        .then(function (res) {
          //return res.data.statistics;
          return [
          { day: "2016-06-27T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: -5, mediaspent: 5, conversions: 40, ctr: 15  },
          { day: "2016-06-28T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 1, mediaspent: 15, conversions: 23, ctr: -10 },
          { day: "2016-06-29T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 2, mediaspent: 5, conversions: 33, ctr: 10 },
          { day: "2016-06-30T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: 6, mediaspent: 55, conversions: 87, ctr: -42 },
          { day: "2016-07-01T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: 9, mediaspent: 44, conversions: -20, ctr: -57 },
          { day: "2016-07-02T00:00:00Z", impression: 10, cpa: 10, cpc: 15, clicks: 8, mediaspent: 77, conversions: 23, ctr: 99 },
          { day: "2016-07-03T00:00:00Z", impression: 30, cpa: 50, cpc: 13, clicks: 23, mediaspent: 66, conversions: -10, ctr: 110 },
          { day: "2016-07-04T00:00:00Z", impression: 40, cpa: 50, cpc: 14, clicks: 12, mediaspent: 11, conversions: 37, ctr: 56 },
          { day: "2016-07-05T00:00:00Z", impression: 50, cpa: 90, cpc: 90, clicks: -10, mediaspent: 99, conversions: 50, ctr: 67 },
          { day: "2016-07-06T00:00:00Z", impression: 40, cpa: 175, cpc: 120, clicks: 31, mediaspent: -11, conversions: 23, ctr: 67 },
          { day: "2016-07-07T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 70, mediaspent: -2, conversions: 58, ctr: -20 },
          { day: "2016-07-08T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 26, mediaspent: 5, conversions: 21, ctr: -10 },
          { day: "2016-07-09T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 52, mediaspent: 76, conversions: 10, ctr: 70 },
          { day: "2016-07-10T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 1, mediaspent: 32, conversions: 49, ctr: 90 },
          { day: "2016-07-11T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 38, mediaspent: 11, conversions: 99, ctr: 10 },
          { day: "2016-07-12T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: -16, mediaspent: 15, conversions: 60, ctr: 58 },
          { day: "2016-07-13T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: -40, mediaspent: 46, conversions: 23, ctr: 78 },
          { day: "2016-07-14T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: 24, mediaspent: 68, conversions: -20, ctr: 80 },
          { day: "2016-07-15T00:00:00Z", impression: 10, cpa: 10, cpc: 15, clicks: 12, mediaspent: 49, conversions: -37, ctr:22 },
          { day: "2016-07-16T00:00:00Z", impression: 30, cpa: 100, cpc: 13, clicks: 83, mediaspent: 36, conversions: -1, ctr: 67 },
          { day: "2016-07-17T00:00:00Z", impression: 40, cpa: 110, cpc: 14, clicks: 41, mediaspent: 28, conversions: 65, ctr: -10 },
          { day: "2016-07-18T00:00:00Z", impression: 50, cpa: 90, cpc: 90, clicks: 27, mediaspent: 95, conversions: 23, ctr: 88 },
          { day: "2016-07-19T00:00:00Z", impression: 40, cpa: 95, cpc: 120, clicks: 83, mediaspent: 92, conversions: 10, ctr: 77 },
          { day: "2016-07-20T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: -20, mediaspent: 15, conversions: 7, ctr: 66 },
          { day: "2016-07-21T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 56, mediaspent: 54, conversions: 34, ctr: -10 },
          { day: "2016-07-22T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 17, mediaspent: 22, conversions: 65, ctr: -40 },
          { day: "2016-07-23T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 22, mediaspent: 77, conversions: 52, ctr: -70 },
          { day: "2016-07-24T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 29, mediaspent: 90, conversions: 23, ctr: -54 },
          { day: "2016-07-25T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 90, mediaspent: 17, conversions: 59, ctr: 28 },
          { day: "2016-07-26T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: 45, mediaspent: 47, conversions: 82, ctr: 65 },
          { day: "2016-07-27T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: -30, mediaspent: 32, conversions: 33, ctr: 58 }
          ];
        });
    }

    function statsCampaigns(from, to, skip, take,sort,order,stat_by,filter) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
        params: {from: from, to: to,  skip: skip, take: take, sort: sort, order: order, stat_by: stat_by, filter: filter}
      })
        .then(function (res) {
          return res.data;
        });
    }

    function cpaBuckets(min, max) {

        var arrayOfCpa = {
          "cnn.com": "34.12",
          "lion.com": "3.76",
          "tiger.com": "7.97",
          "cat.com": "1.23",
          "dog.com": "16.11",
          "mouse.com": "6.53",
          "rabbit.com": "0.91",
          "bear.com": "1.9",
          "snake.com": "3.7",
          "squirrel.com": "4.78",
          "hamster.com": "0.62"
        };
      var a = [];
      for (var i in arrayOfCpa) {
           if ((Number(arrayOfCpa[i])>=Number(min)) && (arrayOfCpa[i]<Number(max))) {
           a.push(i);
        }
      }
  return a;
      }




    _this.nameCampaigns = nameCampaigns;
    _this.statsCampaigns = statsCampaigns;
    _this.statsChart = statsChart;
    _this.cpaBuckets = cpaBuckets;

  }
})();
