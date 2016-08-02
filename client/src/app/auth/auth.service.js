(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('Auth', Auth);

  /** @ngInject */
  function Auth($http, $cookies) {
    var _this = this;

    function advertisersList() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/advertisers'
      })
      .then(function (res) {
        return res.data;
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
        return err;
      });
    }

    _this.authorization = authorization;
    _this.advertisersList = advertisersList;
  }

})();
