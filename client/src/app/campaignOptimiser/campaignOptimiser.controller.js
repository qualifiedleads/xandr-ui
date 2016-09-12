(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('CampaignOptimiserController', CampaignOptimiserController);

  /** @ngInject */
  function CampaignOptimiserController($window, $state, $localStorage, $scope, $translate, Campaign, CampaignOptimiser) {
    var vm = this;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    var LC = $translate.instant;
    vm.object = CampaignOptimiser.campaignTargeting(1,1,1);
    vm.grindIf = 1;

    console.log(vm.content);
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
        dataStart: $window.moment({ hour: '00' }).subtract(1, 'day').unix() ,
        dataEnd: $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix()
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart:  $window.moment({ hour: '00' }).subtract(3, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart:  $window.moment({ hour: '00' }).subtract(7, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart:  $window.moment({ hour: '00' }).subtract(14, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart:  $window.moment({ hour: '00' }).subtract(21, 'day').unix(),
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
    //endregion

    //region MULTIPLE
    vm.selectedItems = [];
    vm.state = '';
/*    vm.selectCell = {
      dataSource: [
        {
          'name': 'White List',
          'state': 'whiteList'
        },
        {
          'name': 'Black List',
          'state': 'blackList'
        },
        {
          'name': 'Suspended',
          'state': 'suspended'
        }
      ],
      disabled: true,
      placeholder: 'Select a state',
      displayExpr: 'name',
      valueExpr: vm.state,
      onSelectionChanged: function () {
        var selectedRows = $window.$('.gridContainerWhite')[0].querySelectorAll('[aria-selected="true"]');
        if (selectedRows[0]) {
          var selectedArr = [];
          for (var i = 0; i < selectedRows.length; i++) {
            selectedArr.push(selectedRows[i].firstChild.innerText);
          }
        }
      }
    };*/

    function headerFilterColumn(source, dataField) {
      return source.dataSource.postProcess = function(data) {
        var list = $window._.uniqBy(data, dataField);
        return list.map(function (item) {
          return {
            text: item[dataField],
            value: item[dataField]
          };
        });
      };
    }
    //endregion

    //region STORE
    vm.gridStore = CampaignOptimiser.getGridCampaignStore(vm.campId, vm.dataStart, vm.dataEnd);
    //endregion

    vm.UI = {
      showGridWhiteList: {
        text: 'Whitelist',
        onClick: function (e) {
          vm.grindIf = 1;
          $scope.$apply();
        }
      },
      showGridBlackList: {
        text: 'Blacklisted',
        onClick: function (e) {
          vm.grindIf = 2;
          $scope.$apply();
        }
      },
      showGridTempSuspendList: {
        text: 'Temp. Suspend',
        onClick: function (e) {
          vm.grindIf = 3;
          $scope.$apply();
        }
      },
      popSuspend: {
        target: ".suspended",
        position: "top",
        width: 300,
        shading: true,
        shadingColor: "rgba(0, 0, 0, 0.5)",
        visible: false
      },
      popRadio: {
        items: ["re-test in", 'Send to "Suspend list" until I get to it'],
        value: "re-test in",
/*        itemTemplate: function(itemData, _, itemElement){
          if (itemData == 're-test in') {
            itemElement
            .parent().addClass('re-test-in')
            .text(itemData)
            .append( "<div class='timeRadio'>Test</div>" );

            $window.$('div.re-test-in').append( "<p>Test</p>" );
     /!*       $window.$('.re-test-in').dxButton({
              text: 'white',
              height: 30,
              width: 89,
              disabled: false,
              onClick: function (e) {

              }
            }).appendTo('div.re-test-in');*!/
          } else {
            itemElement
            .parent().addClass(itemData.toLowerCase())
            .text(itemData);
          }
        },*/
        onValueChanged: function (e) {
          if (e.previousValue != 're-test in') {
/*           var checkbox = e.element.find(".dx-radiobutton-checked")
           var item = $window.$('<div></div>').dxButton({
              text: 'white',
              height: 30,
              width: 89,
              disabled: false,
              onClick: function (e) {

              }
            })
            checkbox.append(item);*/
            //.addClass('white-list').appendTo('div.dx-template-wrapper.dx-item-content');
            //$window.$("#popover4").dxPopover("instance").toggle();
          }
        }
      },
      popRetestRadio: {
        items: ["24hrs", "3 days", "7 days", "Specific date"],

      },
      navCamp: {
        text: LC('CO.CAMPAIGN-HOME'),
        onClick: function () {
          $state.go('home.campaign.details',{"id":vm.campId});
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
      },
      dataGridOptionsCampaign: {
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
          dataSource: 'CO.gridStore'
        },
        paging: {
          pageSize: 10
        },
        remoteOperations: true,
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
            allowEditing: false,
            headerFilter: {
              dataSource: function(source) {
                return headerFilterColumn(source, 'placement');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.NETWORK'),
            dataField: 'NetworkPublisher',
            alignment: 'center',
            dataType: 'string',
            allowEditing: false,
            headerFilter: {
              dataSource: function(source) {
                return headerFilterColumn(source, 'NetworkPublisher');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CONV'),
            dataField: 'conv',
            alignment: 'center',
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'conv');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.IMP'),
            dataField: 'imp',
            dataType: 'number',
            sortOrder: 'desc',
            alignment: 'center',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'imp');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPA') + ' ,$',
            dataField: 'cpa',
            dataType: 'number',
            alignment: 'center',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'cpa');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.COST') + ' ,$',
            dataField: 'cost',
            alignment: 'center',
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'cost');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CLICKS'),
            dataField: 'clicks',
            alignment: 'center',
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'clicks');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPC') + ' ,$',
            dataField: 'cpc',
            alignment: 'center',
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'cpc');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CPM') + ' ,$',
            dataField: 'cpm',
            alignment: 'center',
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'cpm');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CVR') + ' ,%',
            dataField: 'cvr',
            alignment: 'center',
            dataType: 'number',
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'cvr');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.CTR') + ' ,%',
            dataField: 'ctr',
            alignment: 'center',
            dataType: 'number',
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'ctr');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.IMPS_VIEWED'),
            dataField: 'imps_viewed',
            alignment: 'center',
            visible: false,
            width: 80,
            dataType: 'number',

            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'imps_viewed');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_MEASURED_IMPS'),
            dataField: 'view_measured_imps',
            alignment: 'center',
            visible: false,
            width: 100,
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'view_measured_imps');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_MEASUREMENT_RATE') + ' ,%',
            dataField: 'view_measurement_rate',
            alignment: 'center',
            visible: false,
            width: 120,
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'view_measurement_rate');
              }
            }
          },
          {
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_RATE') + ' ,%',
            dataField: 'view_rate',
            alignment: 'center',
            visible: false,
            width: 80,
            dataType: 'number',
            allowEditing: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'view_rate');
              }
            }
          },
          {
            caption: 'State',
            width: 300,
            columnIndex: 16,
            dataField: 'state',
            allowEditing: false,
            headerFilter: {
              dataSource: [ {
                text: "White",
                value: ["white"]
              }, {
                text: "Black",
                value: ["black"]
              }, {
                text: "Suspended",
                value: ["suspend"]
              }]
            },
            cellTemplate: function (container, options) {
              $window.$("<div />").dxButton({
                text: 'white',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  CampaignOptimiser.editCampaignDomains(vm.campId,options.data.placement,'white')
                  .then(function (res) {
                    return res;
                  })
                  .catch(function (err) {
                    return err;
                  });
                  var parentWhiteBtn = e.element[0].parentNode;
                  if (parentWhiteBtn.classList.contains('active-white')) {
                    parentWhiteBtn.classList.remove('active-white');
                    parentWhiteBtn.classList.add('unactive-white');
                    options.data.state.whiteList = 'false';
                  } else if (!parentWhiteBtn.classList.contains('active-white')) {
                    parentWhiteBtn.classList.remove('unactive-white');
                    parentWhiteBtn.classList.add('active-white');
                    options.data.state.whiteList = 'true';
                    options.data.state.suspended = 'false';
                    options.data.state.blackList = 'false';
                    parentWhiteBtn.classList.remove('active-black');
                    parentWhiteBtn.classList.remove('active-suspended');
                  }

                }
              }).addClass('white-list').appendTo(container);

              $window.$("<div />").dxButton({
                text: 'black',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  CampaignOptimiser.editCampaignDomains(vm.campId,options.data.placement,'black')
                  .then(function (res) {
                    return res;
                  })
                  .catch(function (err) {
                    return err;
                  });
                  var parentWhiteBtn = e.element[0].parentNode;
                  if (parentWhiteBtn.classList.contains('active-black')) {
                    parentWhiteBtn.classList.remove('active-black');
                    parentWhiteBtn.classList.add('unactive-black');
                    options.data.state.blackList = 'false';
                  } else if (!parentWhiteBtn.classList.contains('active-black')) {
                    parentWhiteBtn.classList.remove('unactive-black');
                    parentWhiteBtn.classList.add('active-black');
                    options.data.state.blackList = 'true';
                    options.data.state.suspended = 'false';
                    options.data.state.whiteList = 'false';
                    parentWhiteBtn.classList.remove('active-white');
                    parentWhiteBtn.classList.remove('active-suspended');
                  }

                }
              }).addClass('black-list').appendTo(container);

              $window.$("<div />").dxButton({
                text: 'suspend',
                height: 30,
                width: 95,
                disabled: false,
                onClick: function (e) {
/*                  CampaignOptimiser.editCampaignDomains(vm.campId,options.data.placement,'suspend')
                  .then(function (res) {
                    return res;
                  })
                  .catch(function (err) {
                    return err;
                  });
                  var parentWhiteBtn = e.element[0].parentNode;
                  if (parentWhiteBtn.classList.contains('active-suspended')) {
                    parentWhiteBtn.classList.remove('active-suspended');
                    parentWhiteBtn.classList.add('unactive-suspended');
                    options.data.state.suspended = 'false';
                  } else if (!parentWhiteBtn.classList.contains('active-suspended')) {
                    parentWhiteBtn.classList.remove('unactive-suspended');
                    parentWhiteBtn.classList.add('active-suspended');
                    options.data.state.suspended = 'true';
                    options.data.state.whiteList = 'false';
                    options.data.state.blackList = 'false';
                    parentWhiteBtn.classList.remove('active-white');
                    parentWhiteBtn.classList.remove('active-black');

                  }*/

                  $window.$("#popover4").dxPopover("instance").toggle();


                }
              }).addClass('suspended').appendTo(container);
            }
          }
        ],
        summary: {
          totalItems: [
            {
              column: "placement",
              summaryType: "count",
              customizeText: function (data) {
                data.valueText = 'Count: ' + vm.dataGridOptionsMultipleFunc.totalCount();
                return data.valueText;
              }
            },
            {
              column: "conv",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'Conv: ' + CampaignOptimiser.totalSummary.conv;
                return data.valueText;
              }
            },
            {
              column: "imp",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'Imp: ' + CampaignOptimiser.totalSummary.imp;
                return data.valueText;
              }
            },
            {
              column: "cpa",
              summaryType: "sum",
              valueFormat: "currency",
              customizeText: function (data) {
                data.valueText = 'CPA: $' + CampaignOptimiser.totalSummary.cpa.toFixed(4);
                return data.valueText;
              }
            },
            {
              column: "cost",
              summaryType: "sum",
              valueFormat: "currency",
              customizeText: function (data) {
                data.valueText = 'Cost: $' + CampaignOptimiser.totalSummary.cost.toFixed(2);
                return data.valueText;
              }
            },
            {
              column: "clicks",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'Clicks: ' + CampaignOptimiser.totalSummary.clicks;
                return data.valueText;
              }
            },
            {
              column: "cpc",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'CPC: $' + CampaignOptimiser.totalSummary.cpc.toFixed(4);
                return data.valueText;
              }
            },
            {
              column: "cpm",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'CPM: $' + CampaignOptimiser.totalSummary.cpm.toFixed(4);
                return data.valueText;
              }
            },
            {
              column: "cvr",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'CVR: ' + CampaignOptimiser.totalSummary.cvr.toFixed(4);
                return data.valueText;
              }
            },
            {
              column: "ctr",
              summaryType: "sum",
              customizeText: function (data) {
                data.valueText = 'CTR: ' + CampaignOptimiser.totalSummary.ctr.toFixed(4);
                return data.valueText;
              }
            }
          ]
        },
        columnChooser: {
          enabled: true,
          height: 180,
          width: 400,
          emptyPanelText: 'A place to hide the columns'
        },
        selection: {
          mode: 'multiple',
          allowSelectAll: false,
          showCheckBoxesMode: 'always'
        },
        onInitialized: function (data) {
          vm.dataGridOptionsMultipleFunc = data.component;
          vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 9;
          vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].width = 35;
        },
        onRowPrepared: function (data) {
          vm.objectData = data;
          if (vm.objectData.rowType == 'data') {
            var allRowBtns = data.rowElement[0].childNodes[11];
            var state = data.data.state;
            if (state.whiteList == "true") {
              allRowBtns.classList.add('active-white');
            }
            if (state.blackList == "true") {
              allRowBtns.classList.add('active-black');
            }
            if (state.suspended == "true") {
              allRowBtns.classList.add('active-suspended');
            }
          }
        },
        onEditorPreparing: function (info) {
          if ((info.parentType == 'filterRow') && (info.caption=='State')) {
            info.editorElement.dxSelectBox({
              dataSource: [
                {
                  'name': 'White List',
                  'state': 'white'
                },
                {
                  'name': 'Black List',
                  'state': 'black'
                },
                {
                  'name': 'Suspended',
                  'state': 'suspend'
                }
              ],
              placeholder: 'Select a state',
              displayExpr: 'name',
              valueExpr: vm.state,
              onSelectionChanged: function (e) {
                var selectedRows = $window.$('.gridContainerWhite')[0].querySelectorAll('[aria-selected="true"]');
                if (selectedRows[0]) {
                  var selectedArr = [];
                  for (var i = 0; i < selectedRows.length; i++) {
                    selectedArr.push(selectedRows[i].firstChild.innerText);
                  }
                  if (selectedArr != '[]'){
                    CampaignOptimiser.editCampaignDomains(vm.campId, selectedArr, e.selectedItem.state).then(function (res) {
                      $('.gridContainerWhite').dxDataGrid('instance').refresh();
                    }).catch(function (err) {
                      $('.gridContainerWhite').dxDataGrid('instance').refresh();
                    });
                  }
                } else {
                  console.log('поп овер на невыбраные селекты');
                }
              }
            });
            info.cancel = true;
          }
        },
        onSelectionChanged: function (data) {
          vm.selectedItems = data.selectedRowsData;
          vm.disabled = !vm.selectedItems.length;
        }
      }
    };














  }
})();
