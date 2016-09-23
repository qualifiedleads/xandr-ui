(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('CampaignOptimiser', CampaignOptimiser);

  /** @ngInject */
  function CampaignOptimiser($http, $cookies, $window) {
    var _this = this;
    var _totalCountCampaign = 0;

    function getGridCampaignStore(campId, dataStart, dataEnd) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _totalCountCampaign;
        },
        load: function (loadOptions) {
          if (loadOptions.searchOperation && loadOptions.dataField) {
            loadOptions.take = 999999;
          }
          return _campaignDomains(campId, dataStart, dataEnd, loadOptions.skip, loadOptions.take, loadOptions.sort, loadOptions.order, loadOptions.filter, loadOptions.totalSummary);
        }
      });
    }

    function _campaignDomains(id, from, to, skip, take, sort, order, filter, totalSummary) {
      if (sort) {
        if (sort[0].desc === true) {
          order = 'desc'
        } else {
          order = 'asc'
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
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          from_date: from,
          to_date: to,
          skip: skip,
          take: take,
          sort: sort,
          order: order,
          filter: filter,
          totalSummary: totalSummary
        }
      })
      .then(function (res) {
        var i = 0;
        var j  = 1.1;
        var rand = [true, false, null];
        var list = res.data.data.map(function (item) {
          i = i+ 0.1;
          j = j- 0.1;
          return {
            NetworkPublisher: item.NetworkPublisher,
            placement: item.placement,
            placement_name: item.placement_name,
            cvr: parseFloat((item.cvr || 0).toFixed(4)),
            ctr: parseFloat((item.ctr || 0).toFixed(4)),
            cpc: parseFloat((item.cpc || 0).toFixed(4)),
            cpm: parseFloat((item.cpm || 0).toFixed(4)),
            imp: parseFloat((item.imp || 0).toFixed(4)),
            cpa: parseFloat((item.cpa || 0).toFixed(4)),
            clicks: parseFloat((item.clicks || 0).toFixed(4)),
            conv: parseFloat((item.conv || 0).toFixed(4)),
            cost: parseFloat((item.cost || 0).toFixed(2)),
            analitics: {
              "good": i,
              "bad": j,
              "checked": rand[Math.floor(Math.random()*3)]
            },
            imps_viewed: parseFloat((item.imps_viewed || 0).toFixed(4)),
            view_measured_imps: parseFloat((item.view_measured_imps || 0).toFixed(4)),
            view_measurement_rate: parseFloat((item.view_measurement_rate || 0).toFixed(1)),
            view_rate: parseFloat((item.view_rate || 0).toFixed(1)),
            state: {
              blackList: item.state.blackList,
              suspended: item.state.suspended,
              whiteList: item.state.whiteList
            }
          };
        });

        _totalCountCampaign = res.data.totalCount;
        _this.totalSummary = res.data.totalSummary;

        return list;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      });
    }


    function campaignTargeting(id, from, to) {
      return {
        domains: [
          "about.com",
          "celebritytoob.com",
          "lotto.pch.com",
          "verywell.com",
        ],
        geo: [
          "US",
          "UK",
          "NZ"
        ],
        device: [
          "Desktops & Laptops",
          "AND",
          "Web"
        ],
        block: [
          "Phones",
          "Tablets",
          "Mobile web",
          "Apps"
        ]
      };
    }

    function editCampaignDomains(id,placement,activeState, time) {
      return $http({
        method: 'PUT',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          placement: placement,
          activeState: activeState,
          suspendTimes: time
        }
      })
      .then(function (res) {
        return res.data;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      });
    }

    function decisionML(id, placementId, checked) {
      return $http({
        method: 'POST',
        url: '/api/v1/campaigns/' + id + '/placement',
        data: {placementId: placementId, checked: checked}
      })
      .then(function (res) {
        return res;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.statusText, "error", 4000);
      });
    }

    _this.decisionML = decisionML;
    _this.campaignTargeting = campaignTargeting;
    _this.editCampaignDomains = editCampaignDomains;
    _this.getGridCampaignStore = getGridCampaignStore;

  }
})();
