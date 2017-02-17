(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('Main', Main);

  /** @ngInject */
  function Main($http, $window, $cookies) {
    var _this = this;
    var _multipleTotalCount = 0;

    function chartStore (id, dataStart, dataEnd, by) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },
        load: function () {
          return _statsChart(id, dataStart, dataEnd, by)
          .then(function (result) {
            return result.statistics;
          });
        }
      });
    }

    function _statsChart(advertiser_id, from_date, to, by) {
      return $http({
        method: 'GET',
        url: '/api/v1/statistics',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to, by: by}
      })
      .then(function (res) {
        for (var index in res.data.statistics) {
          res.data.statistics[index].cvr = +parseFloat(res.data.statistics[index].cvr).toFixed(4);
          res.data.statistics[index].ctr = +parseFloat(res.data.statistics[index].ctr).toFixed(4);
          res.data.statistics[index].cpc = +parseFloat(res.data.statistics[index].cpc).toFixed(2);
          res.data.statistics[index].cpm = +parseFloat(res.data.statistics[index].cpm).toFixed(4);
          res.data.statistics[index].spend = +parseFloat(res.data.statistics[index].spend).toFixed(2);
          res.data.statistics[index].day = $window.moment(res.data.statistics[index].day).format('DD/MM');
        }
        return res.data;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      });
    }

    function statsTotals(advertiser_id, from_date, to) {
      return $http({
        method: 'GET',
        url: '/api/v1/totals',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to}
      })
      .then(function (res) {
        res.data.totals.cvr = +parseFloat(res.data.totals.cvr).toFixed(4);
        res.data.totals.ctr = +parseFloat(res.data.totals.ctr).toFixed(4);
        res.data.totals.cpc = +parseFloat(res.data.totals.cpc).toFixed(2);
        res.data.totals.cpm = +parseFloat(res.data.totals.cpm).toFixed(2);
        res.data.totals.spend = +parseFloat(res.data.totals.spend).toFixed(2);
        return res.data.totals;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      });
    }

    function multipleStore(id, dataStart, dataEnd, by) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _multipleTotalCount;
        },
        load: function (loadOptions) {
          if (loadOptions.searchOperation && loadOptions.dataField){
            loadOptions.take = 999999;
          }
          return _statsCampaigns(id, dataStart, dataEnd, loadOptions.skip,
              loadOptions.take, loadOptions.sort, loadOptions.order,
              by, loadOptions.filter)
          .then(function (result) {
            _multipleTotalCount = result.totalCount;
            return result.campaigns;
          });
        }
      });
    }

    function _statsCampaigns(advertiser_id, from_date, to, skip, take, sort, order, stat_by, filters) {
      if (sort) {
        if (sort[0].desc === true) {
          order = 'desc'
        } else {
          order = 'asc'
        }
        sort = sort[0].selector;
      } else {
        sort = 'campaign';
        order = 'DESC';
      }
      if (take == null) {
        take = 20;
      }
      if (skip == null) {
        skip = 0;
      }

      return $http({
        method: 'GET',
        url: '/api/v1/campaigns',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          advertiser_id: advertiser_id,
          from_date: from_date,
          to_date: to,
          skip: skip,
          take: take,
          sort: sort,
          order: order,
          stat_by: stat_by,
          filter: filters
        }
      })
      .then(function (res) {
        for (var index in res.data.campaigns) {
          for (var indexJ in res.data.campaigns[index].chart) {
            res.data.campaigns[index].chart[indexJ].conv = +parseFloat(res.data.campaigns[index].chart[indexJ].conv).toFixed(4);
            res.data.campaigns[index].chart[indexJ].cpc = +parseFloat(res.data.campaigns[index].chart[indexJ].cpc).toFixed(2);
            res.data.campaigns[index].chart[indexJ].ctr = +parseFloat(res.data.campaigns[index].chart[indexJ].ctr.toFixed(4));
            res.data.campaigns[index].chart[indexJ].cvr = +parseFloat(res.data.campaigns[index].chart[indexJ].cvr).toFixed(4);
            res.data.campaigns[index].chart[indexJ].spend = +parseFloat(res.data.campaigns[index].chart[indexJ].spend).toFixed(2);
          }
          res.data.campaigns[index].cvr = +parseFloat(res.data.campaigns[index].cvr).toFixed(2)/100;
          res.data.campaigns[index].ctr = +parseFloat(res.data.campaigns[index].ctr).toFixed(2)/100;
          res.data.campaigns[index].cpc = +parseFloat(res.data.campaigns[index].cpc).toFixed(4);
          res.data.campaigns[index].cpm = +parseFloat(res.data.campaigns[index].cpm).toFixed(4);
          res.data.campaigns[index].spend = +parseFloat(res.data.campaigns[index].spend).toFixed(4);
          res.data.campaigns[index].imps_viewed = +parseFloat(res.data.campaigns[index].imps_viewed).toFixed(4);
          res.data.campaigns[index].view_measured_imps = +parseFloat(res.data.campaigns[index].view_measured_imps).toFixed(4);
          res.data.campaigns[index].view_measurement_rate = +parseFloat(res.data.campaigns[index].view_measurement_rate).toFixed(1)/100;
          res.data.campaigns[index].view_rate = +parseFloat(res.data.campaigns[index].view_rate).toFixed(1)/100;
        }
        return res.data;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      });
    }

    function statsMap(advertiser_id, from_date, to) {
      return $http({
        method: 'GET',
        url: '/api/v1/map/clicks',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to}
      })
      .then(function (res) {
        return res.data;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      });
    }

    function updateCampaign(advertiserId) {
      return $http({
        method: 'GET',
        url: '/api/v1/advertiser/' + advertiserId + '/update',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
      })
      .then(function (res) {
        return res.status;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, 'error', 4000);
      });
    }

    _this.updateCampaign = updateCampaign;
    _this.multipleStore = multipleStore;
    _this.chartStore = chartStore;
    _this.statsTotals = statsTotals;
    _this.statsMap = statsMap;

  }
})();
