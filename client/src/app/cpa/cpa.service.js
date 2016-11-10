(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('CPA', CPA);

  /** @ngInject */
  function CPA($http, $cookies) {
    var _this = this;


    function nameCampaigns(id) {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/campaigns/' + encodeURI(id) + ''
      })
        .then(function (res) {
          return res.data;
        });
    }

    function detailsStoreAll(id, from, to, section) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/details',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        params: {from_date: from, to_date: to, section: section}
      })
        .then(function (res) {

          for (var index in res.data.all) {
            res.data.all[index].data = +parseFloat(res.data.all[index].data).toFixed(4);
          }
          for (var index in res.data.conversions) {
            res.data.conversions[index].data = +parseFloat(res.data.conversions[index].data).toFixed(4);
          }
          return res.data;
        });
    }



    function bucketsCpa(id, from, to, section) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/cpabuckets',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        params: {id:id, from_date: from, to_date: to, category: section}
      })
          .then(function (res) {
            for(var index in res.data) {
              res.data[index].cpa = +parseFloat(res.data[index].cpa).toFixed(3);
                        }
            return res.data;
          });

    }

    _this.nameCampaigns = nameCampaigns;
    _this.bucketsCpa = bucketsCpa;
    _this.detailsStoreAll = detailsStoreAll;
  }
})();
