(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CampaignOptimiserController', CampaignOptimiserController);

  /** @ngInject */
  function CampaignOptimiserController($window, $state, $localStorage, $scope, $translate, $compile, Campaign, CampaignOptimiser) {
    var vm = this;
    var LC = $translate.instant;
    var dataSuspend = null;
    var tempSespendRow = {};
    var ruleSuspend = false;
    var ruleTimePopUp = '';
    var ruleIndexPopUp = '';

    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.object = CampaignOptimiser.campaignTargeting(1, 1, 1);
    vm.popUpIf = false;
    vm.arrayDiagram = [];

    vm.saveRules = saveRules;
    vm.popUpHide = popUpHide;
    vm.checkTime = checkTime;

    function popUpHide () {
      vm.popUpIf = false;
    }


    //region Rules

    function checkTime(index, rules) { //CO.checkTime(Index)
      if (rules.then == 'Suspend for review') {
        ruleSuspend = true;
        ruleIndexPopUp = index;
        vm.confirmPopup.option('visible', true);
      } else {
        delete rules.time;
        delete rules.timeString;
      }
    }

    function saveRules() {
      CampaignOptimiser.saveRules(Campaign.id, vm.rulesArray);
    }

    CampaignOptimiser
      .getRules(Campaign.id)
      .then(function (rule) {
        if (rule){
          vm.rulesArray = rule;
        }

      });

    vm.addField = function (rule) {
      if (rule.$parent.$parent.$parent.$parent.rule) {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.$parent.$parent.$parent.rule.push(
          {"id_logic": "NewRule" + newItemNo, "type": "logic", "logicOrAnd": true},
          {"id_rule": "NewRule" + newItemNo,
            "type": "condition",
            "target": "Placement/App",
            "payment": "CPA",
            "compare": ">",
            "value": 0
          }
        );

      } else {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.$parent.rules.if.push(
          {"id_logic": "NewRule" + newItemNo, "type": "logic", "logicOrAnd": true},
          {"id_rule": "NewRule" + newItemNo,
            "type": "condition",
            "target": "Placement/App",
            "payment": "CPA",
            "compare": ">",
            "value": 0
          }
        );
      }
    };

    vm.addGroup = function (rule, ind) {
      if (rule.$parent.$parent.$parent.rule) {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.$parent.$parent.rule.push({
            "id_logic": "NewRule" + newItemNo,
            "type": "logic",
            "logicOrAnd": true
          },
          [
            {
              id_rule: 'NewGroup' + newItemNo,
              "type": "condition",
              "target": "Placement/App",
              "payment": "CPA",
              "compare": ">",
              "value": 0
            }
          ]
        );
      } else {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.rules.if.push({"id_logic": "NewRule" + newItemNo, "type": "logic", "logicOrAnd": true},
          [
            {
              id_rule: 'NewGroup' + newItemNo,
              "type": "condition",
              "target": "Placement/App",
              "payment": "CPA",
              "compare": ">",
              "value": 0
            }
          ]
        );
      }
    };

    vm.addNewRule = function () {
      var newItemNo = vm.rulesArray.length + 1;
      vm.rulesArray.push(
        {
          "id": "rule" + newItemNo,
          "if": [
            {"id_rule": "NewRule" + newItemNo,
              "type": "condition",
              "target": "Placement/App",
              "payment": "CPA",
              "compare": ">",
              "value": 0
            }
          ],
          "then": "Blacklist"
        }
      );
    };

    vm.deleteRule = function (ind) {
      vm.rulesArray.splice(ind, 1);
    };

    vm.deleteFilds = function (rule, ind) {
      if (rule.$parent.$parent.$parent.$parent.rule) {
        rule.$parent.$parent.$parent.$parent.rule.splice(ind, 2);
      } else {
        rule.$parent.$parent.rules.if.splice(ind, 2);
      }
    };

    vm.typeOfLogic = function (rule) {
      if (rule.type === 'logic') {
        return true;
      } else {
        return false;
      }
    };

    vm.typeOfThen = function (rules) {
      if (rules.then === 'Blacklist') {
        return true;
      } else {
        return false;
      }
    };

    vm.typeOfObject = function (rule) {
      if (rule.type == 'condition') {
        return true;
      } else {
        return false;
      }
    };

    vm.typeOfArray = function (rule) {
      if (Array.isArray(rule) == true) {
        return true;
      } else {
        return false;
      }
    };
    //endregion

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

    //region MULTIPLE
    vm.selectedItems = [];
    vm.state = '';


    function headerFilterColumn(source, dataField) {
      return source.dataSource.postProcess = function (data) {
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
      dateFormatPop: {
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
        onValueChanged: function (e) {
          var radioGroupSend = $('#radioGroupSend')
            .dxRadioGroup('instance');
          if (!e.value) return;
          radioGroupSend.option('value', false);

          if (e.value == LC('CO.SPECIFIC-DATE')) {
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
        onValueChanged: function (e) {
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
        height: 300
      },
      confirmPopupOk: {
        width: 110,
        text: 'OK',
        disabled: false,
        onClick: function () {
          if (ruleSuspend == true) {
            var radioGroupMain = $('#radioGroupMain').dxRadioGroup('instance');
            var radioGroupSend = $('#radioGroupSend').dxRadioGroup('instance');

            if (radioGroupMain._options.value !== false) {
              if (radioGroupMain._options.value == LC('CO.24-HRS')) {
                ruleTimePopUp = $window.moment().add(1, 'day').unix();
              }

              if (radioGroupMain._options.value == LC('CO.3-DAYS')) {
                ruleTimePopUp = $window.moment().add(3, 'day').unix();
              }

              if (radioGroupMain._options.value == LC('CO.7-DAYS')) {
                ruleTimePopUp = $window.moment().add(7, 'day').unix();
              }

            }

            if (radioGroupSend._options.value !== false) {
              ruleTimePopUp = "unlimited";
            }

            if (dataSuspend !== null) {
              ruleTimePopUp = $window.moment(dataSuspend).unix();
            }

            if ((radioGroupSend._options.value == null) && (radioGroupMain._options.value == LC('CO.24-HRS'))) {
              ruleTimePopUp = $window.moment().add(1, 'day').unix();
            }

            vm.rulesArray[ruleIndexPopUp].time = ruleTimePopUp;
            vm.rulesArray[ruleIndexPopUp].timeString = ruleTimePopUp;

            ruleSuspend = false;
            vm.confirmPopupVisible = false;
            vm.confirmPopup.option('visible', false);
            $scope.$apply();
            return 0
          }
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

          if ((radioGroupSend._options.value == null) && (radioGroupMain._options.value == LC('CO.24-HRS'))) {
            suspendPlacement = $window.moment().add(1, 'day').unix();
          }

          for (var i =0; i<tempSespendRow.placement.length; i++) {
            var w = $window.$('div.state-white'+ tempSespendRow.placement[i]);
            var b = $window.$('div.state-black'+ tempSespendRow.placement[i]);
            var s = $window.$('div.state-suspended'+ tempSespendRow.placement[i]);
            w.dxButton('instance').option('disabled',true);
            b.dxButton('instance').option('disabled',true);
            s.dxButton('instance').option('disabled',true);
            w.removeClass('active');
            b.removeClass('active');
            s.removeClass('active');
          }
          CampaignOptimiser.editCampaignDomains(vm.campId, tempSespendRow.placement, 1, suspendPlacement)
            .then(function () {
              for (var i =0; i<tempSespendRow.placement.length; i++) {
                var b = $window.$('div.state-black'+ tempSespendRow.placement[i]);
                var w =$window.$('div.state-white'+ tempSespendRow.placement[i]);
                var s = $window.$('div.state-suspended'+ tempSespendRow.placement[i]);
                w.dxButton('instance').option('disabled',false);
                b.dxButton('instance').option('disabled',false);
                s.dxButton('instance').option('disabled',false);
                s.addClass('active');
              }
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
          /*          tempSespendRow = null;
           dataSuspend = null;*/
          //vm.confirmPopupVisible = false;
          vm.confirmPopup.option('visible', false);
          $scope.$apply();
        }
      },
      navCamp: {
        text: LC('CO.CAMPAIGN-HOME'),
        onClick: function () {
          $state.go('home.campaign.details', {"id": vm.campId});
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
              dataSource: function (source) {
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
              dataSource: function (source) {
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
            caption: LC('CAMP.CAMPAIGN.COLUMNS.VIEW_MEASURED_IMPS'),
            dataField: 'view_measured_imps',
            alignment: 'center',
            visible: false,
            width: 100,
            dataType: 'number',
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
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'view_rate');
              }
            }
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
                /*                var tpl = $compile(
                 '<div class="analiticCO">'+
                 '</div>;')( $scope );
                 tpl.appendTo(container);*/
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
                  '<div class="diagramCO" ng-click="CO.showAllDiagram(' + options.data.placement + ')">' +
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
                    CampaignOptimiser.decisionML(vm.campId, options.data.placement, true)
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
                    CampaignOptimiser.decisionML(vm.campId, options.data.placement, false)
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
                  CampaignOptimiser.showAllMLDiagram(vm.campId, item)
                    .then(function (res) {
                      vm.arraytoPopup = res;
                    });
                };
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
              dataSource: [{
                text: "White",
                value: ["state", "=", 4]
              }, {
                text: "Black",
                value: ["state", "=", 2]
              }, {
                text: "Suspended",
                value: ["state", "=", 1]
              }]
            },
            cellTemplate: function (container, options) {
              var white = $window.$("<div />").dxButton({
                text: 'white',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  var w = $window.$('div.state-white'+ options.data.placement);
                  var b = $window.$('div.state-black'+ options.data.placement);
                  var s = $window.$('div.state-suspended'+ options.data.placement);
                  w.dxButton('instance').option('disabled',true);
                  b.dxButton('instance').option('disabled',true);
                  s.dxButton('instance').option('disabled',true);
                  w.removeClass('active');
                  b.removeClass('active');
                  s.removeClass('active');
                  CampaignOptimiser.editCampaignDomains(vm.campId, [options.data.placement], 4)
                    .then(function (res) {
                      w.dxButton('instance').option('disabled',false);
                      b.dxButton('instance').option('disabled',false);
                      s.dxButton('instance').option('disabled',false);
                      w.addClass('active');
                      return res;
                    })
                    .catch(function (err) {
                      return err;
                    });
                }
              });

              if (options.data.state.whiteList == 4) {
                white.addClass('state-white'+ options.data.placement).addClass('active').appendTo(container);
              } else {
                white.addClass('state-white'+ options.data.placement).appendTo(container);
              }


              var black = $window.$("<div />").dxButton({
                text: 'black',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  var w = $window.$('div.state-white'+ options.data.placement);
                  var b = $window.$('div.state-black'+ options.data.placement);
                  var s = $window.$('div.state-suspended'+ options.data.placement);
                  w.dxButton('instance').option('disabled',true);
                  b.dxButton('instance').option('disabled',true);
                  s.dxButton('instance').option('disabled',true);
                  w.removeClass('active');
                  b.removeClass('active');
                  s.removeClass('active');
                  CampaignOptimiser.editCampaignDomains(vm.campId, [options.data.placement], 2)
                    .then(function (res) {
                      w.dxButton('instance').option('disabled',false);
                      b.dxButton('instance').option('disabled',false);
                      s.dxButton('instance').option('disabled',false);
                      b.addClass('active');
                      return res;
                    })
                    .catch(function (err) {
                      return err;
                    });
                }
              });

              if (options.data.state.blackList == 2) {
                black.addClass('state-black'+ options.data.placement).addClass('active').appendTo(container);
              } else {
                black.addClass('state-black'+ options.data.placement).appendTo(container);
              }


              var suspended = $window.$("<div />").dxButton({
                text: 'suspend',
                height: 30,
                width: 95,
                disabled: false,
                onClick: function () {
                  tempSespendRow.placement = [options.data.placement];
                  tempSespendRow.suspend = 1;
                  vm.confirmPopup.option('visible', true);
                }
              });

              if (options.data.state.suspended == 1) {
                suspended.addClass('state-suspended'+ options.data.placement).addClass('active').appendTo(container);
              } else {
                suspended.addClass('state-suspended'+ options.data.placement).appendTo(container);
              }

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
        onEditorPreparing: function (info) {
          if ((info.parentType == 'filterRow') && (info.caption == 'State')) {
            info.editorElement.dxSelectBox({
              dataSource: [
                {
                  'name': 'White List',
                  'state': 4
                },
                {
                  'name': 'Black List',
                  'state': 2
                },
                {
                  'name': 'Suspended',
                  'state': 1
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
                  if (e.selectedItem.state == 1) {
                    if (selectedArr != '[]') {
                      tempSespendRow.placement = selectedArr;
                      tempSespendRow.suspend = 'suspend';
                      vm.confirmPopupVisible = true;
                      vm.confirmPopup.option('visible', true);
                    }
                  } else {
                    if (selectedArr != '[]') {
                      for (var i =0; i<selectedArr.length; i++) {
                        var w = $window.$('div.state-white'+ selectedArr[i]);
                        var b = $window.$('div.state-black'+ selectedArr[i]);
                        var s = $window.$('div.state-suspended'+ selectedArr[i]);
                        w.dxButton('instance').option('disabled',true);
                        b.dxButton('instance').option('disabled',true);
                        s.dxButton('instance').option('disabled',true);
                        w.removeClass('active');
                        b.removeClass('active');
                        s.removeClass('active');
                      }

                      CampaignOptimiser.editCampaignDomains(vm.campId, selectedArr, e.selectedItem.state).then(function (res) {
                        for (var i =0; i<selectedArr.length; i++) {
                          var b = $window.$('div.state-black'+ selectedArr[i]);
                          var w =$window.$('div.state-white'+ selectedArr[i]);
                          var s = $window.$('div.state-suspended'+ selectedArr[i]);
                          w.dxButton('instance').option('disabled',false);
                          b.dxButton('instance').option('disabled',false);
                          s.dxButton('instance').option('disabled',false);
                          if (e.selectedItem.state == 2) {
                            b.addClass('active');
                          }
                          if (e.selectedItem.state == 4) {
                            w.addClass('active');
                          }
                        }
                        $('.gridContainerWhite').dxDataGrid('instance').refresh();
                      }).catch(function () {
                        $('.gridContainerWhite').dxDataGrid('instance').refresh();
                      });
                    }
                  }
                } else {
                  $window.DevExpress.ui.notify(LC('CO.NO-ITEMS-CHOSEN'), "warning", 4000);
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
