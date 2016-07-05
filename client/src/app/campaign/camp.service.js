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
          return res.data;
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
