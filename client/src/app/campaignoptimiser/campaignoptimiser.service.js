(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('CampaignOptimiser', CampaignOptimiser);

  /** @ngInject */
  function CampaignOptimiser($http, $cookies) {
    var _this = this;

    function campaignDomains(id, from, to, skip, take, order, filter) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        params: {id:id, from_date: from, to_date: to, skip: skip, take: take, order: order, filter:filter}
      })
        .then(function (res) {
          return res.data;

        }).catch(function (err) {
          return err;
        });
    }

    _this.campaignDomains = campaignDomains;


  }
})();
