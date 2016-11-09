(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('Auth', Auth);

  /** @ngInject */
  function Auth($http, $cookies, $window) {
    var _this = this;
    var _totalCount = 0;

    function _advertisersList() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/advertisers'
      })
      .then(function (res) {
        return res.data;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.statusText, "error", 4000);
      });
    }

    function selectAdvertisersStore() {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _totalCount;
        },
        load: function () {
          return _advertisersList();
        }
      });
    }

    function authorization(user) {
      return $http({
        method: 'POST',
        url: '/api/v1/login/',
        data: {email: user.email, password: user.password}
      })
      .then(function (res) {
        return res;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.statusText, "error", 4000);
      });
    }

    _this.authorization = authorization;
    _this.selectAdvertisersStore = selectAdvertisersStore;

  }

})();
