(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('Rules', Rules);

  /** @ngInject */
  function Rules($http, $cookies, $window) {
    var _this = this;

    function saveRules(id, ruleObj) {
      return $http({
        method: 'POST',
        url: '/api/v1/campaigns/' + id + '/rules',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        data: {ruleObj: ruleObj}
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, "error", 4000);
        });
    }

    function getRules(id) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + id + '/rules',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, "error", 4000);
        });
    }


    _this.saveRules = saveRules;
    _this.getRules = getRules;

  }
})();
