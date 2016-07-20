(function () {
	'use strict';

	angular
		.module('pjtLayout')
		.service('AdminService', AdminService);

	/** @ngInject */
	function AdminService($http) {
		var _this = this;

    function appNexusUser() {
      return $http({
        method: 'GET',
        url: '/api/v1/appnexus/user'
      })
        .then(function (res) {
          return res.data;
        });
    }

    function usersList() {

      return $http({
        method: 'GET',
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
        data: user
      })
        .then(function (res) {
          return res.data;

        });
    }

		function usersRemove(id) {
      return $http({
        method: 'DELETE',
        url: '/api/v1/user/' + id
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
