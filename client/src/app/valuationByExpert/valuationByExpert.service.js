(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('valuationByExpertS', valuationByExpertS);

  /** @ngInject */
  function valuationByExpertS($http, $cookies, $window) {
    var _this = this;

    function getGridCampaignStore() {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },
        load: function () {
          return _MLRandomTestSet('send');
        }
      });
    }

    function _MLRandomTestSet(send) {
      return $http({
        method: 'GET',
        url: '/api/v1/MLRandomTestSet',
        headers: {'Authoriszation': 'Token ' + $cookies.get('token')},
        params: {
          action: send
        }
      })
        .then(function (res) {
          for (var item in res.data) {
            res.data[item].imps= parseFloat((res.data[item].imps || 0).toFixed(4));
            res.data[item].clicks= parseFloat((res.data[item].clicks || 0).toFixed(4));
            res.data[item].total_convs= parseFloat((res.data[item].total_convs || 0).toFixed(4));
            res.data[item].imps_viewed= parseFloat((res.data[item].imps_viewed || 0).toFixed(4));
            res.data[item].view_measured_imps= parseFloat((res.data[item].view_measured_imps || 0).toFixed(4));
            res.data[item].sum_cost= parseFloat((res.data[item].sum_cost || 0).toFixed(4));
            res.data[item].cpa= parseFloat((res.data[item].cpa || 0).toFixed(4));
            res.data[item].ctr= parseFloat((res.data[item].ctr || 0).toFixed(4));
            res.data[item].cvr= parseFloat((res.data[item].cvr || 0).toFixed(4));
            res.data[item].cpc= parseFloat((res.data[item].cpc || 0).toFixed(4));
            res.data[item].cpm= parseFloat((res.data[item].cpm || 0).toFixed(4));
            res.data[item].view_rate= parseFloat((res.data[item].view_rate || 0).toFixed(1));
            res.data[item].view_measurement_rate= parseFloat((res.data[item].view_measurement_rate || 0).toFixed(1));
          }

          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function goodBadSend(id, checked) {
      return $http({
        method: 'GET',
        url: '/api/v1/MLExpertMark',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          placementId: id,
          day: 7,
          decision: checked
        }
      })
        .then(function (res) {
          return res.status;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.statusText, "error", 4000);
        });
    }

    //http://localhost:8000/api/v1/MLGetAUC?test_type=kmeans&test_name=ctr_cvr_cpc_cpm_cpa
    function MLGetAUC(test_type) {
      return $http({
        method: 'GET',
        url: '/api/v1/MLGetAUC',
        headers: {'Authorization': 'Token ' + $cookies.get('token')},
        params: {
          test_type: test_type,
          test_name: 'ctr_cvr_cpc_cpm_cpa'
        }
      })
        .then(function (res) {
          for (var item in res.data.chartCoord) {
            res.data.chartCoord[item].rocSensetivities = parseFloat((res.data.chartCoord[item].rocSensetivities || 0).toFixed(4));
            res.data.chartCoord[item].rocFalsePositiveRate = parseFloat((res.data.chartCoord[item].rocFalsePositiveRate || 0).toFixed(4));
          }
          res.data.auc = parseFloat((res.data.auc || 0).toFixed(4));
          res.data.chartCoord[0].diagonal = 0;
          res.data.chartCoord[res.data.chartCoord.length-1].diagonal = 100;
          return res.data;
        })
        .catch(function (err) {
          if (err.status == 400) {
            return $window.DevExpress.ui.notify("Not all placements are marked by experts", "warning", 6000);
          }
          $window.DevExpress.ui.notify(err.statusText, "error", 4000);
        });
    }

    function chartAUC () {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },
        load: function () {
          return MLGetAUC()
          .then(function (result) {
            return result;
          });
        }
      });
    }

    _this.MLGetAUC = MLGetAUC;
    _this.chartAUC = chartAUC;
    _this.goodBadSend = goodBadSend;
    _this._MLRandomTestSet = _MLRandomTestSet;
    _this.getGridCampaignStore = getGridCampaignStore;
  }
})();
