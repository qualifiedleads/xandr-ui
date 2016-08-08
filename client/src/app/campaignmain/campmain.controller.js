(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('CampaignMainController', CampaignMainController);

  /** @ngInject */
  function CampaignMainController($window, $state, $localStorage, $translate, $timeout, CampMain, Campaign) {
    var vm = this;
    vm.Camp = CampMain;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';
    var LC = $translate.instant;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.Init = [];

    if ($localStorage.checkCharCamp == null) {
      $localStorage.checkCharCamp = {
        'impression': true,
        'cpa': false,
        'cpc': false,
        'clicks': false,
        'mediaspent': false,
        'conversions': false,
        'ctr': false
      };
    }

    vm.optimiser = {
      text: LC('CAMP.GO-OPTIMISER'),
      onClick: function () {
        $state.go('home.campaignoptimiser', {"id": vm.campId});
      }
    };

    vm.seriesCamp = [{
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
      valueField: "mediaspent",
      name: 'mediaspent',
      axis: 'mediaspent',
      visible: $localStorage.checkCharCamp.mediaspent
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
    }];


    vm.totals = [];
    vm.chartStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.graphinfo(vm.campId, vm.dataStart, vm.dataEnd, vm.by)
        .then(function (result) {
          return result;
        });
      }
    });

    vm.boxPlotStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.cpaReport(vm.campId, vm.dataStart, vm.dataEnd)
        .then(function (result) {
          return result;
        });
      }
    });


    vm.gridStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return vm.Camp.totalCount;
      },
      load: function (loadOptions) {
        return vm.Camp.campaignDomains(vm.campId, vm.dataStart, vm.dataEnd, loadOptions.skip,
          loadOptions.take, loadOptions.sort, loadOptions.order, loadOptions.filter)
      }
    });

    /** BIG DIAGRAM  - START **/
    vm.types = ['line', 'stackedLine', 'fullStackedLine'];
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
                    switch ( item.name) {
                      case 'impression':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.IMPRESSIONS') + '</span><br>' + this.value;
                      case 'cpa':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CPA') + '</span><br>' + this.value;
                      case 'cpc':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CPC') + '</span><br>' + this.value;
                      case 'clicks':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CLICKS') + '</span><br>' + this.value;
                      case 'mediaspent':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.MEDIA_SPENT') + '</span><br>' + this.value;
                      case 'conversions':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CONVERSIONS') + '</span><br>' + this.value;
                      case 'ctr':
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('CAMP.CHECKBOX.CTR') + '</span><br>' + this.value;
                      default:
                        return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + item.name + '</span><br>' + this.value;
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
        {name: 'mediaspent', position: 'left'},
        {name: 'conversions', position: 'left'},
        {name: 'ctr', position: 'left'}
      ],
      argumentAxis: {
        //valueMarginsEnabled: false,
        discreteAxisDivisionMode: 'crossLabels',
        grid: {
          visible: true
        }
      },
      crosshair: {
        enabled: true,
        color: 'deepskyblue',
        label: {
          visible: true
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
      series: vm.seriesCamp,
      loadingIndicator: {
        show: true,
        text: "Creating a chart..."
      }
    };

    vm.rangeOptionsFirst = {
      size:{
        height:80
      },
      scale: {
        minorTickInterval: "day",
        tickInterval: { days: 1 },
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

    /** BIG DIAGRAM  - END **/

    /** CHECKBOX CHART - START **/
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
          if (item == 'mediaspent') {
            vm.gridCharts.getSeriesByName('mediaspent').show();
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
          if (item == 'mediaspent') {
            vm.gridCharts.getSeriesByName('mediaspent').hide();
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

    /** CHECKBOX CHART - START **/
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
    vm.media = {
      text: LC('CAMP.CHECKBOX.MEDIA_SPENT'),
      value: $localStorage.checkCharCamp.mediaspent,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        vm.updateCharts('mediaspent', 'mediaspent', e.value);
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
    /** CHECKBOX CHART - END **/

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


    /** DATE PIKER - START **/
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
      }];

    vm.datePiker = {
      items: products,
      displayExpr: 'Name',
      valueExpr: 'ID',
      value: products[$localStorage.SelectedTime].ID,
      onValueChanged: function (e) {
        //$log.info(products[e.value]);
        $localStorage.SelectedTime = e.value;
        $localStorage.dataStart = products[e.value].dataStart;
        $localStorage.dataEnd = products[e.value].dataEnd;

        //$('#gridContainer1').dxDataGrid('instance').refresh();
        //$('#gridContainer2').dxDataGrid('instance').refresh();
        $state.reload();
      }
    };
    /** DATE PIKER - END **/


    /** BOX PLOT- START **/


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
        // label: {
        //   //visible: true,
		 //      format: "shortDate"
	     //  },
        discreteAxisDivisionMode: 'crossLabels'
      },
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          console.log(arg);
          if (arg.seriesName === "Series 2") {
            return {
              text: "Average: $" + arg.originalValue
            }; 
          }
          if (arg.seriesName === "Series 1") {
            return {
              text: "Open: $" + arg.openValue + "<br/>" +
              "Close: $" + arg.closeValue + "<br/>" +
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
      size:{
        height:80
      },
      bindingOptions: {
        dataSource: 'campmain.boxPlotStore'
      },
      scale: {
        minorTickInterval: "day",
        tickInterval: { days: 1 },
        minRange: "day",
        maxRange: "year",
        minorTick: {
          visible: true
        }
      },
      dataSourceField: 'day',
      sliderMarker: {
        format: "monthAndDay"
      },
      behavior: {
        callSelectedRangeChanged: "onMoving"
      },
      onSelectedRangeChanged: function (e) {
        var zoomedChart = $window.$("#zoomedContainerSecond #zoomedChartSecond").dxChart("instance");
        zoomedChart.zoomArgument(new Date(e.startValue), new Date(e.endValue));
      }
    };


    /** BOX PLOT- END **/


    /** MULTIPLE - START **/
    vm.selectedItems = [];
    vm.chartOptionsFuncgrid = [];
    if ($localStorage.boxPlotData == null) {
      $localStorage.boxPlotData = vm.boxPlotData;
    }

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


    vm.dataGridOptionsCampaign = {
      onInitialized: function (data) {
        vm.dataGridOptionsMultipleFunc = data.component;
        vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 9;
        vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].width = 35;
      },
      onRowPrepared: function (data) {
        vm.objectData = data;
        if (vm.objectData.rowType == 'data') {
          var allRowBtns = data.rowElement[0].childNodes[9];
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
      showBorders: true,
      alignment: 'left',
      headerFilter: {
        visible: true
      },
      bindingOptions: {
        dataSource: 'campmain.gridStore'
      },
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      howBorders: true,
      showRowLines: true,
      columns: [
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.PLACEMENT'),
          dataField: 'placement'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.NETWORK'),
          dataField: 'NetworkPublisher'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CONV'),
          dataField: 'conv'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.IMP'),
          dataField: 'imp'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.COST'),
          dataField: 'cost'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CLICKS'),
          dataField: 'clicks'
        }, {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CPC'),
          dataField: 'cpc'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CPM'),
          dataField: 'cpm'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CVR'),
          dataField: 'cvr'
        },
        {
          caption: LC('CAMP.CAMPAIGN.COLUMNS.CTR'),
          dataField: 'ctr'
        },
        {
          caption: 'State',
          width: 300,
          columnIndex: 16,
          headerCellTemplate: 'headerCellTemplate',
          cellTemplate: function (container, options) {
            $window.$("<div />").dxButton({
              text: 'white',
              height: 30,
              width: 89,
              disabled: true,
              onClick: function (e) {
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
              disabled: true,
              onClick: function (e) {
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
              disabled: true,
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

              }
            }).addClass('suspended').appendTo(container);
          }
        }
      ],
      selection: {
        mode: 'multiple',
        showCheckBoxesMode: 'always'
      },
      onSelectionChanged: function (data) {
        vm.selectedItems = data.selectedRowsData;
        vm.disabled = !vm.selectedItems.length;
      }
    };
    /** MULTIPLE - END **/


    /** RANGE SELECTOR FIRST - START **/
    vm.rangeFirstChartOptions = {
      margin: {
        left: 50
      },
      scale: {
        startValue: new Date($localStorage.dataStart),
        endValue: new Date($localStorage.dataEnd),
        minorTickInterval: "day",
        minRange: "hour",
        maxRange: "month",
        minorTick: {
          visible: false
        }
      },
      sliderMarker: {
        format: "monthAndDay"
      }
      // selectedRange: {
      //   startValue: new Date($localStorage.dataStart),
      //   endValue: new Date($localStorage.dataEnd)
      // }
    };

    /** RANGE SELECTOR FIRST - END **/

    /** RANGE SELECTOR SECOND - START **/
    vm.rangeSecondChartOptions = {
      margin: {
        left: 50,
        top: 12
      },
      size: {
        height: 150,
        width: 450
      },
      scale: {
        startValue: new Date($localStorage.dataStart),
        endValue: new Date($localStorage.dataEnd),
        minorTickInterval: "day",
        minRange: "day",
        maxRange: "month",
        minorTick: {
          visible: false
        }
      },
      sliderMarker: {
        format: "monthAndDay"
      }
      // selectedRange: {
      //   startValue: new Date(2011, 2, 3),
      //   endValue: new Date(2011, 2, 9)
      // }
    };

    /** RANGE SELECTOR SECOND - END **/


    /** PIE CHART CONTAINER - START **/
    vm.ctrlBbtns = {
      placement: {
        btn: 'Placement',
        header: 'Placement'
      },
      creativeId: {
        btn: 'creative_id',
        header: 'creative_id'
      },
      creativeSize: {
        btn: 'creative_size',
        header: 'creative_size'
      },
      viewability: {
        btn: 'viewability',
        header: 'viewability'
      },
      os: {
        btn: 'OS',
        header: 'Operating System used'
      },
      carrier: {
        btn: 'carrier',
        header: 'carrier'
      },
      networkSeller: {
        btn: 'network(seller)',
        header: 'network (seller)'
      },
      connectionType: {
        btn: 'connection_type',
        header: 'connection_type'
      },
      device: {
        btn: 'device',
        header: 'device'
      },
      seller: {
        btn: 'seller',
        header: 'Seller'
      }
    };
    vm.pieChartHeader = $localStorage.pieChartHeader || vm.ctrlBbtns.os.header;

  }
})();

