(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('CampMain', CampMain);

  /** @ngInject */
  function CampMain($http, $window, $cookies) {
    var _this = this;
    var _totalCountCampaign = 0;

    function nameCampaigns(id) {
      return $http({
        method: 'GET',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        url: '/api/v1/campaigns/' + encodeURI(id) + ''
      })
      .then(function (res) {
        return res.data;
      })
      .catch(function (err) {
        return err;
      });
    }

    function _graphInfo(id, from, to, by, type) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/graphinfo',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        params: {
          from_date: from,
          to_date: to,
          by: by,
          type: type
        }
      })
      .then(function (res) {
        for (var index in res.data) {
          res.data[index].ctr = +parseFloat(res.data[index].ctr).toFixed(4);
          res.data[index].conversions = +parseFloat(res.data[index].conversions).toFixed(4);
          res.data[index].impression = +parseFloat(res.data[index].impression).toFixed(4);
          res.data[index].cpa = +parseFloat(res.data[index].cpa).toFixed(4);
          res.data[index].cpc = +parseFloat(res.data[index].cpc).toFixed(4);
          res.data[index].clicks = +parseFloat(res.data[index].clicks).toFixed(4);
          res.data[index].cost = +parseFloat(res.data[index].mediaspent).toFixed(4);
          res.data[index].day = $window.moment(res.data[index].day).format('DD/MM');
        }

        return res.data;
      })
      .catch(function (err) {
        return err;
      });
    }

    function _cpaReport(id, from, to, type) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/cpareport',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        params: {
          from_date: from,
          to_date: to,
          type: type
        }
      })
      .then(function (res) {
        for (var index in res.data) {
          res.data[index].avg = +parseFloat(res.data[index].avg).toFixed(4);
          res.data[index].ctr = +parseFloat(res.data[index].ctr).toFixed(4);
          res.data[index].close = +parseFloat(res.data[index].close).toFixed(4);
          res.data[index].high = +parseFloat(res.data[index].high).toFixed(4);
          res.data[index].low = +parseFloat(res.data[index].low).toFixed(4);
          res.data[index].open = +parseFloat(res.data[index].open).toFixed(4);
          res.data[index].day = $window.moment().locale('en').isoWeekday(res.data[index].date).format('ddd');
        }

        return res.data;
      })
      .catch(function (err) {
        return err;
      });
    }

    function _campaignDomains(id, from, to, skip, take, sort, order, filter, totalSummary, type) {
      if (sort) {
        if (sort[0].desc === true) {
          order = 'desc';
        } else {
          order = 'asc';
        }

        sort = sort[0].selector;
      } else {
        sort = 'placement';
        order = 'DESC';
      }

      if (take == null) {
        take = 10;
      }

      if (skip == null) {
        skip = 0;
      }

      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        params: {
          from_date: from,
          to_date: to,
          skip: skip,
          take: take,
          sort: sort,
          order: order,
          filter: filter,
          totalSummary: totalSummary,
          type: type
        }
      })
      .then(function (res) {
        var list = res.data.data.map(function (item) {
          return {
            NetworkPublisher: item.NetworkPublisher,
            placement: item.placement,
            placement_name: item.placement_name,
            placement__rtbimpressiontrackerplacementdomain__domain: item.placement__rtbimpressiontrackerplacementdomain__domain,
            cvr: parseFloat((item.cvr || 0).toFixed(2) / 100),
            ctr: parseFloat((item.ctr || 0).toFixed(2) / 100),
            cpc: parseFloat((item.cpc || 0).toFixed(4)),
            cpm: parseFloat((item.cpm || 0).toFixed(4)),
            imp: parseFloat((item.imp || 0).toFixed(4)),
            cpa: parseFloat((item.cpa || 0).toFixed(4)),
            clicks: parseFloat((item.clicks || 0).toFixed(4)),
            conv: parseFloat((item.conv || 0).toFixed(4)),
            cost: parseFloat((item.cost || 0).toFixed(2)),
            imps_viewed: parseFloat((item.imps_viewed || 0).toFixed(4)),
            view_measured_imps: parseFloat((item.view_measured_imps || 0).toFixed(4)),
            view_measurement_rate: parseFloat((item.view_measurement_rate || 0).toFixed(1) / 100),
            view_rate: parseFloat((item.view_rate || 0).toFixed(1) / 100),
            state: {
              blackList: item.state & 2,
              suspended: item.state & 1,
              whiteList: item.state & 4
            }
          };
        });

        _totalCountCampaign = res.data.totalCount?res.data.totalCount:null;
        _this.totalSummary = res.data.totalSummary?res.data.totalSummary: null;

        return list;
      })
      .catch(function (err) {
        return err;
      });
    }

    function editCampaignDomains(id, placement, activeState, time) {
      return $http({
        method: 'POST',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/changestate',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        data: {
          placement: placement,
          activeState: activeState,
          suspendTimes: time
        }
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, 'error', 4000);
        });
    }

    function getChartStore(campId, dataStart, dataEnd, by, type) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },

        load: function () {
          return _graphInfo(campId, dataStart, dataEnd, by, type);
        }
      });
    }

    function getBoxPlotStore(campId, dataStart, dataEnd, type) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },

        load: function () {
          return _cpaReport(campId, dataStart, dataEnd, type);
        }
      });
    }

    function getGridCampaignStore(campId, dataStart, dataEnd, type) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _totalCountCampaign;
        },

        load: function (loadOptions) {
          if (loadOptions.searchOperation && loadOptions.dataField) {
            loadOptions.take = 999999;
          }

          return _campaignDomains(campId, dataStart, dataEnd, loadOptions.skip, loadOptions.take, loadOptions.sort, loadOptions.order, loadOptions.filter, loadOptions.totalSummary, type);
        }
      });
    }

    _this.nameCampaigns = nameCampaigns;
    _this.editCampaignDomains = editCampaignDomains;

    _this.getChartStore = getChartStore;
    _this.getGridCampaignStore = getGridCampaignStore;
    _this.getBoxPlotStore = getBoxPlotStore;
  }
})();
