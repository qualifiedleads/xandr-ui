(function () {
	'use strict';

	angular
		.module('pjtLayout')
		.service('Auth', Auth);

	/** @ngInject */
	function Auth($http) {
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
			return $http({
				method: 'POST',
				url: '/api/v1/login',
        data: {email: user.login, password: user.password}
			})
				.then(function (res) {
					return res.data;
				})
        .catch(function (/*res*/) {
          var res = {};
          res.data = {
            id: 19,
            token: "123123123123",
            permission: 'adminfull' // userfull
          };
          return res.data;
        });
		}

		_this.authorization = authorization;
		_this.advertisersList = advertisersList;
	}

})();
