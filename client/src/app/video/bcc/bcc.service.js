(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('BCC', BCC);

  /** @ngInject */
  function BCC($http, $cookies, $window) {
    var _this = this;

    function campaignList(advertiserId) {
      return $http({
        method: 'GET',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        url: '/api/v1/advertiser/campaign/all',
        params: {
          id: advertiserId
        }
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, 'error', 4000);
        });
    }

    function campaignCreateBulk(advertiserId, campaignId, domain) {
      return $http({
        method: 'POST',
        headers: { Authorization: 'Token ' + $cookies.get('token') },
        url: '/api/v1/campaign/create/bulk',
        data: {
          advertiserId: advertiserId,
          campaignId: campaignId,
          domain: domain
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

    _this.campaignList = campaignList;
    _this.campaignCreateBulk = campaignCreateBulk;
  }
})();
