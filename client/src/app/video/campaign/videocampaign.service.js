(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('VideoCampMain', VideoCampMain);

  /** @ngInject */
  function VideoCampMain($http, $window, $cookies) {
    var _this = this;
    var _totalCountCampaign = 0;

    function nameCampaigns(id) {
      return $http({
        method: 'GET',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        url: '/api/v1/campaigns/' + encodeURI(id) + ''
      })
      .then(function (res) {
        return res.data;
      })
      .catch(function (err) {
        return err;
      });
    }

    function _graphInfo(id, from, to, by) {
      return $http({
        method: 'GET',
        url: '/api/v1/videocampaigns/' + encodeURI(id) + '/graphinfo',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          from_date: from,
          to_date: to,
          by: by}
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

    function getChartStore(campId, dataStart, dataEnd, by) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },
        load: function () {
          return _graphInfo(campId, dataStart, dataEnd, by);
        }
      });
    }

    _this.nameCampaigns = nameCampaigns;
    _this.getChartStore = getChartStore;
  }
})();
