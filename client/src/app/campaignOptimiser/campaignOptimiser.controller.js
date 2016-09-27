(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('CampaignOptimiserController', CampaignOptimiserController);

  /** @ngInject */
  function CampaignOptimiserController($window, $state, $localStorage, $scope, $translate, $compile, Campaign, CampaignOptimiser) {
    var vm = this;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    var LC = $translate.instant;
    vm.object = CampaignOptimiser.campaignTargeting(1,1,1);
    vm.grindIf = 1;
    vm.popUpIf = false;
    var dataSuspend = null;
    var tempSespendRow = {};
    vm.confirmAllDiagramPopupVisible = false;


    vm.bad = 0.6;
    vm.good = 0.4;
    vm.badOpasity = 1;
    vm.goodOpasity = 1;
    vm.k = +(( vm.bad*100)/( vm.bad +  vm.good));
    if (((vm.k/100 <=0.5)) && (((vm.k/100) >0.45)) || ((((100-vm.k)/100)<=0.5) && (((100-vm.k)/100)>0.45 ))) { vm.badOpasity = 0.03; vm.goodOpasity = 0.03;}
    if ((vm.k/100 <0.44 && vm.k/100 >0.4)  || (((100-vm.k)/100)<0.44 && ((100-vm.k)/100)>0.4 )) { vm.badOpasity = 0.09; vm.goodOpasity = 0.09;}
    if ((vm.k/100 <0.4 && vm.k/100 >0.3)   || (((100-vm.k)/100)<0.4 && ((100-vm.k)/100)>0.3 )) { vm.badOpasity = 0.2; vm.goodOpasity = 0.2;}
    if ((vm.k/100 <0.3 && vm.k/100 >0.2)   || (((100-vm.k)/100)<0.3 && ((100-vm.k)/100)>0.2 )) { vm.badOpasity = 0.5; vm.goodOpasity = 0.5;}
    if ((vm.k/100 <0.2 && vm.k/100 >0.1)   || (((100-vm.k)/100)<0.2 && ((100-vm.k)/100)>0.1 )) { vm.badOpasity = 0.7; vm.goodOpasity = 0.7;}
    if ((vm.k/100 <0.1 && vm.k/100 >0)     || (((100-vm.k)/100)<0.1 && ((100-vm.k)/100)>0 )) { vm.badOpasity = 1.0; vm.goodOpasity = 1.0;}
    vm.goodDiagram = (100-vm.k)+'%';
    vm.badDiagram = vm.k+'%';

    vm.popUpHide = function () {
      vm.popUpIf = false;
    };


    /*   var array = [{
      "if": {
        [{
          "target": "placement",
          "compare": "<",
          "cpa": "2"
        }]
      },
      "then": "black"
    }];
*/

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

    var startDate = new Date(1981, 3, 27),
      now = new Date();

    vm.UI = {
      showGridWhiteList: {
        text: LC('CO.WHITELIST'),
        onClick: function (e) {
          vm.grindIf = 1;
          $scope.$apply();
        }
      },
      showGridBlackList: {
        text: LC('CO.BLACKLISTED'),
        onClick: function (e) {
          vm.grindIf = 2;
          $scope.$apply();
        }
      },
      showGridTempSuspendList: {
        text: LC('CO.TEMP-SUSPEND'),
        onClick: function (e) {
          vm.grindIf = 3;
          $scope.$apply();
        }
      },
      dateFormatPop :{
        disabled: true,
        type: "date",
        value: now,
        onValueChanged: function (e) {
          dataSuspend = e.value;
        }
      },
      radioGroupMain: {
        items: [LC('CO.24-HRS'), LC('CO.3-DAYS'), LC('CO.7-DAYS'), LC('CO.SPECIFIC-DATE')],
        value: LC('CO.24-HRS'),
        onValueChanged: function(e) {
          var radioGroupSend = $('#radioGroupSend')
          .dxRadioGroup('instance');
          if (!e.value) return;
          radioGroupSend.option('value', false);

          if (e.value ==  LC('CO.SPECIFIC-DATE')) {
            //e;
            var datePik = $('#dateFormatPop')
            .dxDateBox('instance');
            datePik.option('disabled', false);
          } else {
            var datePik = $('#dateFormatPop')
            .dxDateBox('instance');
            datePik.option('disabled', true);
            dataSuspend = null;
          }
        }
      },
      radioGroupSend: {
        items: [LC('CO.SEND-TO-SUSPEND-LIST')],
        onValueChanged: function(e) {
          dataSuspend = null;
          var datePik = $('#dateFormatPop')
          .dxDateBox('instance');
          datePik.option('disabled', true);

          var radioGroupMain = $('#radioGroupMain')
          .dxRadioGroup('instance');
          if (!e.value) return;
          radioGroupMain.option('value', false);
        }
      },
      confirmPopup: {
        onInitialized: function (data) {
          vm.confirmPopup = data.component;
        },
        bindingOptions: {
          visible: 'crc.confirmPopupVisible'
        },
        showTitle: false,
        width: 320,
        height: 280
      },
      confirmPopupOk: {
        width: 110,
        text: 'OK',
        disabled: false,
        onClick: function () {
          var suspendPlacement;
          var radioGroupMain = $('#radioGroupMain').dxRadioGroup('instance');
          var radioGroupSend = $('#radioGroupSend').dxRadioGroup('instance');

          if (radioGroupMain._options.value !== false) {
            if (radioGroupMain._options.value == LC('CO.24-HRS')) {
              suspendPlacement = $window.moment().add(1, 'day').unix();
            }

            if (radioGroupMain._options.value == LC('CO.3-DAYS')) {
              suspendPlacement = $window.moment().add(3, 'day').unix();
            }

            if (radioGroupMain._options.value == LC('CO.7-DAYS')) {
              suspendPlacement = $window.moment().add(7, 'day').unix();
            }

          }

          if (radioGroupSend._options.value !== false) {
            suspendPlacement = "unlimited";
          }

          if (dataSuspend !== null) {
            suspendPlacement = $window.moment(dataSuspend).unix();
          }

          if ((radioGroupSend._options.value == null)&&(radioGroupMain._options.value == LC('CO.24-HRS'))) {
            suspendPlacement = $window.moment().add(1, 'day').unix();
          }

          CampaignOptimiser.editCampaignDomains(vm.campId, tempSespendRow.placement, tempSespendRow.suspend, suspendPlacement)
          .then(function () {
            $('.gridContainerWhite').dxDataGrid('instance').refresh();
          }).catch(function () {
            $('.gridContainerWhite').dxDataGrid('instance').refresh();
          });

          vm.confirmPopupVisible = false;
          vm.confirmPopup.option('visible', false);
          $scope.$apply();
        }
      },
      confirmPopupCancel: {
        width: 120,
        text: LC('COMMON.CANCEL'),
        onClick: function () {
          tempSespendRow = null;
          dataSuspend = null;
          vm.confirmPopupVisible = false;
          vm.confirmPopup.option('visible', false);
          $scope.$apply();
        }
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
            allowEditing: false,
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
            allowEditing: false,
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
            caption: 'Analytics',
            width: 210,
            columnIndex: 16,
            dataField: 'analytics',
            allowEditing: false,
            cellTemplate: function (container, options) {
              var bad = options.data.analitics[7].bad;
              var good = options.data.analitics[7].good;
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
              var tpl = $compile(
                '<div class="analiticCO">'+
                '<div class="diagramCO" ng-click="CO.showAllDiagram()">'+
                '<div class="badDiagramCO" style="width:' + badDiagram + ';opacity:' + badOpasity + ';"></div>'+
                '<div class="goodDiagramCO" style="width:' + goodDiagram + ';opacity:'+goodOpasity+';"></div>'+
                '<p class="textBadDiagramCO" >'+bad.toFixed(1)+'('+k.toFixed(1)+'%)</p>'+
                '<p class="textGoodDiagramCO">'+good.toFixed(1)+'(' + (100-k).toFixed(1)+ '%)</p>'+
                '</div>'+
                '<div class="buttonAnaliticCO'+ options.data.placement+'">'+
                '<div class="trueButtonAnaliticCO'+ options.data.placement +'"></div>'+
                '<div class="falseButtonAnaliticCO'+ options.data.placement +'"></div>'+
                '</div>'+
                '</div>;')( $scope );
              tpl.appendTo(container);

              vm.showAllDiagram = function () {
                vm.popUpIf = true;
                vm.arrayDiagram = options.data.analitics;
              };

              var trueButton = $window.$(".trueButtonAnaliticCO"+ options.data.placement).dxButton({
                text: 'True',
                disabled: false,
                onClick: function () {
                  $window.$(".falseButtonAnaliticCO"+ options.data.placement).removeClass('active-white');
                  $window.$(".trueButtonAnaliticCO"+ options.data.placement).addClass('active-white');
                  CampaignOptimiser.decisionML(vm.campId, options.data.placement, true)
                  .then(function (res) {
                    return res;
                  });
                }
              });

              var falseButton = $window.$(".falseButtonAnaliticCO"+ options.data.placement).dxButton({
                text: 'False',
                disabled: false,
                onClick: function () {
                  $window.$(".falseButtonAnaliticCO"+ options.data.placement).addClass('active-white');
                  $window.$(".trueButtonAnaliticCO"+ options.data.placement).removeClass('active-white');
                  CampaignOptimiser.decisionML(vm.campId, options.data.placement, false)
                  .then(function (res) {
                    return res;
                  });
                }
              });

              if (options.data.analitics[7].checked == true) {
                trueButton.addClass('active-white').append();
              } else {
                trueButton.append();
              }

              if (options.data.analitics[7].checked == false) {
                falseButton.addClass('active-white').append();
              } else {
                falseButton.append();
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
                  }

                  tempSespendRow.placement = options.data.placement;
                  tempSespendRow.suspend = 'suspend';

                  //vm.confirmPopupVisible = true;
                  vm.confirmPopup.option('visible', true);
                }
              }).addClass('suspended' + options.data.placement).appendTo(container);

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
            var analitics = data.data.analitics;
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

                  //e;
                  if (e.selectedItem.state == "suspend") {
                    if (selectedArr != '[]') {
                      tempSespendRow.placement = selectedArr;
                      tempSespendRow.suspend = 'suspend';
                      vm.confirmPopupVisible = true;
                      vm.confirmPopup.option('visible', true);
                    }
                  } else {
                    if (selectedArr != '[]'){
                      CampaignOptimiser.editCampaignDomains(vm.campId, selectedArr, e.selectedItem.state).then(function (res) {
                        $('.gridContainerWhite').dxDataGrid('instance').refresh();
                      }).catch(function () {
                        $('.gridContainerWhite').dxDataGrid('instance').refresh();
                      });
                    }
                  }
                } else {
                  $window.DevExpress.ui.notify( LC('CO.NO-ITEMS-CHOSEN'), "warning", 4000);
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
