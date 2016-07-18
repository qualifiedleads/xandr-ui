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
        url: '/api/v1/'
      })
        .then(function (res) {
          //return res.data;
          return  [{
            "id": "1",
            "login":"cnm@gmail.com",
            "name":"CNM"
          },{
            "id": "2",
            "login":"BBC@gmail.com",
            "name":"BBC"
          },{
            "id": "3",
            "login":"Discovery@gmail.com",
            "name":"Discovery"
          },{
            "id": "4",
            "login":"HTB@gmail.com",
            "name":"HTB"
          },{
            "id": "5",
            "login":"ICTV@gmail.com",
            "name":"ICTV"
          }];
        });
    }

    function usersList() {
      return $http({
        method: 'GET',
        url: '/api/v1/'
      })
        .then(function (res) {
          //return res.data;
          return  [{
            "id": "1",
            "email":"cnm@gmail.com",
            "permission":"11111",
            "name":"CNM"
          },{
            "id": "2",
            "email":"BBC@gmail.com",
            "permission":"11111",
            "name":"BBC"
          },{
            "id": "3",
            "email":"Discovery@gmail.com",
            "permission":"11111",
            "name":"Discovery"
          },{
            "id": "4",
            "email":"HTB@gmail.com",
            "permission":"11111",
            "name":"HTB"
          },{
            "id": "5",
            "email":"ICTV@gmail.com",
            "permission":"11111",
            "name":"ICTV"
          }];
        });
    }

		_this.appNexusUser = appNexusUser;
		_this.usersList = usersList;
	}
})();
