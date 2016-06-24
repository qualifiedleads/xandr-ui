(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('Main', Main);

  /** @ngInject */
  function Main($http) {
    var _this = this;

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

    function statsTotals(from, to) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/totals',
        params: {from: from, to: to}
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

    function statsMap(from, to) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/map/clicks',
        params: {from: from, to: to}
      })
        .then(function (res) {
          return res.data;
        });
    }

    _this.statsCampaigns = statsCampaigns;
    _this.statsTotals = statsTotals;
    _this.statsChart = statsChart;
    _this.statsMap = statsMap;

  }
})();
