(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('valuationByExpertController', valuationByExpertController);

  /** @ngInject */
  function valuationByExpertController($window, $state, $localStorage, $scope, $translate, $compile, valuationByExpertS) {
    var vm = this;
    var LC = $translate.instant;
    vm.campId = 13921687;
    vm.arrayDiagram = [];
    vm.popUpIf = false;
    vm.culcReady = false;
    vm.popUpHide = function () {
      vm.popUpIf = false;
    };

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


    //region STORE
    vm.gridStore = valuationByExpertS.getGridCampaignStore(vm.campId, vm.dataStart, vm.dataEnd);
    //endregion

    vm.UI = {
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
      },
      calculateAUC: {
        text: LC('VBE.CALCULATE-AUC'),
        onClick: function () {
          vm.culcReady = true;
          $scope.$apply();
        }
      }
      ,createTestSet: {
        text: LC('VBE.CREATE-TEST-SET'),
        onClick: function () {
         valuationByExpertS._MLRandomTestSet('create').then(function (res) {
            console.log(res);
         });

          $scope.$apply();
        }
      },
      dataGridOptionsExpert: {
        editing: {
          mode: "batch",
          allowUpdating: true
        },
        alignment: 'left',
        headerFilter: {
          visible: true
        },
        filterRow: {
          visible: true,
          applyFilter: "auto"
        },
        bindingOptions: {
          dataSource: 'VBE.gridStore'
        },
        paging: {
          pageSize: 10
        },
        remoteOperations: false,
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
        },
        allowColumnReordering: true,
        allowColumnResizing: true,
        columnAutoWidth: true,
        wordWrapEnabled: true,
        showBorders: true,
        showRowLines: true,
        columns: [
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.PLACEMENT'),
            dataField: 'placement',
            alignment: 'center',
            dataType: 'number',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.NETWORK'),
            dataField: 'NetworkPublisher',
            alignment: 'center',
            dataType: 'string',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CONV'),
            dataField: 'conv',
            alignment: 'center',
            dataType: 'number',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.IMP'),
            dataField: 'imp',
            dataType: 'number',
            sortOrder: 'desc',
            alignment: 'center',
          format:'fixedPoint'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPA') + ' ,$',
            dataField: 'cpa',
            dataType: 'number',
            alignment: 'center',
            format:'currency'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.COST') + ' ,$',
            dataField: 'cost',
            alignment: 'center',
            dataType: 'number',
            format:'currency'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CLICKS'),
            dataField: 'clicks',
            alignment: 'center',
            dataType: 'number',
            allowEditing: false,
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPC') + ' ,$',
            dataField: 'cpc',
            alignment: 'center',
            dataType: 'number',
            format:'currency'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPM') + ' ,$',
            dataField: 'cpm',
            alignment: 'center',
            dataType: 'number',
            format:'currency'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CVR') + ' ,%',
            dataField: 'cvr',
            alignment: 'center',
            dataType: 'number',
            format:'percent'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CTR') + ' ,%',
            dataField: 'ctr',
            alignment: 'center',
            dataType: 'number',
            format:'percent'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.IMPS_VIEWED'),
            dataField: 'imps_viewed',
            alignment: 'center',
            visible: false,
            width: 80,
            dataType: 'number',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_MEASURED_IMPS'),
            dataField: 'view_measured_imps',
            alignment: 'center',
            visible: false,
            width: 100,
            dataType: 'number',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_MEASUREMENT_RATE') + ' ,%',
            dataField: 'view_measurement_rate',
            alignment: 'center',
            visible: false,
            width: 120,
            dataType: 'number',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_RATE') + ' ,%',
            dataField: 'view_rate',
            alignment: 'center',
            visible: false,
            width: 80,
            dataType: 'number',
          },
          {
            caption: 'Prediction 1',
            width: 115,
            columnIndex: 16,
            dataField: 'analytics',
            allowEditing: false,
            cellTemplate: function (container, options) {
              vm.arrayDiagram.push(options.data);
              if (options.data.analitics === null) {
                //                var tpl = $compile(
                // '<div class="analiticCO">'+
               //  '</div>;')( $scope );
              //   tpl.appendTo(container);
              } else {
                var bad = options.data.analitics.bad;
                var good = options.data.analitics.good;
                var badOpasity = options.data.analitics.badOpasity;
                var goodOpasity = options.data.analitics.goodOpasity;
                var k = options.data.analitics.k;
                var goodDiagram = options.data.analitics.goodDiagram;
                var badDiagram = options.data.analitics.badDiagram;
                var tpl = $compile(
                  '<div class="analiticCO">' +
                  '<div class="diagramCO" ng-click="VBE.showAllDiagram(' + options.data.placement + ')">' +
                  '<div class="badDiagramCO" style="width:' + badDiagram + ';opacity:' + badOpasity + ';"></div>' +
                  '<div class="goodDiagramCO" style="width:' + goodDiagram + ';opacity:' + goodOpasity + ';"></div>' +
                  '<p class="textBadDiagramCO" >' + k.toFixed(1) + '%</p>' +
                  '<p class="textGoodDiagramCO">' + (100 - k).toFixed(1) + '%</p>' +
                  '</div>' +
                  '<div class="buttonAnaliticCO' + options.data.placement + '">' +
                  '<div class="trueButtonAnaliticCO' + options.data.placement + '"></div>' +
                  '<div class="falseButtonAnaliticCO' + options.data.placement + '"></div>' +
                  '</div>' +
                  '</div>;')($scope);
                tpl.appendTo(container);

                var trueButton = $window.$(".trueButtonAnaliticCO" + options.data.placement).dxButton({
                  text: 'True',
                  disabled: false,
                  onClick: function () {
                    $window.$(".falseButtonAnaliticCO" + options.data.placement).removeClass('active-white');
                    $window.$(".trueButtonAnaliticCO" + options.data.placement).addClass('active-white');
                    valuationByExpertS.decisionML(vm.campId, options.data.placement, true)
                      .then(function (res) {
                        return res;
                      });
                  }
                });

                var falseButton = $window.$(".falseButtonAnaliticCO" + options.data.placement).dxButton({
                  text: 'False',
                  disabled: false,
                  onClick: function () {
                    $window.$(".falseButtonAnaliticCO" + options.data.placement).addClass('active-white');
                    $window.$(".trueButtonAnaliticCO" + options.data.placement).removeClass('active-white');
                    valuationByExpertS.decisionML(vm.campId, options.data.placement, false)
                      .then(function (res) {
                        return res;
                      });
                  }
                });

                if (options.data.analitics.checked == true) {
                  trueButton.addClass('active-white').append();
                } else {
                  trueButton.append();
                }

                if (options.data.analitics.checked == false) {
                  falseButton.addClass('active-white').append();
                } else {
                  falseButton.append();
                }

                vm.showAllDiagram = function (item) {
                  vm.popUpIf = true;
                  valuationByExpertS.showAllMLDiagram(vm.campId, item)
                    .then(function (res) {
                      vm.arraytoPopup = res;
                    });
                };

              }
            }
          }
        ],
        columnChooser: {
          enabled: true,
          height: 180,
          width: 400,
          emptyPanelText: 'A place to hide the columns'
        },
        onInitialized: function (data) {
          vm.dataGridOptionsMultipleFunc = data.component;
          vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 9;
          vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].width = 35;
        },
        onSelectionChanged: function (data) {
          vm.selectedItems = data.selectedRowsData;
          vm.disabled = !vm.selectedItems.length;
        }
      }
    };
  }
})();
