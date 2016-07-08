(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('Camp', Camp);

  /** @ngInject */
  function Camp($http) {
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
              url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
              params: {id:id, from: from, to: to, section: section}
          })
              .then(function (res) {
                  return {
                   all:[{
                      section: "Android",
                      data: 60
                  }, {
                      section: "iOs",
                      data: 30
                  }, {
                      section: "Windows",
                      data: 10
                  }],
                  conversions: [{
                      section: "Android",
                      data: 23
                  }, {
                      section: "iOs",
                      data: 72
                  }, {
                      section: "Windows",
                      data:5
                  }],
                  cpabuckets:{
                      "cnn.com": "34.12",
                          "lion.com": "3.76",
                          "tiger.com": "7.97",
                          "cat.com": "1.23",
                          "dog.com": "16.11",
                          "mouse.com": "6.53",
                          "rabbit.com": "0.91",
                          "bear.com": "1.9",
                          "snake.com": "3.7",
                          "squirrel.com": "4.78",
                          "hamster.com": "0.62"
                  }}
              });
      }

    function statsChart(from, to, by) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/statistics',
        params: {from: from, to: to, by: by}
      })
        .then(function (res) {
          //return res.data.statistics;
          return [
          { day: "2016-06-27T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: -5, mediaspent: 5, conversions: 40, ctr: 15  },
          { day: "2016-06-28T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 1, mediaspent: 15, conversions: 23, ctr: -10 },
          { day: "2016-06-29T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 2, mediaspent: 5, conversions: 33, ctr: 10 },
          { day: "2016-06-30T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: 6, mediaspent: 55, conversions: 87, ctr: -42 },
          { day: "2016-07-01T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: 9, mediaspent: 44, conversions: -20, ctr: -57 },
          { day: "2016-07-02T00:00:00Z", impression: 10, cpa: 10, cpc: 15, clicks: 8, mediaspent: 77, conversions: 23, ctr: 99 },
          { day: "2016-07-03T00:00:00Z", impression: 30, cpa: 50, cpc: 13, clicks: 23, mediaspent: 66, conversions: -10, ctr: 110 },
          { day: "2016-07-04T00:00:00Z", impression: 40, cpa: 50, cpc: 14, clicks: 12, mediaspent: 11, conversions: 37, ctr: 56 },
          { day: "2016-07-05T00:00:00Z", impression: 50, cpa: 90, cpc: 90, clicks: -10, mediaspent: 99, conversions: 50, ctr: 67 },
          { day: "2016-07-06T00:00:00Z", impression: 40, cpa: 175, cpc: 120, clicks: 31, mediaspent: -11, conversions: 23, ctr: 67 },
          { day: "2016-07-07T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 70, mediaspent: -2, conversions: 58, ctr: -20 },
          { day: "2016-07-08T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 26, mediaspent: 5, conversions: 21, ctr: -10 },
          { day: "2016-07-09T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 52, mediaspent: 76, conversions: 10, ctr: 70 },
          { day: "2016-07-10T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 1, mediaspent: 32, conversions: 49, ctr: 90 },
          { day: "2016-07-11T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 38, mediaspent: 11, conversions: 99, ctr: 10 },
          { day: "2016-07-12T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: -16, mediaspent: 15, conversions: 60, ctr: 58 },
          { day: "2016-07-13T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: -40, mediaspent: 46, conversions: 23, ctr: 78 },
          { day: "2016-07-14T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: 24, mediaspent: 68, conversions: -20, ctr: 80 },
          { day: "2016-07-15T00:00:00Z", impression: 10, cpa: 10, cpc: 15, clicks: 12, mediaspent: 49, conversions: -37, ctr:22 },
          { day: "2016-07-16T00:00:00Z", impression: 30, cpa: 100, cpc: 13, clicks: 83, mediaspent: 36, conversions: -1, ctr: 67 },
          { day: "2016-07-17T00:00:00Z", impression: 40, cpa: 110, cpc: 14, clicks: 41, mediaspent: 28, conversions: 65, ctr: -10 },
          { day: "2016-07-18T00:00:00Z", impression: 50, cpa: 90, cpc: 90, clicks: 27, mediaspent: 95, conversions: 23, ctr: 88 },
          { day: "2016-07-19T00:00:00Z", impression: 40, cpa: 95, cpc: 120, clicks: 83, mediaspent: 92, conversions: 10, ctr: 77 },
          { day: "2016-07-20T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: -20, mediaspent: 15, conversions: 7, ctr: 66 },
          { day: "2016-07-21T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 56, mediaspent: 54, conversions: 34, ctr: -10 },
          { day: "2016-07-22T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 17, mediaspent: 22, conversions: 65, ctr: -40 },
          { day: "2016-07-23T00:00:00Z", impression: -12, cpa: 10, cpc: 32, clicks: 22, mediaspent: 77, conversions: 52, ctr: -70 },
          { day: "2016-07-24T00:00:00Z", impression: -32, cpa: 30, cpc: 12, clicks: 29, mediaspent: 90, conversions: 23, ctr: -54 },
          { day: "2016-07-25T00:00:00Z", impression: -20, cpa: 20, cpc: 30, clicks: 90, mediaspent: 17, conversions: 59, ctr: 28 },
          { day: "2016-07-26T00:00:00Z", impression: -39, cpa: 50, cpc: 19, clicks: 45, mediaspent: 47, conversions: 82, ctr: 65 },
          { day: "2016-07-27T00:00:00Z", impression: -10, cpa: 10, cpc: 15, clicks: -30, mediaspent: 32, conversions: 33, ctr: 58 }
          ];
        });
    }



      function cpaReport(id, from, to) {
          return $http({
              method: 'GET',
              url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
              params: {id:id, from: from, to: to}
          })
              .then(function (res) {
                  return [{
                      "Date": "03/12/2013",
                      "Open": "827.90",
                      "High": "830.69",
                      "Low": "822.31",
                      "Close": "825.31",
                      "Volume": "1641413"
                  },{
                      "Date": "03/13/2013",
                      "Open": "826.99",
                      "High": "826.99",
                      "Low": "817.39",
                      "Close": "821.54",
                      "Volume": "1651111"
                  }, {
                      "Date": "03/14/2013",
                      "Open": "818.50",
                      "High": "820.30",
                      "Low": "813.34",
                      "Close": "814.30",
                      "Volume": "3099791"
                  },  {
                      "Date": "03/17/2013",
                      "Open": "805.00",
                      "High": "812.76",
                      "Low": "801.47",
                      "Close": "807.79",
                      "Volume": "1838552"
                  }, {
                      "Date": "03/18/2013",
                      "Open": "811.24",
                      "High": "819.25",
                      "Low": "806.45",
                      "Close": "811.32",
                      "Volume": "2098176"

                  }, {
                      "Date": "03/19/2013",
                      "Open": "816.83",
                      "High": "817.51",
                      "Low": "811.44",
                      "Close": "814.71",
                      "Volume": "1464122"
                  }, {
                      "Date": "03/20/2013",
                      "Open": "811.29",
                      "High": "816.92",
                      "Low": "809.85",
                      "Close": "811.26",
                      "Volume": "1477590"
                  }, {
                      "Date": "03/21/2013",
                      "Open": "814.74",
                      "High": "815.24",
                      "Low": "809.64",
                      "Close": "810.31",
                      "Volume": "1491678"
                  }, {
                      "Date": "03/24/2013",
                      "Open": "812.41",
                      "High": "819.23",
                      "Low": "806.82",
                      "Close": "809.64",
                      "Volume": "1712684"
                  }, {
                      "Date": "03/25/2013",
                      "Open": "813.50",
                      "High": "814.00",
                      "Low": "807.79",
                      "Close": "812.42",
                      "Volume": "1191912"
                  }, {
                      "Date": "03/26/2013",
                      "Open": "806.68",
                      "High": "807.00",
                      "Low": "801.33",
                      "Close": "802.66",
                      "Volume": "2163295"
                  }, {
                      "Date": "03/27/2013",
                      "Open": "803.99",
                      "High": "805.37",
                      "Low": "793.30",
                      "Close": "794.19",
                      "Volume": "2287712"
                  }, {
                      "Date": "03/31/2013",
                      "Open": "795.01",
                      "High": "802.25",
                      "Low": "793.25",
                      "Close": "801.19",
                      "Volume": "1807580"
                  }, {
                      "Date": "04/01/2013",
                      "Open": "804.54",
                      "High": "814.83",
                      "Low": "804.00",
                      "Close": "813.04",
                      "Volume": "2041713"
                  }, {
                      "Date": "04/02/2013",
                      "Open": "813.46",
                      "High": "814.20",
                      "Low": "800.67",
                      "Close": "806.20",
                      "Volume": "1738753"
                  }, {
                      "Date": "04/03/2013",
                      "Open": "804.25",
                      "High": "805.75",
                      "Low": "791.30",
                      "Close": "795.07",
                      "Volume": "2448102"
                  }, {
                      "Date": "04/04/2013",
                      "Open": "786.06",
                      "High": "786.99",
                      "Low": "776.40",
                      "Close": "783.05",
                      "Volume": "3433994"
                  }, {
                      "Date": "04/07/2013",
                      "Open": "778.75",
                      "High": "779.55",
                      "Low": "768.40",
                      "Close": "774.85",
                      "Volume": "2832718"
                  }, {
                      "Date": "04/08/2013",
                      "Open": "775.50",
                      "High": "783.75",
                      "Low": "773.11",
                      "Close": "777.65",
                      "Volume": "2157928"
                  }, {
                      "Date": "04/09/2013",
                      "Open": "782.92",
                      "High": "792.35",
                      "Low": "776.00",
                      "Close": "790.18",
                      "Volume": "1978862"
                  }, {
                      "Date": "04/10/2013",
                      "Open": "792.88",
                      "High": "793.10",
                      "Low": "784.06",
                      "Close": "790.39",
                      "Volume": "2028766"
                  }, {
                      "Date": "04/11/2013",
                      "Open": "791.99",
                      "High": "792.10",
                      "Low": "782.93",
                      "Close": "790.05",
                      "Volume": "1636829"
                  }, {
                      "Date": "04/14/2013",
                      "Open": "785.95",
                      "High": "797.00",
                      "Low": "777.02",
                      "Close": "781.93",
                      "Volume": "2454767"
                  }, {
                      "Date": "04/15/2013",
                      "Open": "786.59",
                      "High": "796.00",
                      "Low": "783.92",
                      "Close": "793.37",
                      "Volume": "1742374"
                  }, {
                      "Date": "04/16/2013",
                      "Open": "786.75",
                      "High": "790.84",
                      "Low": "778.10",
                      "Close": "782.56",
                      "Volume": "2037355"
                  }, {
                      "Date": "04/17/2013",
                      "Open": "785.35",
                      "High": "785.80",
                      "Low": "761.26",
                      "Close": "765.91",
                      "Volume": "3328777"
                  }]
              });
      }


      function campaignDomains(id, from, to) {
          return $http({
              method: 'GET',
              url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
              params: {id:id, from: from, to: to}
          })
              .then(function (res) {
                  return[{
                      "placement":"CNN.com",
                      "NetworkPublisher":"Google Adx",
                      "conv":"8",
                      "imp":"5500",
                      "clicks":"21",
                      "cpc":"$0,31",
                      "cpm":"$1,38",
                      "cvr":"",
                      "ctr":"",
                      "state": {
                          "whiteList": "true",
                          "blackList": "false",
                          "suspended": "false"
                      }
                  },
                      {
                          "placement":"Hidden",
                          "NetworkPublisher":"PubMatic",
                          "conv":"3",
                          "imp":"5500",
                          "clicks":"21",
                          "cpc":"$0,31",
                          "cpm":"$1,38",
                          "cvr":"",
                          "ctr":"",
                          "state": {
                              "whiteList": "false",
                              "blackList": "true",
                              "suspended": "false"
                          }
                      },
                      {
                          "placement":"BBC.com",
                          "NetworkPublisher":"OpenX",
                          "conv":"1",
                          "imp":"5500",
                          "clicks":"21",
                          "cpc":"$0,31",
                          "cpm":"$1,38",
                          "cvr":"",
                          "ctr":"",
                          "state": {
                              "whiteList": "false",
                              "blackList": "false",
                              "suspended": "true"
                          }
                      },
                      {
                          "placement":"msn.com",
                          "NetworkPublisher":"Rubicon",
                          "conv":"8",
                          "imp":"5500",
                          "clicks":"21",
                          "cpc":"$0,31",
                          "cpm":"$1,38",
                          "cvr":"",
                          "ctr":"",
                          "state": {
                              "whiteList": "true",
                              "blackList": "false",
                              "suspended": "false"
                          }
                      }
                  ];
              });
      }


    function statsCampaigns(from, to, skip, take,sort,order,stat_by,filter) {
      return $http({
        method: 'GET',
        url: 'http://private-anon-d71dffb7f-rtbs.apiary-mock.com/api/v1/campaigns',
        params: {from: from, to: to,  skip: skip, take: take, sort: sort, order: order, stat_by: stat_by, filter: filter}
      })
        .then(function (res) {
          return res.data;
        });
    }

    function cpaBuckets(min, max) {

        var arrayOfCpa = {
          "cnn.com": "34.12",
          "lion.com": "3.76",
          "tiger.com": "7.97",
          "cat.com": "1.23",
          "dog.com": "16.11",
          "mouse.com": "6.53",
          "rabbit.com": "0.91",
          "bear.com": "1.9",
          "snake.com": "3.7",
          "squirrel.com": "4.78",
          "hamster.com": "0.62"
        };
      var a = [];
      for (var i in arrayOfCpa) {
           if ((Number(arrayOfCpa[i])>=Number(min)) && (arrayOfCpa[i]<Number(max))) {
           a.push(i);
        }
      }
  return a;
      }



    _this.cpaReport = cpaReport;
    _this.nameCampaigns = nameCampaigns;
    _this.statsCampaigns = statsCampaigns;
    _this.statsChart = statsChart;
    _this.cpaBuckets = cpaBuckets;
    _this.campaignDetails = campaignDetails;
    _this.campaignDomains = campaignDomains

  }
})();
