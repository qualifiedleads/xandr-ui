(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('BCC', BCC);

  /** @ngInject */
  function BCC($http, $cookies, $window) {
    var _this = this;
    var _totalCount = 0;

    function _campaignList() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/campaign'
      })
      .then(function (res) {
        return res.data;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.statusText, "error", 4000);
      });
    }

    function selectCampaignStore() {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _totalCount
        },
        load: function () {
          return _campaignList()
        }
      });
    }

    _this.selectCampaignStore = selectCampaignStore;
  }
})();
