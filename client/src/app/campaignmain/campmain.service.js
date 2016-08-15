(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('CampMain', CampMain);

  /** @ngInject */
  function CampMain($http, $window, $cookies) {
    var _this = this;
    _this.totalCount = 0;

    function nameCampaigns(id) {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
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
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
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
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        params: {from_date: from, to_date: to}
      })
      .then(function (res) {
        for (var index in res.data) {
          res.data[index].avg = +parseFloat(res.data[index].avg).toFixed(4);
          res.data[index].ctr = +parseFloat(res.data[index].ctr).toFixed(4);
          res.data[index].close = +parseFloat(res.data[index].close).toFixed(4);
          res.data[index].high = +parseFloat(res.data[index].high).toFixed(4);
          res.data[index].low = +parseFloat(res.data[index].low).toFixed(4);
          res.data[index].open = +parseFloat(res.data[index].open).toFixed(4);
          res.data[index].day = $window.moment(res.data[index].date).toDate();
        }
        return res.data;
      })
      .catch(function (err) {
        return err;
      });
    }


    function campaignDomains(id, from, to, skip, take, sort, order, filter) {
      if (sort) {
        if (sort[0].desc === true) {
          order = 'desc'
        } else {
          order = 'asc'
        }
        sort = sort[0].selector;
      } else {
        sort = 'placement';
        order = 'DESC';
      }
      if (take == null) {
        take = 20;
      }
      if (skip == null) {
        skip = 0;
      }

      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        params: {from_date: from, to_date: to, skip: skip, take: take, sort: sort, order: order, filter: filter}
      })
      .then(function (res) {
        for (var index in res.data.data) {
          res.data.data[index].cvr = +parseFloat(res.data.data[index].cvr).toFixed(4);
          res.data.data[index].ctr = +parseFloat(res.data.data[index].ctr).toFixed(4);
          res.data.data[index].cpc = +parseFloat(res.data.data[index].cpc).toFixed(4) || null;
          res.data.data[index].cpm = +parseFloat(res.data.data[index].cpm).toFixed(4);
          res.data.data[index].imp = +parseFloat(res.data.data[index].imp).toFixed(4);
          res.data.data[index].cpa = +parseFloat(res.data.data[index].cpa).toFixed(4) || null;
          res.data.data[index].clicks = +parseFloat(res.data.data[index].clicks).toFixed(4);
          res.data.data[index].conv = +parseFloat(res.data.data[index].conv).toFixed(4);
          res.data.data[index].cost = +parseFloat(res.data.data[index].cost).toFixed(2);
          res.data.data[index].imps_viewed = +parseFloat(res.data.data[index].imps_viewed).toFixed(4);
          res.data.data[index].view_measured_imps = +parseFloat(res.data.data[index].view_measured_imps).toFixed(4);
          res.data.data[index].view_measurement_rate = +parseFloat(res.data.data[index].view_measurement_rate).toFixed(4);
          res.data.data[index].view_rate = +parseFloat(res.data.data[index].view_rate).toFixed(4);
        }
        return res.data;
      })
      .then(function (result) {
        _this.totalCount = result.totalCount || 0;
        return result.data;
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
