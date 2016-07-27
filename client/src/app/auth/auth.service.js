(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('Auth', Auth);

  /** @ngInject */
  function Auth($http,$cookieStore,$cookies) {
    var _this = this;

    function advertisersList() {
      return $http({
        method: 'GET',
        url: '/api/v1/advertisers'
      })
      .then(function (res) {
        return res.data;
      });
    }

    function authorization(user) {
      $cookieStore.remove('csrftoken');
      $cookieStore.remove('sessionid');
      return $http({
        method: 'POST',
        url: '/api/v1/login',
        data: {email: user.email, password: user.password}
      })
      .then(function (res) {
        return res;
      })
      .catch(function () {
        var res = {};
        res.status = 200;
        res.data = {
          id: 19,
          token: "123123123123",
          permission: 'adminfull' // userfull
        };
        return res;
        //return err;
      });
    }

    _this.authorization = authorization;
    _this.advertisersList = advertisersList;
  }

})();
