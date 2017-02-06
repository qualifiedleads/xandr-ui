(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('AutomaticCpmController', AutomaticCpmController);

  /** @ngInject */
  function AutomaticCpmController($window, $state, $localStorage, AutomaticCpm, $translate, Campaign, $rootScope) {
    var vm = this;
    var LC = $translate.instant;
    $rootScope.id = Campaign.id;
    var selectMethod = null;
    vm.charIsUpdating = false;
    vm.loadindicatorVisible = false;
    $rootScope.name = Campaign.campaign;
    $rootScope.line_item = Campaign.line_item;
    $rootScope.line_item_id = Campaign.line_item_id;

    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.line_item = Campaign.line_item;
    vm.line_item_id = Campaign.line_item_id;
    vm.Init = [];

    vm.cpmGraph = [
      {
        true_cpm: null,
        gradient_cpm: null,
        abtree_cpm: null,
        random_forest_cpm: null,
        day: null
      },
    ];

    vm.fillrateGraph = [
      {
        true_fillrate: null,
        gradient_fillrate: null,
        abtree_fillrate: null,
        random_forest_fillrate: null,
        day: null
      },
    ];

    vm.profitGraph = [
      {
        true_profit: null,
        gradient_profit: null,
        abtree_cpm: null,
        random_forest_cpm: null,
        day: null
      }
    ];

    if ($localStorage.campaign == null) {
      $state.go('home.main');
    }

    AutomaticCpm.getList(Campaign.id).then(function (res) {
      if (res == undefined) {
        return;
      }

      vm.selectMethod = res.choice_list ? res.choice_list : null;
      vm.cpmGraph = res.cpm_graph;
      vm.fillrateGraph = res.fillrate_graph;
      vm.profitGraph = res.profit_graph;
    });

    //region DATE PIKER
    /** DATE PIKER **/
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
      $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
      $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
      vm.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
      vm.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
    } else {
      if ($localStorage.dataStart == null || $localStorage.dataEnd == null) {
        $localStorage.SelectedTime = 0;
        $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
        $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
        vm.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
        vm.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
      } else {
        vm.dataStart = $localStorage.dataStart;
        vm.dataEnd = $localStorage.dataEnd;
      }
    }

    var products = [
      {
        ID: 0,
        Name: LC('MAIN.DATE_PICKER.YESTERDAY'),
        dataStart: $window.moment({ hour: '00' }).subtract(1, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix()
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(3, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(7, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(14, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(21, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
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
        dataStart: $window.moment({ hour: '00' }).subtract(90, 'day').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 8,
        Name: LC('MAIN.DATE_PICKER.ALL_TIME'),
        dataStart: 0,
        dataEnd: $window.moment().unix()
      }
    ];

    // endregion

    vm.UI = {
      chartCPM: {
        series: [
          { valueField: 'true_cpm', axis: 'true_cpm', name: 'CPM True' },
          { valueField: 'gradient_cpm', name: 'Gradient CPM' },
          { valueField: 'abtree_cpm', name: 'Adaboost tree CPM' },
          { valueField: 'random_forest_cpm', name: 'Random forest CPM' },
        ],
        bindingOptions: {
          dataSource: 'acpmc.cpmGraph'
        },
        commonSeriesSettings: {
          argumentField: 'date',
          type: 'Line',
          point: {
            size: 6,
            hoverStyle: {
              border: {
                visible: true,
                width: 2
              },
              size: 5
            }
          }
        },
        tooltip: {
          enabled: true,
          customizeTooltip: function (arg) {
            return {
              text: arg.valueText
            };
          },
        },
        crosshair: {
          enabled: true,
          color: 'deepskyblue',
          visible: true,
          horizontalLine: {
            label: {
              visible: true,
              customizeText: function (arg) {
                return this.value;
              },
            },
          },
        },
        commonAxisSettings: {
          valueMarginsEnabled: true,
        },
        margin: {
          bottom: 20
        },
        argumentAxis: {
          discreteAxisDivisionMode: 'crossLabels',
          grid: {
            visible: true
          }
        },
        valueAxis: [
          { name: 'true_cpm' },
          { name: 'gradient_cpm' },
          { name: 'abtree_cpm' },
          { name: 'random_forest_cpm' }
        ],
        legend: {
          verticalAlignment: 'bottom',
          horizontalAlignment: 'center',
          itemTextPosition: 'bottom'
        },
      },
      chartFillRate: {
        series: [
          { valueField: 'true_fillrate', name: 'True fill rate' },
          { valueField: 'gradient_fillrate', name: 'Gradient fill rate' },
          { valueField: 'abtree_fillrate', name: 'Abtree fill rate' },
          { valueField: 'random_forest_fillrate', name: 'Random forest fill rate' },
        ],
        bindingOptions: {
          dataSource: 'acpmc.fillrateGraph'
        },
        commonSeriesSettings: {
          argumentField: 'date',
          type: 'Line',
          point: {
            size: 6,
            hoverStyle: {
              border: {
                visible: true,
                width: 2
              },
              size: 5
            }
          }
        },
        tooltip: {
          enabled: true,
          customizeTooltip: function (arg) {
            return {
              text: arg.valueText
            };
          },
        },
        crosshair: {
          enabled: true,
          color: 'deepskyblue',
          visible: true,
          horizontalLine: {
            label: {
              visible: true,
              customizeText: function (arg) {
                return this.value;
              },
            },
          },
          verticalLine: {
            label: {
              visible: true
            }
          }
        },
        commonAxisSettings: {
          valueMarginsEnabled: true,
        },
        margin: {
          bottom: 20
        },
        argumentAxis: {
          discreteAxisDivisionMode: 'crossLabels',
          grid: {
            visible: true
          }
        },
        valueAxis: [
          { name: 'true_fillrate', position: 'left' },
          { name: 'gradient_fillrate', position: 'left' },
          { name: 'abtree_fillrate', position: 'left' },
          { name: 'random_forest_fillrate', position: 'left' },
        ],
        legend: {
          verticalAlignment: 'bottom',
          horizontalAlignment: 'center',
          itemTextPosition: 'bottom'
        },
      },
      chartProfit: {
        series: [
          { valueField: 'true_profit', name: 'True profit' },
          { valueField: 'gradient_profit', name: 'Gradient profit' },
          { valueField: 'abtree_cpm', name: 'Abtree CPM' },
          { valueField: 'random_forest_cpm', name: 'Random forest CPM' },
        ],
        bindingOptions: {
          dataSource: 'acpmc.profitGraph'
        },
        commonSeriesSettings: {
          argumentField: 'date',
          type: 'Line',
          point: {
            size: 6,
            hoverStyle: {
              border: {
                visible: true,
                width: 2
              },
              size: 5
            }
          }
        },
        tooltip: {
          enabled: true,
          customizeTooltip: function (arg) {
            return {
              text: arg.valueText
            };
          },
        },
        crosshair: {
          enabled: true,
          color: 'deepskyblue',
          visible: true,
          horizontalLine: {
            label: {
              visible: true,
              customizeText: function (arg) {
                return this.value;
              },
            },
          },
          verticalLine: {
            label: {
              visible: true
            }
          }
        },
        commonAxisSettings: {
          valueMarginsEnabled: true,
        },
        margin: {
          bottom: 20
        },
        argumentAxis: {
          discreteAxisDivisionMode: 'crossLabels',
          grid: {
            visible: true
          }
        },
        valueAxis: [
          {
            constantLines: [
              {
                value: 0,
                color: 'black',
                width: 1
              }
            ]
          },
          { name: 'true_profit', position: 'left' },
          { name: 'gradient_profit', position: 'left' },
          { name: 'abtree_cpm', position: 'left' },
          { name: 'random_forest_cpm', position: 'left' },
        ],
        legend: {
          verticalAlignment: 'bottom',
          horizontalAlignment: 'center',
          itemTextPosition: 'bottom'
        },
      },
      loadPanel: {
        shadingColor: 'rgba(0,0,0,0.4)',
        bindingOptions: {
          visible: 'acpmc.loadindicatorVisible'
        },
        showIndicator: true,
        showPane: true,
        shading: true,
        closeOnOutsideClick: false
      },
      send: {
        text: LC('ACPMC.SEND'),
        onClick: function () {
          if ((!selectMethod) || (selectMethod == null)) {
            $window.DevExpress.ui.notify('Select method please', 'warning', 4000);
            return;
          }

          vm.loadindicatorVisible = true;
          return AutomaticCpm.saveMethod($localStorage.advertiser.id, vm.campId, selectMethod)
            .then(function (res) {
            if (res == false) {
              vm.loadindicatorVisible = false;
              return;
            }

            vm.message = 'Save method: ' + res;
            vm.loadindicatorVisible = false;
          });
        }
      },
      choiceList: {
        displayExpr: 'name',
        valueExpr: 'back_name',
        searchEnabled: true,
        bindingOptions: {
          dataSource: 'acpmc.selectMethod'
        },
        onValueChanged: function (res) {
          selectMethod = res.value;
        }
      },
      datePiker: {
        items: products,
        displayExpr: 'Name',
        valueExpr: 'back_name',
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
