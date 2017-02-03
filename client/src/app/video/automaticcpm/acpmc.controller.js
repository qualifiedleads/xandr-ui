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
        cpm: null,
        cpmTrue: null,
        day: null
      },
    ];

    vm.fillrateGraph = [
      {
        fill_rate: null,
        day: null
      },
    ];

    vm.profitGraph = [
      {
        profit: null,
        day: null
      }
    ];

    if ($localStorage.campaign == null) {
      $state.go('home.main');
    }

    AutomaticCpm.getList(Campaign.id).then(function (res) {
      vm.selectMethod = res.choice_list;
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
          { valueField: 'cpm', name: 'CPM' },
          { valueField: 'cpmTrue', name: 'CPM True' },
        ],
        bindingOptions: {
          dataSource: 'acpmc.cpmGraph'
        },
        commonSeriesSettings: {
          argumentField: 'day',
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
                if (arg.point.series.name == 'Cost' || arg.point.series.name == 'CPC') {
                  return '$' + this.value;
                }

                if (arg.point.series.name == 'Impressions')  {
                  return this. value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                }

                if ((arg.point.series.name == 'CTR') || (arg.point.series.name == 'CVR')) {
                  return this.value + '%';
                }
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
            name: 'cpm',
            position: 'left'
          },
          {
            name: 'cpmTrue',
            position: 'left'
          },

        ],
        legend: {
          verticalAlignment: 'bottom',
          horizontalAlignment: 'center',
          itemTextPosition: 'bottom'
        },
      },
      chartFillRate: {
        series: [
          { valueField: 'fill_rate', name: 'Fill rate' },
        ],
        bindingOptions: {
          dataSource: 'acpmc.fillrateGraph'
        },
        commonSeriesSettings: {
          argumentField: 'day',
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
                if (arg.point.series.name == 'Cost' || arg.point.series.name == 'CPC') {
                  return '$' + this.value;
                }

                if (arg.point.series.name == 'Impressions')  {
                  return this. value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                }

                if ((arg.point.series.name == 'CTR') || (arg.point.series.name == 'CVR')) {
                  return this.value + '%';
                }
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
            name: 'fill_rate',
            position: 'left'
          },
        ],
        legend: {
          verticalAlignment: 'bottom',
          horizontalAlignment: 'center',
          itemTextPosition: 'bottom'
        },
      },
      chartProfit: {
        series: [
          { valueField: 'profit', name: 'Profit' },
        ],
        bindingOptions: {
          dataSource: 'acpmc.profitGraph'
        },
        commonSeriesSettings: {
          argumentField: 'day',
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
                if (arg.point.series.name == 'Cost' || arg.point.series.name == 'CPC') {
                  return '$' + this.value;
                }

                if (arg.point.series.name == 'Impressions')  {
                  return this. value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                }

                if ((arg.point.series.name == 'CTR') || (arg.point.series.name == 'CVR')) {
                  return this.value + '%';
                }
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
          {
            name: 'profit',
            position: 'left'
          }
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
          return AutomaticCpm.saveMethod(vm.campId, selectMethod).then(function (res) {
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

