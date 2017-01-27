(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('BCCController', BCCController);

  /** @ngInject */
  function BCCController($window, $state, $localStorage, $translate, BCC, Campaign) {
    var vm = this;
    var LC = $translate.instant;
    var ruleSuspend = false;
    var ruleIndexPopUp = '';
    var selectCampaignId;
    var domainAreaText;
    vm.loadindicatorVisible = false;
    vm.message = false;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.line_item = Campaign.line_item;
    vm.line_item_id = Campaign.line_item_id;


    if ($localStorage.campaign == null) {
      $state.go('home.main');
    }

    BCC.campaignList($localStorage.advertiser.id).then(function (res) {
      vm.selectCampaignStore = res;
    });

    //region DATE PIKER
    /** DATE PIKER **/
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
      $localStorage.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
      $localStorage.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
      vm.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
      vm.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
    } else {
      if ($localStorage.dataStart == null || $localStorage.dataEnd == null) {
        $localStorage.SelectedTime = 0;
        $localStorage.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
        $localStorage.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
        vm.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
        vm.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
      } else {
        vm.dataStart = $localStorage.dataStart;
        vm.dataEnd = $localStorage.dataEnd;
      }
    }

    var products = [
      {
        ID: 0,
        Name: LC('MAIN.DATE_PICKER.YESTERDAY'),
        dataStart: $window.moment({hour: '00'}).subtract(1, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix()
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(3, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(7, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(14, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(21, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 5,
        Name: LC('MAIN.DATE_PICKER.CURRENT_MONTH'),
        dataStart: $window.moment().startOf('month').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 6,
        Name: LC('MAIN.DATE_PICKER.LAST_MONTH'),
        dataStart: $window.moment().subtract(1, 'month').startOf('month').unix(),
        dataEnd: $window.moment().subtract(1, 'month').endOf('month').unix()
      }, {
        ID: 7,
        Name: LC('MAIN.DATE_PICKER.LAST_90_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(90, 'day').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 8,
        Name: LC('MAIN.DATE_PICKER.ALL_TIME'),
        dataStart: 0,
        dataEnd: $window.moment().unix()
      }
    ];
    //endregion

    vm.UI = {
      loadPanel: {
        shadingColor: "rgba(0,0,0,0.4)",
        bindingOptions: {
          visible: "bcc.loadindicatorVisible"
        },
        showIndicator: true,
        showPane: true,
        shading: true,
        closeOnOutsideClick: false
      },
      send: {
        text: LC('BCC.CREATE'),
        onClick: function () {
          if ((!selectCampaignId) || (selectCampaignId == null)) {
            $window.DevExpress.ui.notify("Select campaign please", "warning", 4000);
            return
          }
          if ((!domainAreaText) || (domainAreaText == null)) {
            $window.DevExpress.ui.notify("Insert the list of domains please", "warning", 4000);
            return
          }
          vm.loadindicatorVisible = true;
          return BCC.campaignCreateBulk($localStorage.advertiser.id, selectCampaignId, domainAreaText).then(function (res) {
            if (res == false) {
              vm.loadindicatorVisible = false;
              return
            }
            vm.message = 'Created campaigns: ' + res;
            vm.loadindicatorVisible = false;
            // $scope.$apply();
          })
        }
      },
      searchOptions: {
        displayExpr: "name",
        valueExpr: "id",
        searchEnabled: true,
        bindingOptions: {
          dataSource: 'bcc.selectCampaignStore'
        },
        onValueChanged: function (res, data) {
          selectCampaignId = res.value;
        }
      },
      domainArea: {
        height: 150,
        placeholder: LC('BCC.PLACEHOLDER-DOMAIN'),
        onValueChanged: function (data) {
          domainAreaText = data.value;
        }
      },
      datePiker: {
        items: products,
        displayExpr: 'Name',
        valueExpr: 'ID',
        value: products[$localStorage.SelectedTime].ID,
        onValueChanged: function (e) {
          $localStorage.SelectedTime = e.value;
          $localStorage.dataStart = products[e.value].dataStart;
          $localStorage.dataEnd = products[e.value].dataEnd;
          $state.reload();
        }
      }
    };
  }
})();
