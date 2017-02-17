(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('AutomaticCpm', AutomaticCpm);

  /** @ngInject */
  function AutomaticCpm($http, $cookies, $window) {
    var _this = this;

    function getList(id) {
      return $http({
        method: 'GET',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        url: '/api/v1/videocampaigns/' + id + '/mlgraph',
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, 'error', 4000);
        });
    }

    function saveMethod(advertiserId, campaignId, backName) {
      return $http({
        method: 'PUT',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        url: '/api/v1/videocampaigns/' + campaignId + '/mlsetalgo',
        data: {
          advertiserId: advertiserId,
          back_name: backName,
        }
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, 'error', 4000);
          return false;
        });
    }

    _this.getList = getList;
    _this.saveMethod = saveMethod;
  }
})();
