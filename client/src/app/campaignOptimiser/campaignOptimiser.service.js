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
          //7 - Whole week, 0 - Sunday, 1 - Monday, .., 6 - Saturday
          for (var itemAnal in res.data.data[item].analitics) {
            if (res.data.data[item].analitics[itemAnal].day == '0') {
              res.data.data[item].analitics[itemAnal].day = 'Sunday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '1') {
              res.data.data[item].analitics[itemAnal].day = 'Monday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '2') {
              res.data.data[item].analitics[itemAnal].day = 'Tuesday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '3') {
              res.data.data[item].analitics[itemAnal].day = 'Wednesday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '4') {
              res.data.data[item].analitics[itemAnal].day = 'Thursday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '5') {
              res.data.data[item].analitics[itemAnal].day = 'Friday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '6') {
              res.data.data[item].analitics[itemAnal].day = 'Saturday';
            }
            if (res.data.data[item].analitics[itemAnal].day == '7') {
              res.data.data[item].analitics[itemAnal].day = 'All week';
            }

            var bad = res.data.data[item].analitics[itemAnal].bad;
            var good = res.data.data[item].analitics[itemAnal].good;
            var badOpasity = 1;
            var goodOpasity = 1;
            var k = +((bad*100)/(bad + good));
            if (((k/100 <=0.5)) && (((k/100) >0.45)) || ((((100-k)/100)<=0.5) && (((100-k)/100)>0.45 ))) { badOpasity = 0.03; goodOpasity = 0.03;}
            if ((k/100 <0.44 && k/100 >0.4)  || (((100-k)/100)<0.44 && ((100-k)/100)>0.4 )) { badOpasity = 0.09; goodOpasity = 0.09;}
            if ((k/100 <0.4 && k/100 >0.3)   || (((100-k)/100)<0.4 && ((100-k)/100)>0.3 )) { badOpasity = 0.2; goodOpasity = 0.2;}
            if ((k/100 <0.3 && k/100 >0.2)   || (((100-k)/100)<0.3 && ((100-k)/100)>0.2 )) { badOpasity = 0.5; goodOpasity = 0.5;}
            if ((k/100 <0.2 && k/100 >0.1)   || (((100-k)/100)<0.2 && ((100-k)/100)>0.1 )) { badOpasity = 0.7; goodOpasity = 0.7;}
            if ((k/100 <0.1 && k/100 >0)     || (((100-k)/100)<0.1 && ((100-k)/100)>0 )) { badOpasity = 1.0; goodOpasity = 1.0;}
            var goodDiagram = (100-k)+'%';
            var badDiagram = k+'%';

            if (res.data.data[item].analitics[itemAnal].good == -1) {
              itemArray.push({
                "day" : res.data.data[item].analitics[itemAnal].day,
                "good": null,
                "bad": null,
                "checked": null,
                "badDiagram": null,
                "goodDiagram": null,
                "badOpasity": 0,
                "goodOpasity": 0,
                "k": 0
              });
            } else {
              itemArray.push({
                "day" : res.data.data[item].analitics[itemAnal].day,
                "good": res.data.data[item].analitics[itemAnal].good,
                "bad": res.data.data[item].analitics[itemAnal].bad,
                "checked": res.data.data[item].analitics[itemAnal].checked,
                "badDiagram": badDiagram,
                "goodDiagram": goodDiagram,
                "badOpasity": badOpasity,
                "goodOpasity": goodOpasity,
                "k": k
              });
            }
          }

            res.data.data[item].NetworkPublisher= res.data.data[item].NetworkPublisher,
            res.data.data[item].placement= res.data.data[item].placement,
            res.data.data[item].placement_name= res.data.data[item].placement_name,
            res.data.data[item].cvr= parseFloat((res.data.data[item].cvr || 0).toFixed(4)),
            res.data.data[item].ctr= parseFloat((item.ctr || 0).toFixed(4)),
            res.data.data[item].cpc= parseFloat((item.cpc || 0).toFixed(4)),
            res.data.data[item].cpm= parseFloat((item.cpm || 0).toFixed(4)),
            res.data.data[item].imp= parseFloat((item.imp || 0).toFixed(4)),
            res.data.data[item].cpa= parseFloat((item.cpa || 0).toFixed(4)),
            res.data.data[item].clicks= parseFloat((item.clicks || 0).toFixed(4)),
            res.data.data[item].conv= parseFloat((item.conv || 0).toFixed(4)),
            res.data.data[item].cost= parseFloat((item.cost || 0).toFixed(2)),
            res.data.data[item].analitics = itemArray,
            res.data.data[item].imps_viewed= parseFloat((item.imps_viewed || 0).toFixed(4)),
            res.data.data[item].view_measured_imps= parseFloat((item.view_measured_imps || 0).toFixed(4)),
            res.data.data[item].view_measurement_rate= parseFloat((item.view_measurement_rate || 0).toFixed(1)),
            res.data.data[item].view_rate= parseFloat((item.view_rate || 0).toFixed(1)),
            res.data.data[item].state= {
              blackList: res.data.data[item].state.blackList,
              suspended: res.data.data[item].state.suspended,
              whiteList: res.data.data[item].state.whiteList
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
        method: 'PUT',
        url: '/api/v1/campaigns/' + encodeURI(id) + '/domains',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
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
        url: '/api/v1/campaigns/' + id + '/placement',
        data: {placementId: placementId, checked: checked}
      })
      .then(function (res) {
        return res;
      })
      .catch(function (err) {
        $window.DevExpress.ui.notify(err.statusText, "error", 4000);
      });
    }

    _this.decisionML = decisionML;
    _this.campaignTargeting = campaignTargeting;
    _this.editCampaignDomains = editCampaignDomains;
    _this.getGridCampaignStore = getGridCampaignStore;

  }
})();
