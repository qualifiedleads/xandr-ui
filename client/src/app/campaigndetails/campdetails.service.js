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



    // function cpaReport(id, from, to) {
    //   return $http({
    //     method: 'GET',
    //     url: '/api/v1/campaigns/' + encodeURI(id) + '/cpareport',
    //     params: {id:id, from_date: from, to_date: to}
    //   })
    //     .then(function () {
    //       //return res.data;
    //       return [{ date: new Date(1994, 2, 1), low: 24.00, high: 25.00, open: 25.00, close: 24.875, avg: 24.5 },
    //         { date: new Date(1994, 2, 2), low: 23.625, high: 25.125, open: 24.00, close: 24.875, avg: 24.375 },
    //         { date: new Date(1994, 2, 3), low: 26.25, high: 28.25, open: 26.75, close: 27.00, avg: 27.25 },
    //         { date: new Date(1994, 2, 4), low: 26.50, high: 27.875, open: 26.875, close: 27.25, avg: 27.1875 },
    //         { date: new Date(1994, 2, 7), low: 26.375, high: 27.50, open: 27.375, close: 26.75, avg: 26.9375 },
    //         { date: new Date(1994, 2, 8), low: 25.75, high: 26.875, open: 26.75, close: 26.00, avg: 26.3125 },
    //         { date: new Date(1994, 2, 9), low: 25.75, high: 26.75, open: 26.125, close: 26.25, avg: 25.9375 },
    //         { date: new Date(1994, 2, 10), low: 25.75, high: 26.375, open: 26.375, close: 25.875, avg: 26.0625 },
    //         { date: new Date(1994, 2, 11), low: 24.875, high: 26.125, open: 26.00, close: 25.375, avg: 25.5 },
    //         { date: new Date(1994, 2, 14), low: 25.125, high: 26.00, open: 25.625, close: 25.75, avg: 25.5625 },
    //         { date: new Date(1994, 2, 15), low: 25.875, high: 26.625, open: 26.125, close: 26.375, avg: 26.25 }];
    //     });
    // }


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


    function statsCampaigns(from, to, skip, take,sort,order,stat_by,filter) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
        params: {from_date: from, to_date: to,  skip: skip, take: take, sort: sort, order: order, stat_by: stat_by, filter: filter}
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
        .then(function (res) {
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
    _this.statsCampaigns = statsCampaigns;
    _this.statsChart = statsChart;
    _this.bucketsCpa = bucketsCpa;
    _this.campaignDetails = campaignDetails;
    _this.campaignDomains = campaignDomains

  }
})();
