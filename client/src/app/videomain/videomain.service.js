(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('VideoMain', VideoMain);

  /** @ngInject */
  function VideoMain($http, $window, $cookies) {
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
            return result;
          });
        }
      });
    }

    function _statsChart(advertiser_id, from_date, to, by) {
      return $http({
        method: 'GET',
        url: '/api/v1/videostatistics',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to, by: by}
      })
      .then(function (res) {
        return [
          {"fill_rate":1,"profit_loss":5,"spend":100.115817,"imp":89901,"ad_starts":4,"day":"2016-06-21"},
          {"fill_rate":5,"profit_loss":4,"spend":37.901687,"imp":62183,"ad_starts":5,"day":"2016-06-22"},
          {"fill_rate":4,"profit_loss":3,"spend":0.112469,"imp":206,"ad_starts":6,"day":"2016-06-23"},
          {"fill_rate":8,"profit_loss":5,"spend":100.115817,"imp":89901,"ad_starts":7,"day":"2016-06-24"},
          {"fill_rate":4,"profit_loss":7,"spend":37.901687,"imp":62183,"ad_starts":9,"day":"2016-06-25"},
          {"fill_rate":8,"profit_loss":6,"spend":0.112469,"imp":206,"ad_starts":4,"day":"2016-06-26"},
          {"fill_rate":9,"profit_loss":9,"spend":100.115817,"imp":89901,"ad_starts":1,"day":"2016-06-27"},
          {"fill_rate":8,"profit_loss":4,"spend":37.901687,"imp":62183,"ad_starts":0,"day":"2016-06-28"},
          {"fill_rate":7,"profit_loss":1,"spend":0.112469,"imp":206,"ad_starts":1,"day":"2016-06-29"},
          ];
        return res.data;
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
              by, loadOptions.filter, loadOptions.totalSummary)
          .then(function (result) {
            _multipleTotalCount = result.total_count;
            return result.campaigns;
          });
        }
      });
    }

    function _statsCampaigns(advertiser_id, from_date, to, skip, take, sort, order, stat_by, filters, totalSummary) {
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
        url: '/api/v1/videocampaigns',
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
          filter: filters,
          totalSummary: totalSummary
        }
      })
      .then(function (res) {

        _this.totalSummary = {
          "campaign": res.data.total_count || 0,
          "ad_starts": res.data.total_ad_starts,
          "cpm": res.data.total_cpm,
          "fill_rate": res.data.total_fill_rate,
          "fill_rate_hour": res.data.total_fill_rate_hour,
          "profit_loss": res.data.total_profit_loss,
          "profit_loss_hour": res.data.total_profit_loss_hour,
          "spent": res.data.total_spent,
          "sum_imps": res.data.total_sum_imps
        };

        for(var i=0; i < res.data.campaigns.length; i++) {
          res.data.campaigns[i].chart = [
          {"fill_rate":1,"profit_loss":5,"spend":100.115817,"imp":89901,"ad_starts":4,"day":"2016-06-21"},
          {"fill_rate":5,"profit_loss":4,"spend":37.901687,"imp":62183,"ad_starts":5,"day":"2016-06-22"},
          {"fill_rate":4,"profit_loss":3,"spend":0.112469,"imp":206,"ad_starts":6,"day":"2016-06-23"},
          {"fill_rate":8,"profit_loss":5,"spend":100.115817,"imp":89901,"ad_starts":7,"day":"2016-06-24"},
          {"fill_rate":4,"profit_loss":7,"spend":37.901687,"imp":62183,"ad_starts":9,"day":"2016-06-25"},
          {"fill_rate":8,"profit_loss":6,"spend":0.112469,"imp":206,"ad_starts":4,"day":"2016-06-26"},
          {"fill_rate":9,"profit_loss":9,"spend":100.115817,"imp":89901,"ad_starts":1,"day":"2016-06-27"},
          {"fill_rate":8,"profit_loss":4,"spend":37.901687,"imp":62183,"ad_starts":0,"day":"2016-06-28"},
          {"fill_rate":7,"profit_loss":1,"spend":0.112469,"imp":206,"ad_starts":1,"day":"2016-06-29"},
          ];
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
        url: '/api/v1/map/imps',
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

    _this.multipleStore = multipleStore;
    _this.chartStore = chartStore;
    _this.statsMap = statsMap;

  }
})();
