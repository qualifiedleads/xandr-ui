(function () {
	'use strict';

	angular
		.module('pjtLayout')
		.service('Main', Main);

	/** @ngInject */
	function Main($http, $translateLocalStorage, $window ) {
		var _this = this;

		function statsChart(advertiser_id, from_date, to, by) {
			return $http({
				method: 'GET',
				url: '/api/v1/statistics',
				params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to, by: by}
			})
				.then(function (res) {
					for(var index in res.data.statistics) {
						/*var loc = $translateLocalStorage.get('TRANSLATE_LANG_KEY');*/
						res.data.statistics[index].cvr = +parseFloat(res.data.statistics[index].cvr).toFixed(4);
						res.data.statistics[index].ctr = +parseFloat(res.data.statistics[index].ctr).toFixed(4);
						res.data.statistics[index].cpc = +parseFloat(res.data.statistics[index].cpc).toFixed(4);
						res.data.statistics[index].cpm = +parseFloat(res.data.statistics[index].cpm).toFixed(4);
						res.data.statistics[index].spend = +parseFloat(res.data.statistics[index].spend).toFixed(4);
						res.data.statistics[index].day = $window.moment(res.data.statistics[index].day).format('DD/MM');
					}
					return res.data;
				});
		}

		function statsTotals(advertiser_id, from_date, to) {
			return $http({
				method: 'GET',
				url: '/api/v1/totals',
				params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to}
			})
				.then(function (res) {
          res.data.totals.cvr = +parseFloat(res.data.totals.cvr).toFixed(4);
          res.data.totals.ctr = +parseFloat(res.data.totals.ctr).toFixed(4);
					res.data.totals.cpc = +parseFloat(res.data.totals.cpc).toFixed(4);
					res.data.totals.cpm = +parseFloat(res.data.totals.cpm).toFixed(4);
					res.data.totals.spend = +parseFloat(res.data.totals.spend).toFixed(4);
					return res.data.totals;
				});
		}

		function statsCampaigns(advertiser_id, from_date, to, skip, take,sort,order,stat_by,filters) {
			if(sort){
				if (sort[0].desc === true){
					order = 'desc'
				} else {
					order = 'asc'
				}
				sort = sort[0].selector;
			} else {
				sort = 'campaign';
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
				url: '/api/v1/campaigns',
				params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to,  skip: skip, take: take, sort: sort, order: order, stat_by: stat_by, filter: filters}
			})
				.then(function (res) {
					for(var index in res.data.campaigns) {
						res.data.campaigns[index].cvr = +parseFloat(res.data.campaigns[index].cvr).toFixed(4);
						res.data.campaigns[index].ctr = +parseFloat(res.data.campaigns[index].ctr).toFixed(4);
						res.data.campaigns[index].cpc = +parseFloat(res.data.campaigns[index].cpc).toFixed(4);
						res.data.campaigns[index].cpm = +parseFloat(res.data.campaigns[index].cpm).toFixed(4);
						res.data.campaigns[index].spend = +parseFloat(res.data.campaigns[index].spend).toFixed(4);
					}
					return res.data;
				});
		}

		function statsMap(advertiser_id, from_date, to) {
			return $http({
				method: 'GET',
				url: '/api/v1/map/clicks',
				params: {advertiser_id: advertiser_id, from_date: from_date, to_date: to}
			})
				.then(function (res) {
					return res.data;
				});
		}

		_this.statsCampaigns = statsCampaigns;
		_this.statsTotals = statsTotals;
		_this.statsChart = statsChart;
		_this.statsMap = statsMap;

	}
})();
