(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CampaignMainController', CampaignMainController);

  /** @ngInject */
  function CampaignMainController($window, $state, $localStorage, $translate, $timeout, CampMain, Campaign, $scope, CampaignOptimiser, $rootScope) {
    var vm = this;
    var LC = $translate.instant;
    var dataSuspend = null;
    var tempSespendRow = {};
    vm.Camp = CampMain;
    var now = new Date();
    var oneSuspend = false;
    $rootScope.id = Campaign.id;
    $rootScope.name = Campaign.campaign;
    $rootScope.line_item = Campaign.line_item;
    $rootScope.line_item_id = Campaign.line_item_id;

    vm.checkChart = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';

    if ($localStorage.campaign == null) {
      $state.go('home.main');
    }
    $localStorage.campaign = {
      "id": Campaign.id,
      "name": Campaign.campaign,
      "line_item": Campaign.line_item
    };

    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.line_item = Campaign.line_item;
    vm.line_item_id = Campaign.line_item_id;
    vm.Init = [];

    if ($localStorage.checkCharCamp == null) {
      $localStorage.checkCharCamp = {
        'impression': true,
        'cpa': false,
        'cpc': false,
        'clicks': false,
        'cost': false,
        'conversions': false,
        'ctr': false
      };
    }

    //region DATE PIKER
    /** DATE PIKER - START **/
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
      $localStorage.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
      $localStorage.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
      $localStorage.type = 'yesterday';
      vm.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
      vm.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
      vm.type = 'yesterday';
    } else {
      if ($localStorage.dataStart == undefined || !$localStorage.dataEnd || !$localStorage.type) {
        $localStorage.SelectedTime = 0;
        $localStorage.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
        $localStorage.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
        $localStorage.type = 'yesterday';
        vm.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
        vm.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
        vm.type = 'yesterday';
      } else {
        vm.dataStart = $localStorage.dataStart;
        vm.dataEnd = $localStorage.dataEnd;
        vm.type = $localStorage.type;
      }
    }

    var products = [
      {
        ID: 0,
        Name: LC('MAIN.DATE_PICKER.YESTERDAY'),
        dataStart: $window.moment({hour: '00'}).subtract(1, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'yesterday'
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(3, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_3_days'
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(7, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_7_days'
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(14, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_14_days'
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(21, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_21_days'
      }, {
        ID: 5,
        Name: LC('MAIN.DATE_PICKER.CURRENT_MONTH'),
        dataStart: $window.moment().startOf('month').unix(),
        dataEnd: $window.moment().unix(),
        type: 'cur_month'
      }, {
        ID: 6,
        Name: LC('MAIN.DATE_PICKER.LAST_MONTH'),
        dataStart: $window.moment().subtract(1, 'month').startOf('month').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_month'
      }, {
        ID: 7,
        Name: LC('MAIN.DATE_PICKER.LAST_90_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(90, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_90_days'
      }, {
        ID: 8,
        Name: LC('MAIN.DATE_PICKER.ALL_TIME'),
        dataStart: 0,
        dataEnd: $window.moment().unix(),
        type: 'all'
      }];

    vm.datePiker = {
      items: products,
      displayExpr: 'Name',
      valueExpr: 'ID',
      value: products[$localStorage.SelectedTime].ID,
      onValueChanged: function (e) {
        $localStorage.SelectedTime = e.value;
        $localStorage.dataStart = products[e.value].dataStart;
        $localStorage.dataEnd = products[e.value].dataEnd;
        $localStorage.type = products[e.value].type;

        //$('#gridContainer1').dxDataGrid('instance').refresh();
        //$('#gridContainer2').dxDataGrid('instance').refresh();
        $state.reload();
      }
    };
    //endregion

    vm.optimiser = {
      text: LC('CAMP.GO-OPTIMISER'),
      onClick: function () {
        $state.go('home.campaignOptimiser', {"id": vm.campId});
      }
    };

    //region STORES
    vm.chartStore = CampMain.getChartStore(vm.campId, vm.dataStart, vm.dataEnd, vm.by, vm.type);
    vm.boxPlotStore = CampMain.getBoxPlotStore(vm.campId, vm.dataStart, vm.dataEnd, vm.type);
    vm.gridStore = CampMain.getGridCampaignStore(vm.campId, vm.dataStart, vm.dataEnd, vm.type);
    //endregion

    var wrapper = angular.element($window.document.querySelector("#wrapper"))[0];
    wrapper.classList.remove('hidden-menu');

    //region BIG DIAGRAM
    vm.charIsUpdating = false;
    vm.chartOptionsFirst = {
      onDone: function () {
        var chart = $('#zoomedChartFirst').dxChart('instance');
        if (!vm.charIsUpdating) {
          var update = [];
          var flag = 'left';
          vm.chartOptionsFirst.valueAxis.forEach(function (item, index) {
            var visible = $localStorage.checkCharCamp[item.name];
            update.push({
              name: item.name,
              position: flag,
              label: {
                alignment: 'center',
                customizeText: function () {
                  vm.charIsUpdating = true;
                  var major = chart._valueAxes[index]._majorTicks;
                  var maxMajor = null;
                  if (Array.isArray(major) && maxMajor < major[major.length - 1].value) {
                    maxMajor = major[major.length - 1].value;
                  }
                  if (this.value == maxMajor) {
                    switch (item.name) {
                      case 'impression':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.IMPRESSIONS') + '</span><br>' + this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                      case 'cpa':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + '$' + LC('CAMP.CHECKBOX.CPA') + '</span><br>' + '$' + this.value;
                      case 'cpc':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + '$' + LC('CAMP.CHECKBOX.CPC') + '</span><br>' + '$' + this.value;
                      case 'clicks':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CLICKS') + '</span><br>' + this.value;
                      case 'cost':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.COST') + '</span><br>' + '$' + this.value;
                      case 'conversions':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CONVERSIONS') + '</span><br>' + this.value;
                      case 'ctr':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CTR') + '%' + '</span><br>' + this.value + '%';
                      default:
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + item.name + '</span><br>' + this.value;
                    }
                  } else {
                    switch (item.name) {
                      case 'impression':
                        return this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                      case 'cpa':
                        return '$' + this.value;
                      case 'cpc':
                        return '$' + this.value;
                      case 'cost':
                        return '$' + this.value;
                      case 'spend':
                        return '$' + this.value;
                      case 'ctr':
                        return this.value + '%';
                    }
                  }

                  return this.value;
                }
              }
            });
            if (visible) {
              if (flag == 'left')
                flag = 'right';
              else
                flag = 'left';
            }
          });
          chart.option('valueAxis', update);
        }
      },
      onInitialized: function (data) {
        vm.chartOptionsFuncFirst = data.component;
      },
      valueAxis: [
        {name: 'impression', position: 'left'},
        {name: 'cpa', position: 'left'},
        {name: 'cpc', position: 'left'},
        {name: 'clicks', position: 'left'},
        {name: 'cost', position: 'left'},
        {name: 'conversions', position: 'left'},
        {name: 'ctr', position: 'left'}
      ],
      argumentAxis: {
        discreteAxisDivisionMode: 'crossLabels',
        grid: {
          visible: true
        }
      },
      crosshair: {

        enabled: true,
        color: 'deepskyblue',
        visible: true,
        horizontalLine: {
          label: {
            visible: true,
            customizeText: function (arg) {
              //console.log(arg);
              if (arg.point.series.name == 'Cost' || arg.point.series.name == 'CPC' || arg.point.series.name == 'CPA') {
                return '$' + this.value;
              }
              if (arg.point.series.name == 'Impressions') {
                return this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
              }
              if ((arg.point.series.name == 'CTR') || (arg.point.series.name == 'CVR')) {
                return this.value + '%';
              }
            },
          }
        },
        verticalLine: {
          label: {
            visible: true
          }
        }

      },
      legend: {
        verticalAlignment: 'top',
        horizontalAlignment: 'center',
        itemTextPosition: 'top'
      },
      commonSeriesSettings: {
        point: {
          size: 7,
          hoverStyle: {
            border: {
              visible: true,
              width: 2
            },
            size: 5
          }
        }
      },
      bindingOptions: {
        dataSource: 'campmain.chartStore'
      },
      series: [{
        name: 'Impressions',
        argumentField: "day",
        valueField: "impression",
        axis: 'impression',
        visible: $localStorage.checkCharCamp.impression
      }, {
        argumentField: "day",
        valueField: "cpa",
        name: 'CPA',
        axis: 'cpa',
        visible: $localStorage.checkCharCamp.cpa
      }, {
        argumentField: "day",
        valueField: "cpc",
        name: 'CPC',
        axis: 'cpc',
        visible: $localStorage.checkCharCamp.cpc
      }, {
        argumentField: "day",
        valueField: "clicks",
        name: 'Clicks',
        axis: 'clicks',
        visible: $localStorage.checkCharCamp.clicks
      }, {
        argumentField: "day",
        valueField: "cost",
        name: 'Cost',
        axis: 'cost',
        visible: $localStorage.checkCharCamp.cost
      }, {
        argumentField: "day",
        valueField: "conversions",
        name: 'Conversions',
        axis: 'conversions',
        visible: $localStorage.checkCharCamp.conversions
      }, {
        argumentField: "day",
        valueField: "ctr",
        name: 'CTR',
        axis: 'ctr',
        visible: $localStorage.checkCharCamp.ctr
      }],
      loadingIndicator: {
        show: true,
        text: "Creating a chart..."
      }
    };

    vm.rangeOptionsFirst = {
      size: {
        height: 80
      },
      scale: {
        minorTickInterval: "day",
        tickInterval: {days: 1},
        minRange: "day",
        maxRange: "year",
        minorTick: {
          visible: true
        }
      },
      bindingOptions: {
        dataSource: 'campmain.chartStore'
      },
      dataSourceField: 'day',
      sliderMarker: {
        format: "monthAndDay"
      },
      behavior: {
        callSelectedRangeChanged: "onMoving"
      },
      onSelectedRangeChanged: function (e) {
        var zoomedChart = $window.$("#zoomedContainerFirst #zoomedChartFirst").dxChart("instance");
        zoomedChart.zoomArgument(e.startValue, e.endValue);
      }
    };

    //endregion

    //region CHECKBOX CHART
    /**
     * @param seriesName {string}
     * @param seriesShortName {string}
     * @param selected {boolean}
     */

    vm.updateCharts = function (seriesName, seriesShortName, selected) {
      $localStorage.checkCharCamp[seriesShortName] = selected;
      vm.gridCharts = $window.$('#zoomedChartFirst').dxChart('instance');
      vm.rangeChartFirst = $window.$('#rangeChartFirst').dxRangeSelector('instance');
      if (selected) {
        vm.gridCharts.getSeriesByName(seriesName).show();
      } else {
        vm.chartOptionsFuncFirst.getSeriesByName(seriesName).hide();
      }
    };

    vm.onlyTwo = function (value) {
      var i = 0;
      var checkTrue = [];
      var checkFalse = [];
      for (i = 0; i < vm.Init.length; i++) {
        if (vm.Init[i]._options.value == true) {
          checkTrue.push(vm.Init[i]);
        } else {
          checkFalse.push(vm.Init[i]);
        }
      }
      if (value == true) {
        if (checkTrue.length == 2 && checkFalse.length > 4) {
          for (i = 0; i < checkFalse.length; i++) {
            checkFalse[i].option('disabled', true);
          }
        }
      } else {
        if (checkTrue.length <= 2) {
          for (i = 0; i < checkFalse.length; i++) {
            checkFalse[i].option('disabled', false);
          }
        }
      }
    };


    function CheckLocalStorage() {
      for (var item in $localStorage.checkCharCamp) {
        if ($localStorage.checkCharCamp[item]) {
          if (item == 'impression') {
            vm.gridCharts.getSeriesByName('Impressions').show();
          }
          if (item == 'cpa') {
            vm.gridCharts.getSeriesByName('CPA').show();
          }
          if (item == 'cpc') {
            vm.gridCharts.getSeriesByName('CPC').show();
          }
          if (item == 'clicks') {
            vm.gridCharts.getSeriesByName('Clicks').show();
          }
          if (item == 'cost') {
            vm.gridCharts.getSeriesByName('Cost').show();
          }
          if (item == 'conversions') {
            vm.gridCharts.getSeriesByName('Conversions').show();
          }
          if (item == 'ctr') {
            vm.gridCharts.getSeriesByName('CTR').show();
          }
        } else {
          if (item == 'impression') {
            vm.gridCharts.getSeriesByName('Impressions').hide();
          }
          if (item == 'cpa') {
            vm.gridCharts.getSeriesByName('CPA').hide();
          }
          if (item == 'cpc') {
            vm.gridCharts.getSeriesByName('CPC').hide();
          }
          if (item == 'clicks') {
            vm.gridCharts.getSeriesByName('Clicks').hide();
          }
          if (item == 'cost') {
            vm.gridCharts.getSeriesByName('Cost').hide();
          }
          if (item == 'conversions') {
            vm.gridCharts.getSeriesByName('Conversions').hide();
          }
          if (item == 'ctr') {
            vm.gridCharts.getSeriesByName('CTR').hide();
          }
        }
      }
    }

    vm.impressions = {
      text: LC('CAMP.CHECKBOX.IMPRESSIONS'),
      value: $localStorage.checkCharCamp.impression,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('Impressions', 'impression', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };

    vm.CPA = {
      text: LC('CAMP.CHECKBOX.CPA'),
      value: $localStorage.checkCharCamp.cpa,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('CPA', 'cpa', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };

    vm.CPC = {
      text: LC('CAMP.CHECKBOX.CPC'),
      value: $localStorage.checkCharCamp.cpc,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('CPC', 'cpc', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };

    vm.clicks = {
      text: LC('CAMP.CHECKBOX.CLICKS'),
      value: $localStorage.checkCharCamp.clicks,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('Clicks', 'clicks', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };
    vm.cost = {
      text: LC('CAMP.CHECKBOX.COST'),
      value: $localStorage.checkCharCamp.cost,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('Cost', 'cost', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };
    vm.conversions = {
      text: LC('CAMP.CHECKBOX.CONVERSIONS'),
      value: $localStorage.checkCharCamp.conversions,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('Conversions', 'conversions', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };
    vm.CTR = {
      text: LC('CAMP.CHECKBOX.CTR'),
      value: $localStorage.checkCharCamp.ctr,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('CTR', 'ctr', e.value);
        vm.onlyTwo(e.value);
        vm.charIsUpdating = false;
        vm.chartOptionsFirst.onDone();
        CheckLocalStorage();
      }
    };
    //endregion

    $timeout(function () {
      var i = 0;
      var checkTrue = [];
      var checkFalse = [];
      for (i = 0; i < vm.Init.length; i++) {
        if (vm.Init[i]._options.value == true) {
          checkTrue.push(vm.Init[i]);
        } else {
          checkFalse.push(vm.Init[i]);
        }
      }
      if (checkTrue.length >= 2 && checkFalse.length > 4) {
        for (i = 0; i < checkFalse.length; i++) {
          checkFalse[i].option('disabled', true);
        }
      }

    });


    //region BOX PLOT
    vm.chartOptionsSecond = {
      bindingOptions: {
        dataSource: 'campmain.boxPlotStore'
      },
      valueAxis: {
        title: 'CPA, $'
      },
      argumentAxis: {
        //valueMarginsEnabled: false,
        grid: {
          visible: true
        },
        label: {
          visible: true
        },
        discreteAxisDivisionMode: 'crossLabels'
      },
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          if (arg.seriesName === "Series 2") {
            return {
              text: "Average: $" + arg.originalValue
            };
          }
          if (arg.seriesName === "Series 1") {
            return {
              text: "Q1: $" + arg.openValue + "<br/>" +
              "Q3: $" + arg.closeValue + "<br/>" +
              "High: $" + arg.highValue + "<br/>" +
              "Low: $" + arg.lowValue + "<br/>"
            };
          }
        }

      },
      legend: {
        visible: false
      },
      loadingIndicator: {
        show: true,
        text: "Creating a chart..."
      },
      useAggregation: true,
      commonSeriesSettings: {
        candlestick: {
          openValueField: 'open',
          closeValueField: 'close',
          highValueField: 'high',
          lowValueField: 'low'
        },
        argumentField: 'day',
        point: {
          size: 6,
          hoverStyle: {
            border: {
              visible: true,
              width: 1
            },
            size: 4
          }
        }
      },
      series: [
        {type: 'candlestick'},
        {valueField: 'avg', color: 'silver'}
      ]
    };

    vm.rangeOptionsSecond = {
      size: {
        height: 80
      },
      bindingOptions: {
        dataSource: 'campmain.boxPlotStore'
      },
      scale: {
        minorTickInterval: "day",
        tickInterval: {days: 1},
        minRange: "day",
        maxRange: "year",
        minorTick: {
          visible: true
        }
      },
      dataSourceField: 'day',
      sliderMarker: {
        format: "week"
      },
      behavior: {
        callSelectedRangeChanged: "onMoving"
      },
      onSelectedRangeChanged: function (e) {
        var zoomedChart = $window.$("#zoomedContainerSecond #zoomedChartSecond").dxChart("instance");
        zoomedChart.zoomArgument(new Date(e.startValue), new Date(e.endValue));
      }
    };
    //endregion


    //region MULTIPLE
    vm.selectedItems = [];
    vm.chartOptionsFuncgrid = [];

    vm.state = '';
    vm.selectCell = {
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
        var selectedRows = $window.$('#gridContainer2')[0].querySelectorAll('[aria-selected="true"]');
        if (selectedRows[0]) {
          var selectedArr = [];
          for (var i = 0; i < selectedRows.length; i++) {
            selectedArr.push(selectedRows[i].firstChild.innerText);
          }
        }
      }
    };

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

    vm.UI = {
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
          oneSuspend = true;
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

          for (var i = 0; i < tempSespendRow.placement.length; i++) {
            var w = $window.$('div.state-white' + tempSespendRow.placement[i]);
            var b = $window.$('div.state-black' + tempSespendRow.placement[i]);
            var s = $window.$('div.state-suspended' + tempSespendRow.placement[i]);
            w.dxButton('instance').option('disabled', true);
            b.dxButton('instance').option('disabled', true);
            s.dxButton('instance').option('disabled', true);
            w.removeClass('active');
            b.removeClass('active');
            s.removeClass('active');
          }

          CampMain.editCampaignDomains(vm.campId, tempSespendRow.placement, 1, suspendPlacement)
            .then(function (res) {
              for (var i = 0; i < tempSespendRow.placement.length; i++) {
                var b = $window.$('div.state-black' + tempSespendRow.placement[i]);
                var w = $window.$('div.state-white' + tempSespendRow.placement[i]);
                var s = $window.$('div.state-suspended' + tempSespendRow.placement[i]);
                w.dxButton('instance').option('disabled', false);
                b.dxButton('instance').option('disabled', false);
                s.dxButton('instance').option('disabled', false);
                if (res == 404) {
                  $window.DevExpress.ui.notify("Not found", "warning", 4000);
                  $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                  return res;
                }
                if (res == 503) {
                  $window.DevExpress.ui.notify("Not connect to appnexus server, please try again later", "warning", 4000);
                  $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                  return res;
                }
                if (res !== 'Unactive') {
                  s.addClass('active');
                }
              }
              oneSuspend = false;
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
      }
    };


    vm.dataGridOptionsCampaign = {
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
      alignment: 'left',
      headerFilter: {
        visible: true
      },
      filterRow: {
        visible: true,
        applyFilter: "auto"
      },
      loadPanel: {
        shadingColor: "rgba(0,0,0,0.4)",
        visible: false,
        showIndicator: true,
        showPane: true,
        shading: true,
        closeOnOutsideClick: false
      },
      bindingOptions: {
        dataSource: 'campmain.gridStore'
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
          headerFilter: {
            dataSource: function (source) {
              return headerFilterColumn(source, 'placement');
            }
          }
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.DOMAIN'),
          dataField: 'placement__rtbimpressiontrackerplacementdomain__domain',
          alignment: 'center',
          dataType: 'string',
          allowEditing: false,
          headerFilter: {
            dataSource: function (source) {
              return headerFilterColumn(source, 'domain');
            }
          }
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.NETWORK'),
          dataField: 'NetworkPublisher',
          alignment: 'center',
          dataType: 'string',
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
          format: 'fixedPoint',
          alignment: 'center',
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
          format: 'currency',
          precision: 4,
          alignment: 'center',
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
          format: 'currency',
          precision: 2,
          dataType: 'number',
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
          format: 'currency',
          precision: 4,
          dataType: 'number',
          headerFilter: {
            dataSource: function (source) {
              return headerFilterColumn(source, 'cpc');
            }
          },

        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CPM') + ' ,$',
          dataField: 'cpm',
          alignment: 'center',
          format: 'currency',
          precision: 4,
          dataType: 'number',
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
          format: 'percent',
          precision: 2,
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
          format: 'percent',
          precision: 2,
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
          format: 'fixedPoint',
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
          format: 'fixedPoint',
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
          format: 'percent',
          precision: 1,
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
          format: 'percent',
          precision: 1,
          dataType: 'number',
          headerFilter: {
            dataSource: function (source) {
              return headerFilterColumn(source, 'view_rate');
            }
          }
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.STATE'),
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
                var w = $window.$('div.state-white' + options.data.placement);
                var b = $window.$('div.state-black' + options.data.placement);
                var s = $window.$('div.state-suspended' + options.data.placement);
                w.dxButton('instance').option('disabled', true);
                b.dxButton('instance').option('disabled', true);
                s.dxButton('instance').option('disabled', true);
                w.removeClass('active');
                b.removeClass('active');
                s.removeClass('active');
                CampMain.editCampaignDomains(vm.campId, [options.data.placement], 4)
                  .then(function (res) {
                    w.dxButton('instance').option('disabled', false);
                    b.dxButton('instance').option('disabled', false);
                    s.dxButton('instance').option('disabled', false);
                    if (res == 404) {
                      $window.DevExpress.ui.notify("Not found", "warning", 4000);
                      $('#gridContainerWhite').dxDataGrid('instance').refresh();
                      return res;
                    }
                    if (res == 503) {
                      $window.DevExpress.ui.notify("Not connect to appnexus server, please try again later", "warning", 4000);
                      $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                      return res;
                    }
                    if (res !== 'Unactive') {
                      w.addClass('active');
                    }
                    return res;
                  })
                  .catch(function (err) {
                    return err;
                  });
              }
            });

            if (options.data.state.whiteList == 4) {
              white.addClass('state-white' + options.data.placement).addClass('active').appendTo(container);
            } else {
              white.addClass('state-white' + options.data.placement).appendTo(container);
            }

            var black = $window.$("<div />").dxButton({
              text: 'black',
              height: 30,
              width: 89,
              disabled: false,
              onClick: function (e) {
                var w = $window.$('div.state-white' + options.data.placement);
                var b = $window.$('div.state-black' + options.data.placement);
                var s = $window.$('div.state-suspended' + options.data.placement);
                w.dxButton('instance').option('disabled', true);
                b.dxButton('instance').option('disabled', true);
                s.dxButton('instance').option('disabled', true);
                w.removeClass('active');
                b.removeClass('active');
                s.removeClass('active');
                CampMain.editCampaignDomains(vm.campId, [options.data.placement], 2)
                  .then(function (res) {
                    w.dxButton('instance').option('disabled', false);
                    b.dxButton('instance').option('disabled', false);
                    s.dxButton('instance').option('disabled', false);
                    if (res == 404) {
                      $window.DevExpress.ui.notify("Not found", "warning", 4000);
                      $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                      return res;
                    }
                    if (res == 503) {
                      $window.DevExpress.ui.notify("Not connect to appnexus server, please try again later", "warning", 4000);
                      $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                      return res;
                    }
                    if (res !== 'Unactive') {
                      b.addClass('active');
                    }
                    return res;
                  })
                  .catch(function (err) {
                    return err;
                  });
              }
            });

            if (options.data.state.blackList == 2) {
              black.addClass('state-black' + options.data.placement).addClass('active').appendTo(container);
            } else {
              black.addClass('state-black' + options.data.placement).appendTo(container);
            }


            var suspended = $window.$("<div />").dxButton({
              text: 'suspend',
              height: 30,
              width: 95,
              disabled: false,
              onClick: function () {
                if (oneSuspend == true) {
                  $window.DevExpress.ui.notify("Wait please", "warning", 4000);
                  return 0;
                }
                tempSespendRow.placement = [options.data.placement];
                tempSespendRow.suspend = 1;
                vm.confirmPopup.option('visible', true);
              }
            });

            if (options.data.state.suspended == 1) {
              suspended.addClass('state-suspended' + options.data.placement).addClass('active').appendTo(container);
            } else {
              suspended.addClass('state-suspended' + options.data.placement).appendTo(container);
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
              data.valueText = 'Conv: ' + vm.Camp.totalSummary.conv;
              return data.valueText;
            }
          },
          {
            column: "imp",
            summaryType: "sum",
            customizeText: function (data) {
              data.valueText = 'Imp: ' + vm.Camp.totalSummary.imp.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
              return data.valueText;
            }
          },
          {
            column: "cpa",
            summaryType: "sum",
            valueFormat: "currency",
            customizeText: function (data) {
              data.valueText = 'CPA: $' + vm.Camp.totalSummary.cpa.toFixed(4);
              return data.valueText;
            }
          },
          {
            column: "cost",
            summaryType: "sum",
            valueFormat: "currency",
            customizeText: function (data) {
              data.valueText = 'Cost: $' + vm.Camp.totalSummary.cost.toFixed(2);
              return data.valueText;
            }
          },
          {
            column: "clicks",
            summaryType: "sum",
            customizeText: function (data) {
              data.valueText = 'Clicks: ' + vm.Camp.totalSummary.clicks;
              return data.valueText;
            }
          },
          {
            column: "cpc",
            summaryType: "sum",
            customizeText: function (data) {
              data.valueText = 'CPC: $' + vm.Camp.totalSummary.cpc.toFixed(4);
              return data.valueText;
            }
          },
          {
            column: "cpm",
            summaryType: "sum",
            customizeText: function (data) {
              data.valueText = 'CPM: $' + vm.Camp.totalSummary.cpm.toFixed(4);
              return data.valueText;
            }
          },
          {
            column: "cvr",
            summaryType: "sum",

            customizeText: function (data) {
              data.valueText = 'CVR: %' + vm.Camp.totalSummary.cvr.toFixed(4);
              return data.valueText;
            }
          },
          {
            column: "ctr",
            valueFormat: "percent",
            summaryType: "sum",
            customizeText: function (data) {
              data.valueText = 'CTR: %' + vm.Camp.totalSummary.ctr.toFixed(4);
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
      onEditorPreparing: function (info) {
        if ((info.parentType == 'filterRow') && (info.dataField == 'state')) {
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
              },
              {
                'name': 'Clear state',
                'state': 0
              }
            ],
            placeholder: 'Select a state',
            displayExpr: 'name',
            valueExpr: vm.state,
            onSelectionChanged: function (e) {
              var selectedRows = $window.$('#gridContainer2')[0].querySelectorAll('[aria-selected="true"]');
              if (selectedRows[0]) {
                var selectedArr = [];
                for (var i = 0; i < selectedRows.length; i++) {
                  selectedArr.push(selectedRows[i].firstChild.innerText);
                }
                if (e.selectedItem.state == 1) {
                  if (selectedArr != '[]') {
                    tempSespendRow.placement = selectedArr;
                    tempSespendRow.suspend = 'suspend';
                    vm.confirmPopupVisible = true;
                    vm.confirmPopup.option('visible', true);
                  }
                } else {
                  if (selectedArr != '[]') {
                    for (var i = 0; i < selectedArr.length; i++) {
                      var w = $window.$('div.state-white' + selectedArr[i]);
                      var b = $window.$('div.state-black' + selectedArr[i]);
                      var s = $window.$('div.state-suspended' + selectedArr[i]);
                      w.dxButton('instance').option('disabled', true);
                      b.dxButton('instance').option('disabled', true);
                      s.dxButton('instance').option('disabled', true);
                      w.removeClass('active');
                      b.removeClass('active');
                      s.removeClass('active');
                    }

                    CampaignOptimiser.editCampaignDomains(vm.campId, selectedArr, e.selectedItem.state).then(function (res) {
                      for (var i = 0; i < selectedArr.length; i++) {
                        var b = $window.$('div.state-black' + selectedArr[i]);
                        var w = $window.$('div.state-white' + selectedArr[i]);
                        var s = $window.$('div.state-suspended' + selectedArr[i]);
                        w.dxButton('instance').option('disabled', false);
                        b.dxButton('instance').option('disabled', false);
                        s.dxButton('instance').option('disabled', false);
                        if (res == 404) {
                          $window.DevExpress.ui.notify("Not found", "warning", 4000);
                          $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                          return res;
                        }
                        if (res == 503) {
                          $window.DevExpress.ui.notify("Not connect to appnexus server, please try again later", "warning", 4000);
                          $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                          return res;
                        }
                        if (e.selectedItem.state == 2) {
                          b.addClass('active');
                        }
                        if (e.selectedItem.state == 4) {
                          w.addClass('active');
                        }
                      }
                      $('#gridContainer2').dxDataGrid('instance').refresh();
                    });
                  }
                }
              } else {
                return $window.DevExpress.ui.notify(LC('CO.NO-ITEMS-CHOSEN'), "warning", 4000);
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
    };
    //endregion
  }
})();

