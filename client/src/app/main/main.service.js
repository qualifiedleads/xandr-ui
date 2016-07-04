(function () {
	'use strict';

	angular
		.module('pjtLayout')
		.service('Main', Main);

	/** @ngInject */
	function Main($http, $translateLocalStorage) {
		var _this = this;

		function statsChart(advertiser_id, from_date, to, by) {
			return $http({
				method: 'GET',
				url: '/api/v1/statistics',
				params: {/*advertiser_id: advertiser_id,*/ from_date: from_date, to: to, by: by}
			})
				.then(function (res) {
					for(var index in res.data.statistics) {
						var loc = $translateLocalStorage.get('TRANSLATE_LANG_KEY');
						res.data.statistics[index].cpc = parseFloat(res.data.statistics[index].cpc).toFixed(4);
						res.data.statistics[index].cpm = parseFloat(res.data.statistics[index].cpm).toFixed(4);
						res.data.statistics[index].spend = parseFloat(res.data.statistics[index].spend).toFixed(4);
						res.data.statistics[index].day = moment(res.data.statistics[index].day).locale(loc).format('L');
					 }
					return res.data;
				});
		}

		function statsTotals(advertiser_id, from_date, to) {
			return $http({
				method: 'GET',
				url: '/api/v1/totals',
				params: {/*advertiser_id: advertiser_id,*/ from_date: from_date, to: to}
			})
				.then(function (res) {

						res.data.totals.cpc = parseFloat(res.data.totals.cpc).toFixed(4);
						res.data.totals.cpm = parseFloat(res.data.totals.cpm).toFixed(4);
						res.data.totals.spend = parseFloat(res.data.totals.spend).toFixed(4);

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
			/*var rowFilter = '';
			if(filters) {
				if (Array.isArray(filters[0])) {
					for (var i = 0; i < filters.length; i += 2) {
						var filter = filters[i];
						if (Array.isArray(filter[0])) {
							if (i > 0) rowFilter += ';';
							for(var j = 0; j < filter.length; j += 2) {
								var nestedFilters = filter[j];
								if (j === 0)
									rowFilter += nestedFilters[0] + '=';
								rowFilter += nestedFilters[2];
								if (j+2 < filter.length)
									rowFilter += ',';
							}
						} else {
							if (i > 0)
								if (Array.isArray(filters[i-2][0])) rowFilter += ';' + filter[0] + '=';
							if (i === 0)
								rowFilter += filter[0] + '=';
							rowFilter += filter[2];
							if (i+2 < filters.length)
								rowFilter += ',';
						}
					}
				} else {
					rowFilter += filters[0] + '=' + filters[2];
				}
			}*/

			if(take == null) {
				take = 20;
			}
			if(skip == null) {
				skip = 0;
			}

			return $http({
				method: 'GET',
				url: '/api/v1/campaigns',
				params: {/*advertiser_id: advertiser_id, */from_date: from_date, to: to,  skip: skip, take: take, sort: sort, order: order, stat_by: stat_by, filter: filters}
			})
				.then(function (res) {
					for(var index in res.data.campaigns) {
						res.data.campaigns[index].cpc = parseFloat(res.data.campaigns[index].cpc).toFixed(4);
						res.data.campaigns[index].cpm = parseFloat(res.data.campaigns[index].cpm).toFixed(4);
						res.data.campaigns[index].spend = parseFloat(res.data.campaigns[index].spend).toFixed(4);
					}
					return res.data;
				});
		}

		function statsMap(advertiser_id, from_date, to) {
			return $http({
				method: 'GET',
				url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/map/clicks',
				params: {advertiser_id: advertiser_id, from_date: from_date, to: to}
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
