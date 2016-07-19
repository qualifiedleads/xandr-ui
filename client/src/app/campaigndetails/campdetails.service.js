(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('CampDetails', CampDetails);

  /** @ngInject */
  function CampDetails($http) {
    var _this = this;


    function nameCampaigns(id) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + ''
      })
        .then(function (res) {
          return res.data;
        });
    }

    function campaignDetails(id, from, to, section) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/details',
        params: {from_date: from, to_date: to, section: section}
      })
        .then(function (res) {
          return res.data;
        });
    }

    function statsChart(id, from, to, by) {
      return $http({
        method: 'GET',
        url:'/api/v1/campaigns/' + encodeURI(id) + '/graphinfo',
        params: {from_date: from, to_date: to, by: by}
      })
        .then(function (res) {
          return res.data;
        });
    }


    function campaignDomains(id, from, to, skip, take, order, filter) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        params: {id:id, from_date: from, to_date: to, skip: skip, take: take, order: order, filter:filter}
      })
        .then(function (res) {
          return res.data;
        });
    }

    function bucketsCpa(id, from, to) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/cpabuckets',
        params: {id:id, from_date: from, to_date: to}
      })
        .then(function (/*res*/) {
          //return res.data;
          return [{cpa:1.2, sellerid: 123, sellername: "Rovio", placementid: 234, placementname: "AngryBirds"},
            {cpa:0.4, sellerid: 678, sellername:"Paris", placementid:9789, placementname:"Cat"},
            {cpa:10.1, sellerid: 3453, sellername:"France", placementid:2325, placementname:"Tom"},
            {cpa:4.1, sellerid: 545, sellername: "Lipton", placementid: 111, placementname: "Mouse"},
            {cpa:0.8, sellerid: 35, sellername: "River", placementid: 45, placementname: "Tributary"},
            {cpa:9.3, sellerid: 90, sellername: "Wood", placementid: 3545, placementname: "Land"},
            {cpa:2.4, sellerid: 222, sellername: "Pen", placementid: 333, placementname: "Gear"},
            {cpa:5.4, sellerid: 54, sellername: "World", placementid: 3444454, placementname: "Flower"},
            {cpa:6.1, sellerid: 888, sellername: "Bird", placementid: 999, placementname: "Kitten"},
            {cpa:13.1, sellerid: 444, sellername: "Dreams", placementid: 56656, placementname: "Sweet"},
            {cpa:0.1, sellerid: 787, sellername: "Hotel", placementid: 76876, placementname: "California"},
            {cpa:1.9, sellerid: 678678, sellername: "Star", placementid: 12312, placementname: "Sky"}]
        });
    }

    _this.nameCampaigns = nameCampaigns;
    _this.statsChart = statsChart;
    _this.bucketsCpa = bucketsCpa;
    _this.campaignDetails = campaignDetails;
    _this.campaignDomains = campaignDomains;
  }
})();
