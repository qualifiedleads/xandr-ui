(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('CampaignOptimiser', CampaignOptimiser);

  /** @ngInject */
  function CampaignOptimiser($http, $cookies, $window) {
    var _this = this;
    var _totalCountCampaign = 0;

    function getGridCampaignStore(campId, dataStart, dataEnd) {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _totalCountCampaign;
        },
        load: function (loadOptions) {
          if (loadOptions.searchOperation && loadOptions.dataField) {
            loadOptions.take = 999999;
          }
          return _campaignDomains(campId, dataStart, dataEnd, loadOptions.skip, loadOptions.take, loadOptions.sort, loadOptions.order, loadOptions.filter, loadOptions.totalSummary);
        }
      });
    }

    function _campaignDomains(id, from, to, skip, take, sort, order, filter, totalSummary) {
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
        take = 10;
      }
      if (skip == null) {
        skip = 0;
      }

      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          from_date: from,
          to_date: to,
          skip: skip,
          take: take,
          sort: sort,
          order: order,
          filter: filter,
          totalSummary: totalSummary
        }
      })
        .then(function (res) {
          for (var item in res.data.data) {
            var itemArray = [];
            /*          res.data.data[item].analitics = {
             "good": 1,
             "bad": 0.5,
             "checked": true,
             };*/
            if (res.data.data[item].analitics.good == -1 || res.data.data[item].analitics.good == -2 || res.data.data[item].analitics.good == -3) {
              itemArray = null;
            } else {
              var bad = res.data.data[item].analitics.bad;
              var good = res.data.data[item].analitics.good;
              var badOpasity = 1;
              var goodOpasity = 1;
              var k = +((bad*100)/(bad + good));
              if (((k/100 <=0.5)) && (((k/100) >0.45)) || ((((100-k)/100)<=0.5) && (((100-k)/100)>0.45 ))) { badOpasity = 0.03; goodOpasity = 0.03;}
              if ((k/100 <0.45 && k/100 >0.4)  || (((100-k)/100)<0.45 && ((100-k)/100)>0.4 )) { badOpasity = 0.09; goodOpasity = 0.09;}
              if ((k/100 <0.4 && k/100 >0.3)   || (((100-k)/100)<0.4 && ((100-k)/100)>0.3 )) { badOpasity = 0.2; goodOpasity = 0.2;}
              if ((k/100 <0.3 && k/100 >0.2)   || (((100-k)/100)<0.3 && ((100-k)/100)>0.2 )) { badOpasity = 0.5; goodOpasity = 0.5;}
              if ((k/100 <0.2 && k/100 >0.1)   || (((100-k)/100)<0.2 && ((100-k)/100)>0.1 )) { badOpasity = 0.7; goodOpasity = 0.7;}
              if ((k/100 <0.1 && k/100 >0)     || (((100-k)/100)<0.1 && ((100-k)/100)>0 )) { badOpasity = 1.0; goodOpasity = 1.0;}
              var goodDiagram = (100-k)+'%';
              var badDiagram = k+'%';


              itemArray = {
                "good": res.data.data[item].analitics.good,
                "bad": res.data.data[item].analitics.bad,
                "checked": res.data.data[item].analitics.checked,
                "badDiagram": badDiagram,
                "goodDiagram": goodDiagram,
                "badOpasity": badOpasity,
                "goodOpasity": goodOpasity,
                "k": k
              };
            }

            res.data.data[item].cvr= parseFloat((res.data.data[item].cvr || 0).toFixed(4)),
              res.data.data[item].ctr= parseFloat((res.data.data[item].ctr || 0).toFixed(4)),
              res.data.data[item].cpc= parseFloat((res.data.data[item].cpc || 0).toFixed(4)),
              res.data.data[item].cpm= parseFloat((res.data.data[item].cpm || 0).toFixed(4)),
              res.data.data[item].imp= parseFloat((res.data.data[item].imp || 0).toFixed(4)),
              res.data.data[item].cpa= parseFloat((res.data.data[item].cpa || 0).toFixed(4)),
              res.data.data[item].clicks= parseFloat((res.data.data[item].clicks || 0).toFixed(4)),
              res.data.data[item].conv= parseFloat((res.data.data[item].conv || 0).toFixed(4)),
              res.data.data[item].cost= parseFloat((res.data.data[item].cost || 0).toFixed(2)),
              res.data.data[item].analitics = itemArray,
              res.data.data[item].imps_viewed= parseFloat((res.data.data[item].imps_viewed || 0).toFixed(4)),
              res.data.data[item].view_measured_imps= parseFloat((res.data.data[item].view_measured_imps || 0).toFixed(4)),
              res.data.data[item].view_measurement_rate= parseFloat((res.data.data[item].view_measurement_rate || 0).toFixed(1)),
              res.data.data[item].view_rate= parseFloat((res.data.data[item].view_rate || 0).toFixed(1)),
              res.data.data[item].state= {
                blackList: res.data.data[item].state & 2,
                suspended: res.data.data[item].state & 1,
                whiteList: res.data.data[item].state & 4
              }
          }

          _totalCountCampaign = res.data.totalCount;
          _this.totalSummary = res.data.totalSummary;

          return res.data.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }


    function campaignTargeting(id, from, to) {
      return {
        domains: [
          "about.com",
          "celebritytoob.com",
          "lotto.pch.com",
          "verywell.com",
        ],
        geo: [
          "US",
          "UK",
          "NZ"
        ],
        device: [
          "Desktops & Laptops",
          "AND",
          "Web"
        ],
        block: [
          "Phones",
          "Tablets",
          "Mobile web",
          "Apps"
        ]
      };
    }

    function editCampaignDomains(id,placement,activeState, time) {
      return $http({
        method: 'POST',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/changestate',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        data: {
          placement: placement,
          activeState: activeState,
          suspendTimes: time
        }
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function decisionML(id, placementId, checked) {
      return $http({
        method: 'POST',
        url: '/api/v1/campaigns/' + id + '/MLPlacement',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        data: {placementId: placementId, checked: checked}
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, "error", 4000);
        });
    }

    function showAllMLDiagram(id, placementId) {
      return $http({
        method: 'GET',
        url: '/api/v1/campaigns/' + id + '/MLPlacement',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          placementId: placementId,
        }
      })
        .then(function (res) {
          var itemArray = [];
          for (var item in res.data.analitics) {
            if (res.data.analitics[item].good == -1) {
              itemArray[item] = false;
            } else {
              if (res.data.analitics[item].day == '0') {
                res.data.analitics[item].day = 'Sunday';
              }
              if (res.data.analitics[item].day == '1') {
                res.data.analitics[item].day = 'Monday';
              }
              if (res.data.analitics[item].day == '2') {
                res.data.analitics[item].day = 'Tuesday';
              }
              if (res.data.analitics[item].day == '3') {
                res.data.analitics[item].day = 'Wednesday';
              }
              if (res.data.analitics[item].day == '4') {
                res.data.analitics[item].day = 'Thursday';
              }
              if (res.data.analitics[item].day == '5') {
                res.data.analitics[item].day = 'Friday';
              }
              if (res.data.analitics[item].day == '6') {
                res.data.analitics[item].day = 'Saturday';
              }
              if (res.data.analitics[item].day == '7') {
                res.data.analitics[item].day = 'All week';
              }

              var bad = res.data.analitics[item].bad;
              var good = res.data.analitics[item].good;
              var badOpasity = 1;
              var goodOpasity = 1;
              var k = +((bad * 100) / (bad + good));
              if (((k / 100 <= 0.5)) && (((k / 100) >= 0.45)) || ((((100 - k) / 100) <= 0.5) && (((100 - k) / 100) > 0.45 ))) {
                badOpasity = 0.03;
                goodOpasity = 0.03;
              }
              if ((k / 100 < 0.45 && k / 100 > 0.4) || (((100 - k) / 100) <= 0.45 && ((100 - k) / 100) > 0.4 )) {
                badOpasity = 0.09;
                goodOpasity = 0.09;
              }
              if ((k / 100 <= 0.4 && k / 100 > 0.3) || (((100 - k) / 100) <= 0.4 && ((100 - k) / 100) > 0.3 )) {
                badOpasity = 0.2;
                goodOpasity = 0.2;
              }
              if ((k / 100 <= 0.3 && k / 100 > 0.2) || (((100 - k) / 100) <= 0.3 && ((100 - k) / 100) > 0.2 )) {
                badOpasity = 0.5;
                goodOpasity = 0.5;
              }
              if ((k / 100 <= 0.2 && k / 100 > 0.1) || (((100 - k) / 100) <= 0.2 && ((100 - k) / 100) > 0.1 )) {
                badOpasity = 0.7;
                goodOpasity = 0.7;
              }
              if ((k / 100 <= 0.1 && k / 100 > 0) || (((100 - k) / 100) <= 0.1 && ((100 - k) / 100) > 0 )) {
                badOpasity = 1.0;
                goodOpasity = 1.0;
              }
              var goodDiagram = (100 - k) + '%';
              var badDiagram = k + '%';

              itemArray.push({
                "day": res.data.analitics[item].day,
                "good": res.data.analitics[item].good,
                "bad": res.data.analitics[item].bad,
                "checked": res.data.analitics[item].checked,
                "badDiagram": badDiagram,
                "goodDiagram": goodDiagram,
                "badOpasity": badOpasity,
                "goodOpasity": goodOpasity,
                "k": k
              });
            }
          }
          return itemArray;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, "error", 4000);
        });
      /*var res = {
       data: [
       {
       "day": 0,
       "good": 0.8,
       "bad": 0.5,
       "checked": true,
       },
       {
       "day": 1,
       "good": 1,
       "bad": 1.5,
       "checked": true,
       },
       {
       "day": 2,
       "good": 5,
       "bad": 0.5,
       "checked": true,
       },
       {
       "day": 3,
       "good": 0.1,
       "bad": 0.5,
       "checked": true,
       },
       {
       "day": 4,
       "good": 1,
       "bad": 0.8,
       "checked": true,
       },
       {
       "day": 5,
       "good": 0.78,
       "bad": 1.5,
       "checked": true,
       },
       {
       "day": 6,
       "good": 1,
       "bad": 1.1,
       "checked": true,
       },
       {
       "day": 7,
       "good": 1,
       "bad": 0.5,
       "checked": true,
       }]
       };*/



    }

    _this.showAllMLDiagram = showAllMLDiagram;
    _this.decisionML = decisionML;
    _this.campaignTargeting = campaignTargeting;
    _this.editCampaignDomains = editCampaignDomains;
    _this.getGridCampaignStore = getGridCampaignStore;

  }
})();
