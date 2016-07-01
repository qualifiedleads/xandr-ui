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

		_this.advertisersList = advertisersList;
	}
})();
