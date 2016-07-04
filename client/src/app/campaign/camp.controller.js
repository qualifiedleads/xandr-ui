(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CampaignController', CampaignController);

  /** @ngInject */
  function CampaignController($compile, $window, $state, $localStorage, $translate, $log, $stateParams, Camp, Main) {
    var vm = this;
    vm.Camp = Camp;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.by = '';
    var LC = $translate.instant;



    if ($localStorage.series == null ){
      $localStorage.series = [
        { valueField: 'impressions', name: 'Impressions' },
        { valueField: 'cpa', name: 'CPA' },
        { valueField: 'cpc', name: 'CPC' },
        { valueField: 'clicks', name: 'clicks' },
        { valueField: 'media', name: 'media' },
        { valueField: 'conversions', name: 'conversions' },
        { valueField: 'ctr', name: 'CTR' }
      ];
    }
    //$localStorage.checkChart = null;
    var tempIndex = [];
    if ($localStorage.checkChart == null ){
      $localStorage.checkChart = {
        'impressions': true,
        'cpa': true,
        'cpc':true,
        'clicks': true,
        'media': true,
        'conversions': true,
        'ctr': true
      };
      tempIndex = [];
      for(var index in $localStorage.checkChart) {
        if ($localStorage.checkChart[index] == true) {
          tempIndex.push(index);
        }
      }
      vm.by = tempIndex.join();
    } else {
      tempIndex = [];
      for(var index in $localStorage.checkChart) {
        if ($localStorage.checkChart[index] == true) {
          tempIndex.push(index);
        }
      }
      vm.by = tempIndex.join();
    }
    //console.log($stateParams.id);

    vm.Camp.nameCampaigns($stateParams.id)
      .then(function (result) {
        for (var i = 0; i < result.length; i++) {
          if (result[i].id == $stateParams.id) {
            vm.campName = result[i].campaign;
            break
          }
        }
      });

    /** BIG DIAGRAM  - START **/
    vm.types = ['line', 'stackedLine', 'fullStackedLine'];

    var series = [
      { valueField: 'impressions', name: 'Impressions' },
      { valueField: 'cpa', name: 'CPA' },
      { valueField: 'cpc', name: 'CPC' },
      { valueField: 'clicks', name: 'clicks' },
      { valueField: 'media', name: 'media' },
      { valueField: 'conversions', name: 'conversions' },
      { valueField: 'ctr', name: 'CTR' }
    ];

    vm.chartOptions = {
      onInitialized: function (data) {
        vm.chartOptionsFunc = data.component;
      },
      series: $localStorage.series,
      size: {
        width: 500,
        height: 230
      },
      bindingOptions: {
        dataSource: 'camp.chartStore'
      },
      commonSeriesSettings: {
        argumentField: 'day',
        type: vm.types[0],
        point: {
          size: 3,
          hoverStyle: {
            border: {
              visible: true,
              width: 2
            },
            size: 5
          }
        }

      },
      margin: {
        bottom: 20
      },
      argumentAxis: {
        valueMarginsEnabled: false,
        discreteAxisDivisionMode: 'crossLabels',
        grid: {
          visible: true
        }
      },
      legend: {
        verticalAlignment: 'bottom',
        horizontalAlignment: 'center',
        itemTextPosition: 'bottom'
      },
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          return {
            text: arg.valueText
          };
        }
      }
    };
    /** BIG DIAGRAM  - END **/
    vm.totals = [];
    vm.chartStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.statsChart(vm.dataStart, vm.dataEnd,vm.by)
          .then(function (result) {
            return result.statistics;
          });
      }
    });



    vm.multipleStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return vm.multipleTotalCount ;
      },
      load: function (loadOptions) {
        if(loadOptions.take == null) {
          loadOptions.take = 20;
        }
        if(loadOptions.skip == null) {
          loadOptions.skip = 0;
        }
        if(loadOptions.sort == null) {
          loadOptions.sort = 'campaign';
        }
        if(loadOptions.order == null) {
          loadOptions.order = 'DESC';
        }
        return vm.Camp.statsCampaigns(vm.dataStart, vm.dataEnd, loadOptions.skip,
          loadOptions.take, loadOptions.sort, loadOptions.order,
          vm.by, loadOptions.filter)
          .then(function (result) {
            vm.multipleTotalCount = result.totalCount;
            return result.campaigns;
          });
      }
    });

    /** CHECKBOX CHART - START **/
    vm.impressions = {
      text: LC('MAIN.CHECKBOX.IMPRESSIONS'),
      value: $localStorage.checkChart.impressions? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.impressions = true;
          $localStorage.series.push({ valueField: 'impressions', name: 'Impressions' });
          $state.reload();
        } else {
          $localStorage.checkChart.impressions = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'impressions') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };

    vm.CPA = {
      text: LC('MAIN.CHECKBOX.CPA'),
      value: $localStorage.checkChart.cpa? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.cpa = true;
          $localStorage.series.push({ valueField: 'cpa', name: 'CPA' });
          $state.reload();
        } else {
          $localStorage.checkChart.cpa = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'cpa') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };

    vm.CPC = {
      text: LC('MAIN.CHECKBOX.CPC'),
      value: $localStorage.checkChart.cpc? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.cpc = true;
          $localStorage.series.push({ valueField: 'cpc', name: 'CPC' });
          $state.reload();
        } else {
          $localStorage.checkChart.cpc = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'cpc') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.clicks = {
      text: LC('MAIN.CHECKBOX.CLICKS'),
      value: $localStorage.checkChart.clicks? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.clicks = true;
          $localStorage.series.push({ valueField: 'clicks', name: 'clicks' });
          $state.reload();
        } else {
          $localStorage.checkChart.clicks = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'clicks') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.media = {
      text: LC('MAIN.CHECKBOX.MEDIA_SPENT'),
      value: $localStorage.checkChart.media? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.media = true;
          $localStorage.series.push({ valueField: 'media', name: 'media' });
          $state.reload();
        } else {
          $localStorage.checkChart.media = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'media') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.conversions = {
      text: LC('MAIN.CHECKBOX.CONVERSIONS'),
      value: $localStorage.checkChart.conversions? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.conversions = true;
          $localStorage.series.push({ valueField: 'conversions', name: 'conversions' });
          $state.reload();
        } else {
          $localStorage.checkChart.conversions = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'conversions') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.CTR = {
      text: LC('MAIN.CHECKBOX.CTR'),
      value: $localStorage.checkChart.ctr? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkChart.ctr = true;
          $localStorage.series.push({ valueField: 'ctr', name: 'CTR' });
          $state.reload();
        } else {
          $localStorage.checkChart.ctr = false;
          for(var index in $localStorage.series) {
            if ($localStorage.series[index].valueField == 'ctr') {
              $localStorage.series.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    /** CHECKBOX CHART - END **/

    /** DATE PIKER - START **/
    if ($localStorage.dataStart == null && $localStorage.dataEnd == null ){
      $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix() ;
      $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
    } else {
      vm.dataStart = $localStorage.dataStart;
      vm.dataEnd = $localStorage.dataEnd;
    }
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
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
    vm.boxPlot = {
      onInitialized: function (data) {
        vm.chartOptionsFunc = data.component;
      },
      size: {
        width: 500,
        height: 200
      },dataSource: [{
        date: new Date(1994, 2, 1),
        l: 23.00,
        h: 27.00,
        o: 24.00,
        c: 25.875
      }, {
        date: new Date(1994, 2, 2),
        l: 23.625,
        h: 25.125,
        o: 24.00,
        c: 24.875
      }, {
        date: new Date(1994, 2, 3),
        l: 27.25,
        h: 30.25,
        o: 26.75,
        c: 30.00
      }, {
        date: new Date(1994, 2, 4),
        l: 26.50,
        h: 27.875,
        o: 26.875,
        c: 27.25
      }, {
        date: new Date(1994, 2, 7),
        l: 26.375,
        h: 27.50,
        o: 27.375,
        c: 26.75
      }],
      commonSeriesSettings: {
        argumentField: "date",
        type: "candlestick"
      },
      series: [
        {
          openValueField: "o",
          highValueField: "h",
          lowValueField: "l",
          closeValueField: "c",
          reduction: {
            color: "red"
          }
        }
      ],
      valueAxis: {
        tickInterval: 1,
        title: {
          text: "US dollars"
        },
        label: {
          format: "currency",
          precision: 0
        }
      },
      argumentAxis: {
        label: {
          format: "shortDate"
        }
      },
      tooltip: {
        enabled: true,
        location: "edge",
        customizeTooltip: function (arg) {
          return {
            text: "Open: $" + arg.openValue + "<br/>" +
            "Close: $" + arg.closeValue + "<br/>" +
            "High: $" + arg.highValue + "<br/>" +
            "Low: $" + arg.lowValue + "<br/>"
          };
        }
      }
    };

    /** BOX PLOT- END **/



    /** MULTIPLE - START **/
    vm.selectedItems = [];
    vm.chartOptionsFuncgrid = [];
    vm.boxPlotData = [{
      "placement":"CNN.com",
      "NetworkPublisher":"Google Adx",
      "conv":"8",
      "imp":"5500",
      "clicks":"21",
      "cpc":"$0,31",
      "cpm":"$1,38",
      "cvr":"",
      "ctr":"",
      "state": {
        "whiteList": "true",
        "blackList": "false",
        "suspended": "false"
      }
    },
      {
        "placement":"Hidden",
        "NetworkPublisher":"PubMatic",
        "conv":"3",
        "imp":"5500",
        "clicks":"21",
        "cpc":"$0,31",
        "cpm":"$1,38",
        "cvr":"",
        "ctr":"",
        "state": {
          "whiteList": "false",
          "blackList": "true",
          "suspended": "false"
        }
      },
      {
        "placement":"BBC.com",
        "NetworkPublisher":"OpenX",
        "conv":"1",
        "imp":"5500",
        "clicks":"21",
        "cpc":"$0,31",
        "cpm":"$1,38",
        "cvr":"",
        "ctr":"",
        "state": {
          "whiteList": "false",
          "blackList": "false",
          "suspended": "true"
        }
      },
      {
        "placement":"msn.com",
        "NetworkPublisher":"Rubicon",
        "conv":"8",
        "imp":"5500",
        "clicks":"21",
        "cpc":"$0,31",
        "cpm":"$1,38",
        "cvr":"",
        "ctr":"",
        "state": {
          "whiteList": "true",
          "blackList": "false",
          "suspended": "false"
        }
      }
    ];
    if ($localStorage.boxPlotData == null){
      $localStorage.boxPlotData = vm.boxPlotData;
    }
    vm.dataGridOptionsCampaign = {
      onInitialized: function (data) {
         vm.dataGridOptionsMultipleFunc = data.component;
         vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 9;
         //console.log(data);
        },
      onRowPrepared: function(data) {
        vm.objectData = data;
        if(vm.objectData.rowType == 'data') {
          //console.log(vm.objectData);
          var allRowBtns = data.rowElement[0].childNodes[9];
          var state = data.data.state;
          if(state.whiteList == "true"){
            allRowBtns.classList.add('active-white');
          }
          if(state.blackList == "true"){
            allRowBtns.classList.add('active-black');
          }
          if(state.suspended == "true"){
            allRowBtns.classList.add('active-suspended');
          }
        }
      },
      showBorders: true,
      alignment: 'left',
      headerFilter: {
        visible: true
      },
      dataSource:  $localStorage.boxPlotData || vm.boxPlotData,
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      howBorders: true,
      showRowLines: true,
      columns: [
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.PLACEMENT'),
          dataField: 'placement'
        },
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.NETWORK'),
          dataField: 'NetworkPublisher'
        },
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.CONV'),
          dataField: 'conv'
        }, {
          caption:  LC('MAIN.CAMPAIGN.COLUMNS.IMP'),
          dataField: 'imp'
        }, {
          caption:  LC('MAIN.CAMPAIGN.COLUMNS.CLICKS'),
          dataField: 'clicks'
        }, {
          caption:  LC('MAIN.CAMPAIGN.COLUMNS.CPC'),
          dataField: 'cpc'
        },
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.CPM'),
          dataField: 'cpm'
        },
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.CVR'),
          dataField: 'cvr'
        },
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.CTR'),
          dataField: 'ctr'
        },
        {
          width: 300,
          columnIndex: 16,
          cellTemplate: function (container, options) {
            $("<div />").dxButton({
              text: 'white list',
              height:30,
              width: 89,
              onClick: function (e) {
                console.log(options.data.state);
                var parentWhiteBtn = e.element[0].parentNode;
                console.log(parentWhiteBtn);
                if (parentWhiteBtn.classList.contains('active-white')) {
                  parentWhiteBtn.classList.remove('active-white');
                  parentWhiteBtn.classList.add('unactive-white');
                  options.data.state.whiteList = 'false';
                } else if (!parentWhiteBtn.classList.contains('active-white')){
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

            $("<div />").dxButton({
              text: 'black list',
              height:30,
              width: 89,
              onClick: function (e) {
                console.log(e);
                var parentWhiteBtn = e.element[0].parentNode;
                console.log(parentWhiteBtn);
                if (parentWhiteBtn.classList.contains('active-black')) {
                  parentWhiteBtn.classList.remove('active-black');
                  parentWhiteBtn.classList.add('unactive-black');
                  options.data.state.blackList = 'false';
                } else if (!parentWhiteBtn.classList.contains('active-black')){
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

            $("<div />").dxButton({
              text: 'suspended',
              height:30,
              width: 95,
               onClick: function (e) {
                 console.log(e);
                 var parentWhiteBtn = e.element[0].parentNode;
                 console.log(parentWhiteBtn);
                 if (parentWhiteBtn.classList.contains('active-suspended')) {
                   parentWhiteBtn.classList.remove('active-suspended');
                   parentWhiteBtn.classList.add('unactive-suspended');
                   options.data.state.suspended = 'false';
                 } else if (!parentWhiteBtn.classList.contains('active-suspended')){
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
      bindingOptions: {
          allowColumnResizing: 'true'
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
        size: {
        height: 150,
        width: 450
      },
      scale: {
        startValue:  new Date($localStorage.dataStart),
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
      placement:'Placement',
      creativeId:'creative_id',
      creativeSize:'creative_size',
      viewability: 'viewability',
      os:'OS',
      carrier:'carrier',
      networkSeller: 'network (seller)',
      connectionType: 'connection_type',
      device:'device',
      extra:'extra',
      publisher:'Publisher'
  };
    vm.pieChartHeader = $localStorage.pieChartHeader;
   vm.btnsNodesArray = $('.label-container')[0].children;

    vm.selectInfoBtn = function ($event, value) {
      vm.pieChartHeader = value;
        $localStorage.pieChartHeader = vm.pieChartHeader;

      Array.prototype.forEach.call(vm.btnsNodesArray, function(node) {
        if(node.classList.contains('nav-btn-active')){
          node.classList.remove('nav-btn-active');
        }
      });
      $localStorage.pieChartHeader = vm.pieChartHeader;
      $event.currentTarget.classList.add('nav-btn-active');

   
    }


  }
})();
