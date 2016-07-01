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
        url: 'api/v1/campaigns'
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

  

    _this.nameCampaigns = nameCampaigns;
    _this.statsCampaigns = statsCampaigns;
    _this.statsChart = statsChart;
    // _this.statsMap = statsMap;

  }
})();
