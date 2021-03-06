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
    vm.chartCoord = [];
    var buttonIndicator, buttonIndicator1;
    vm.selectType = 'kmeans';
    vm.popUpHide = function () {
      vm.popUpIf = false;
    };
    vm.auc = null;
    vm.titlePred = '';

    valuationByExpertS.MLGetAUC(vm.selectType)
      .then(function (res) {
        if (vm.selectType == "log") {
          vm.titlePred = "Logistic regression";
        }
        if (vm.selectType == "kmeans") {
          vm.titlePred = "K-means";
        }
        vm.auc = res.auc;
        vm.chartCoord = res.chartCoord;
        vm.culcReady = true;
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
        template: function(data, container) {
          $("<div class='button-indicator'></div><span class='dx-button-text'>" + data.text + "</span>").appendTo(container);
          buttonIndicator = container.find(".button-indicator").dxLoadIndicator({
            height: 15,
            visible: false
          }).dxLoadIndicator("instance");
        },
        onClick: function (data) {
          data.component.option("text", "Calculate");
          buttonIndicator.option("visible", true);
          valuationByExpertS.MLGetAUC(vm.selectType)
            .then(function (res) {
              if (vm.selectType == "log") {
                vm.titlePred = "Logistic regression";
              }
              if (vm.selectType == "kmeans") {
                vm.titlePred = "K-means";
              }
              vm.auc = res.auc;
              vm.chartCoord = res.chartCoord;
              vm.culcReady = true;
              buttonIndicator.option("visible", false);
              data.component.option("text", "Calculate AUC");
            })
            .catch(function (err) {
              buttonIndicator.option("visible", false);
              data.component.option("text", "Calculate AUC");
            });
        }
      },
      createTestSet: {
        text: LC('VBE.CREATE-TEST-SET'),
        template: function(data, container) {
          $("<div class='button-indicator1'></div><span class='dx-button-text'>" + data.text + "</span>").appendTo(container);
          buttonIndicator1 = container.find(".button-indicator1").dxLoadIndicator({
            height: 10,
            visible: false
          }).dxLoadIndicator("instance");
        },
        onClick: function (data) {
          data.component.option("text", "Create");
          buttonIndicator1.option("visible", true);
          valuationByExpertS._MLRandomTestSet('create')
            .then(function (res) {
              $('.gridContainerWhite').dxDataGrid('instance').refresh();
              buttonIndicator1.option("visible", false);
              data.component.option("text", "Create test set");
            })
            .catch(function (err) {
              buttonIndicator1.option("visible", false);
              data.component.option("text", "Create test set");
            });
        }
      },
      test_type: {
        items: [
          "K-means",
          "Logistic regression"
        ],
        value: "K-means",
        width: 200,
        onValueChanged: function(data) {
          if (data.selectedItem == "Logistic regression") {
            vm.selectType = "log";
          }
          if (data.selectedItem == "K-means") {
            vm.selectType = "kmeans";
          }
        }
      },
      ROC_curve: {
        palette: "violet",
        bindingOptions: {
          dataSource: "VBE.chartCoord"
        },
        commonSeriesSettings: {
          argumentField: "rocFalsePositiveRate",
          type: 'line'
        },
        margin: {
          bottom: 20
        },
        argumentAxis: {
          valueMarginsEnabled: false,
          discreteAxisDivisionMode: "crossLabels",
          grid: {
            visible: true
          },
          title: 'False positive rate'
        },
        size: {
          width: 400,
          height: 400
        },
        series: [
          { valueField: "rocSensetivities", name: "ROC Curve", showInLegend: false },
          { valueField: "diagonal", showInLegend: false, color: 'gray'}
        ],
        valueAxis: {
          title: {
            text: "Sensetivity"
          }
        },
        title: {
          text: "ROC Curve",
          subtitle: {
            text: "(Confidence interval - 95%, Confidence error - 5%)"
          }
        },
        "export": {
          enabled: true
        },
        tooltip: {
          enabled: true,
          customizeTooltip: function (arg) {
            return {
              text: arg.valueText
            };
          }
        }
      },
      dataGridOptionsExpert: {
        editing: {
          mode: "batch"
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
        loadPanel: {
          shadingColor: "rgba(0,0,0,0.4)",
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false,
        },
        remoteOperations: false,
        allowColumnReordering: true,
        allowColumnResizing: true,
        columnAutoWidth: true,
        wordWrapEnabled: true,
        showBorders: true,
        showRowLines: true,
        columns: [
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.PLACEMENT'),
            dataField: 'placement_id',
            alignment: 'center',
            dataType: 'string',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.NETWORK'),
            dataField: 'publisher',
            alignment: 'center',
            dataType: 'string',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.DOMAIN'),
            dataField: 'domain',
            alignment: 'center',
            dataType: 'string',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CONV'),
            dataField: 'total_convs',
            alignment: 'center',
            dataType: 'number',
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.IMP'),
            dataField: 'imps',
            dataType: 'number',
            sortOrder: 'desc',
            alignment: 'center',
            format:'fixedPoint'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.IMPS_VIEWED'),
            dataField: 'imps_viewed',
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
            format:'currency',
            precision:4,
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.COST') + ' ,$',
            dataField: 'sum_cost',
            dataType: 'number',
            alignment: 'center',
            format:'currency',
            precision:4,
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
            precision:4,
            format:'currency'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPM') + ' ,$',
            dataField: 'cpm',
            alignment: 'center',
            dataType: 'number',
            precision:4,
            format:'currency'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CVR') + ' ,%',
            dataField: 'cvr',
            alignment: 'center',
            dataType: 'number',
            precision:2,
            format:'percent'
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CTR') + ' ,%',
            dataField: 'ctr',
            alignment: 'center',
            dataType: 'number',
            precision:2,
            format:'percent'
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
            caption: 'Good/Bad',
            columnIndex: 16,
            dataField: 'goodBad',
            width:125,
            allowEditing: false,
            cellTemplate: function (container, options) {
              var tpl = $compile(
                '<div class="goodBad">' +
                '<div class="button goodButtonAnaliticCO' + options.data.placement_id + '"></div>' +
                '<div class="button badButtonAnaliticCO' + options.data.placement_id + '"></div>' +
                '</div>')($scope);
              tpl.appendTo(container);

              var trueButton = $window.$(".goodButtonAnaliticCO" + options.data.placement_id).dxButton({
                text: 'Good',
                disabled: false,
                onClick: function () {
                  $window.$(".badButtonAnaliticCO" + options.data.placement_id).removeClass('active-white');
                  $window.$(".goodButtonAnaliticCO" + options.data.placement_id).addClass('active-white');
                  valuationByExpertS.goodBadSend(options.data.placement_id, 'good')
                    .then(function (res) {
                      options.data.mark = 'good';
                      return res;
                    });
                }
              });

              var falseButton = $window.$(".badButtonAnaliticCO" + options.data.placement_id).dxButton({
                text: 'Bad',
                disabled: false,
                onClick: function () {
                  $window.$(".badButtonAnaliticCO" + options.data.placement_id).addClass('active-white');
                  $window.$(".goodButtonAnaliticCO" + options.data.placement_id).removeClass('active-white');
                  valuationByExpertS.goodBadSend(options.data.placement_id, 'bad')
                    .then(function (res) {
                      options.data.mark = 'bad';
                      return res;
                    });
                }
              });

              if (options.data.mark == 'good') {
                trueButton.addClass('active-white').append();
              } else {
                trueButton.append();
              }

              if (options.data.mark == 'bad') {
                falseButton.addClass('active-white').append();
              } else {
                falseButton.append();
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
