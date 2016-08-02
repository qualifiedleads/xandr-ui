(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('AdminService', AdminService);

  /** @ngInject */
  function AdminService($http, $cookies) {
    var _this = this;

    function appNexusUser() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/appnexus/user'
      })
      .then(function (res) {
        return res.data;
      });
    }

    function usersList() {

      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/user/'
      })
      .then(function (res) {
        return res.data;

      });
    }

    function addUser(user) {
      return $http({
        method: 'POST',
        url: '/api/v1/user/',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        data: user
      })
      .then(function (res) {
        return res.data;

      });
    }

    function usersRemove(id) {

      return $http({
        method: 'DELETE',
        url: '/api/v1/user/' + id,
        headers: { 'Authorization': 'Token ' + $cookies.get('token') }
      })
      .then(function (response) {
        return response.data;
      })
      .catch(function () {
        //ErrorMessages.process(response);
        return [];
      });
    }

    _this.usersRemove = usersRemove;
    _this.addUser = addUser;
    _this.appNexusUser = appNexusUser;
    _this.usersList = usersList;
  }
})();
