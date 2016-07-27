(function () {
	'use strict';

	angular
	.module('pjtLayout')
	.service('CampMain', CampMain);

	/** @ngInject */
	function CampMain($http, $translateLocalStorage, $window) {
		var _this = this;


		function nameCampaigns(id) {
			return $http({
				method: 'GET',
				url: '/api/v1/campaigns/' + encodeURI(id) + ''
			})
			.then(function (res) {
				return res.data;
			})
			.catch(function (err) {
				return err;
			});
		}

		function graphinfo(id, from, to, by) {
			return $http({
				method: 'GET',
				url: '/api/v1/campaigns/' + encodeURI(id) + '/graphinfo',
				params: {from_date: from, to_date: to, by: by}
			})
			.then(function (res) {
				for (var index in res.data) {
					res.data[index].ctr = +parseFloat(res.data[index].ctr).toFixed(4);
					res.data[index].conversions = +parseFloat(res.data[index].conversions).toFixed(4);
					res.data[index].impression = +parseFloat(res.data[index].impression).toFixed(4);
					res.data[index].cpa = +parseFloat(res.data[index].cpa).toFixed(4);
					res.data[index].cpc = +parseFloat(res.data[index].cpc).toFixed(4);
					res.data[index].clicks = +parseFloat(res.data[index].clicks).toFixed(4);
					res.data[index].mediaspent = +parseFloat(res.data[index].mediaspent).toFixed(4);
					res.data[index].day = $window.moment(res.data[index].day).format('DD/MM');
				}
				return res.data;
			})
			.catch(function (err) {
				return err;
			});
		}


		function cpaReport(id, from, to) {
			return $http({
				method: 'GET',
				url: '/api/v1/campaigns/' + encodeURI(id) + '/cpareport',
				params: {from_date: from, to_date: to}
			})
			.then(function (res) {
				for (var index in res.data) {
					res.data[index].day = $window.moment(res.data[index].date).toDate();
				}
				return res.data;
			})
			.catch(function (err) {
				return err;
			});
		}


		function campaignDomains(id, from, to, skip, take, sort, order, filter) {
			if(sort){
				if (sort[0].desc === true){
					order = 'desc'
				} else {
					order = 'asc'
				}
				sort = sort[0].selector;
			} else {
				sort = 'placement';
				order = 'DESC';
			}
			if(take == null) {
				take = 20;
			}
			if(skip == null) {
				skip = 0;
			}

			return $http({
				method: 'GET',
				url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
				params: {from_date: from, to_date: to, skip: skip, take: take, sort: sort, order: order, filter: filter}
			})
			.then(function (res) {
				return res.data;
			})
			.catch(function (err) {
				return err;
			});
		}




		_this.cpaReport = cpaReport;
		_this.nameCampaigns = nameCampaigns;
		_this.graphinfo = graphinfo;
		_this.campaignDomains = campaignDomains

	}
})();
