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



    if ($localStorage.seriesCamp == null ){
      $localStorage.seriesCamp = [{
        argumentField: "day",
        valueField: "impression"
      }, {
        argumentField: "day",
        valueField: "cpa"
      }, {
        argumentField: "day",
        valueField: "cpc"
      }, {
        argumentField: "day",
        valueField: "clicks"
      }, {
        argumentField: "day",
        valueField: "mediaspent"
      }, {
        argumentField: "day",
        valueField: "conversions"
      }, {
        argumentField: "day",
        valueField: "ctr"
      }];

    }
    //$localStorage.checkCharCamp = null;
    var tempIndex = [];
    if ($localStorage.checkCharCamp== null ){
      $localStorage.checkCharCamp = {
        'impressions': true,
        'cpa': true,
        'cpc':true,
        'clicks': true,
        'mediaspent': true,
        'conversions': true,
        'ctr': true
      };
      tempIndex = [];
      for(var index in $localStorage.checkCharCamp) {
        if ($localStorage.checkCharCamp[index] == true) {
          tempIndex.push(index);
        }
      }
      vm.by = tempIndex.join();
    } else {
      tempIndex = [];
      for(var index in $localStorage.checkCharCamp) {
        if ($localStorage.checkCharCamp[index] == true) {
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
            break;
          }
        }
      });

    /** BIG DIAGRAM  - START **/
    vm.types = ['line', 'stackedLine', 'fullStackedLine'];


    vm.series = [{
      argumentField: "day",
      valueField: "impression"
    }, {
      argumentField: "day",
      valueField: "cpa"
    }, {
      argumentField: "day",
      valueField: "cpc"
    }, {
      argumentField: "day",
      valueField: "clicks"
    }, {
      argumentField: "day",
      valueField: "mediaspent"
    }, {
      argumentField: "day",
      valueField: "conversions"
    }, {
      argumentField: "day",
      valueField: "ctr"
    }];

    vm.chartOptionsFirst = {
      argumentAxis: {
        valueMarginsEnabled: false,
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
      commonSeriesSettings: {
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
      size: {
        width: 500,
        height: 230
      },
      bindingOptions: {
        dataSource: 'camp.chartStore'
      },
      series: $localStorage.seriesCamp,
      legend:{
        visible: false
      },
      loadingIndicator: {
        show: true,
        text: "Creating a chart..."
      }
      //   tooltip: {
      //   enabled: true,
      //     customizeTooltip: function (arg) {
      //     return {
      //       text: arg.valueText
      //     };
      //   }
      // }
    };

    vm.rangeOptionsFirst = {
      size: {
        height: 100,
        width: 500
      },
      margin: {
        left: 10
      },
      scale: {
        minorTickCount:1
      },
      bindingOptions: {
        dataSource: 'camp.chartStore'
      },
      chart: {
        series: $localStorage.seriesCamp
      },
      behavior: {
        callSelectedRangeChanged: "onMoving"
      },
      onSelectedRangeChanged: function (e) {
        var zoomedChart = $("#zoomedContainerFirst #zoomedChartFirst").dxChart("instance");
         zoomedChart.zoomArgument(e.startValue, e.endValue);
      }
    };

    // applyBindings(model, $("#zoomedContainer")[0]);

    /** BIG DIAGRAM  - END **/
    vm.totals = [];
    vm.chartStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.statsChart(vm.dataStart, vm.dataEnd,vm.by)
          .then(function (result) {
            return result;
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
      value: $localStorage.checkCharCamp.impressions? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.impressions = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "impression"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.impressions = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'impression') {
              $localStorage.seriesCamp.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };



    vm.CPA = {
      text: LC('MAIN.CHECKBOX.CPA'),
      value: $localStorage.checkCharCamp.cpa? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.cpa = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "cpa"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.cpa = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'cpa') {
              $localStorage.seriesCamp.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };

    vm.CPC = {
      text: LC('MAIN.CHECKBOX.CPC'),
      value: $localStorage.checkCharCamp.cpc? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.cpc = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "cpc"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.cpc = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'cpc') {
              $localStorage.seriesCamp.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };

    vm.clicks = {
      text: LC('MAIN.CHECKBOX.CLICKS'),
      value: $localStorage.checkCharCamp.clicks? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.clicks = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "clicks"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.clicks = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'clicks') {
              $localStorage.seriesCamp.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.media = {
      text: LC('MAIN.CHECKBOX.MEDIA_SPENT'),
      value: $localStorage.checkCharCamp.mediaspent? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.mediaspent = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "mediaspent"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.mediaspent = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'mediaspent') {
              $localStorage.seriesCamp.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.conversions = {
      text: LC('MAIN.CHECKBOX.CONVERSIONS'),
      value: $localStorage.checkCharCamp.conversions? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.conversions = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "conversions"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.conversions = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'conversions') {
              $localStorage.seriesCamp.splice(index, 1);
            }
          }
          $state.reload();
        }
      }
    };
    vm.CTR = {
      text: LC('MAIN.CHECKBOX.CTR'),
      value: $localStorage.checkCharCamp.ctr? true:false,
      onValueChanged: function (e) {
        if (e.value == true) {
          $localStorage.checkCharCamp.ctr = true;
          $localStorage.seriesCamp.push({
            argumentField: "day",
            valueField: "ctr"
          });
          $state.reload();
        } else {
          $localStorage.checkCharCamp.ctr = false;
          for(var index in $localStorage.seriesCamp) {
            if ($localStorage.seriesCamp[index].valueField == 'ctr') {
              $localStorage.seriesCamp.splice(index, 1);
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

    vm.dataSourceSecond = [{
      "Date": "03/12/2013",
      "Open": "827.90",
      "High": "830.69",
      "Low": "822.31",
      "Close": "825.31",
      "Volume": "1641413"
    },{
      "Date": "03/13/2013",
      "Open": "826.99",
      "High": "826.99",
      "Low": "817.39",
      "Close": "821.54",
      "Volume": "1651111"
    }, {
      "Date": "03/14/2013",
      "Open": "818.50",
      "High": "820.30",
      "Low": "813.34",
      "Close": "814.30",
      "Volume": "3099791"
    },  {
      "Date": "03/17/2013",
      "Open": "805.00",
      "High": "812.76",
      "Low": "801.47",
      "Close": "807.79",
      "Volume": "1838552"
    }, {
      "Date": "03/18/2013",
      "Open": "811.24",
      "High": "819.25",
      "Low": "806.45",
      "Close": "811.32",
      "Volume": "2098176"

    }, {
      "Date": "03/19/2013",
      "Open": "816.83",
      "High": "817.51",
      "Low": "811.44",
      "Close": "814.71",
      "Volume": "1464122"
    }, {
      "Date": "03/20/2013",
      "Open": "811.29",
      "High": "816.92",
      "Low": "809.85",
      "Close": "811.26",
      "Volume": "1477590"
    }, {
      "Date": "03/21/2013",
      "Open": "814.74",
      "High": "815.24",
      "Low": "809.64",
      "Close": "810.31",
      "Volume": "1491678"
    }, {
      "Date": "03/24/2013",
      "Open": "812.41",
      "High": "819.23",
      "Low": "806.82",
      "Close": "809.64",
      "Volume": "1712684"
    }, {
      "Date": "03/25/2013",
      "Open": "813.50",
      "High": "814.00",
      "Low": "807.79",
      "Close": "812.42",
      "Volume": "1191912"
    }, {
      "Date": "03/26/2013",
      "Open": "806.68",
      "High": "807.00",
      "Low": "801.33",
      "Close": "802.66",
      "Volume": "2163295"
    }, {
      "Date": "03/27/2013",
      "Open": "803.99",
      "High": "805.37",
      "Low": "793.30",
      "Close": "794.19",
      "Volume": "2287712"
    }, {
      "Date": "03/31/2013",
      "Open": "795.01",
      "High": "802.25",
      "Low": "793.25",
      "Close": "801.19",
      "Volume": "1807580"
    }, {
      "Date": "04/01/2013",
      "Open": "804.54",
      "High": "814.83",
      "Low": "804.00",
      "Close": "813.04",
      "Volume": "2041713"
    }, {
      "Date": "04/02/2013",
      "Open": "813.46",
      "High": "814.20",
      "Low": "800.67",
      "Close": "806.20",
      "Volume": "1738753"
    }, {
      "Date": "04/03/2013",
      "Open": "804.25",
      "High": "805.75",
      "Low": "791.30",
      "Close": "795.07",
      "Volume": "2448102"
    }, {
      "Date": "04/04/2013",
      "Open": "786.06",
      "High": "786.99",
      "Low": "776.40",
      "Close": "783.05",
      "Volume": "3433994"
    }, {
      "Date": "04/07/2013",
      "Open": "778.75",
      "High": "779.55",
      "Low": "768.40",
      "Close": "774.85",
      "Volume": "2832718"
    }, {
      "Date": "04/08/2013",
      "Open": "775.50",
      "High": "783.75",
      "Low": "773.11",
      "Close": "777.65",
      "Volume": "2157928"
    }, {
      "Date": "04/09/2013",
      "Open": "782.92",
      "High": "792.35",
      "Low": "776.00",
      "Close": "790.18",
      "Volume": "1978862"
    }, {
      "Date": "04/10/2013",
      "Open": "792.88",
      "High": "793.10",
      "Low": "784.06",
      "Close": "790.39",
      "Volume": "2028766"
    }, {
      "Date": "04/11/2013",
      "Open": "791.99",
      "High": "792.10",
      "Low": "782.93",
      "Close": "790.05",
      "Volume": "1636829"
    }, {
      "Date": "04/14/2013",
      "Open": "785.95",
      "High": "797.00",
      "Low": "777.02",
      "Close": "781.93",
      "Volume": "2454767"
    }, {
      "Date": "04/15/2013",
      "Open": "786.59",
      "High": "796.00",
      "Low": "783.92",
      "Close": "793.37",
      "Volume": "1742374"
    }, {
      "Date": "04/16/2013",
      "Open": "786.75",
      "High": "790.84",
      "Low": "778.10",
      "Close": "782.56",
      "Volume": "2037355"
    }, {
      "Date": "04/17/2013",
      "Open": "785.35",
      "High": "785.80",
      "Low": "761.26",
      "Close": "765.91",
      "Volume": "3328777"
    }];

    vm.chartOptionsSecond = {
      dataSource: vm.dataSourceSecond,
      commonSeriesSettings: {
        type: 'candleStick'
      },
      size: {
        height: 205,
        width:500
      },
      valueAxis: {
        valueType: 'numeric'
      },
      argumentAxis: {
        valueMarginsEnabled: false,
        grid: {
          visible: true
        },
        label: {
          visible: false
        },
        argumentType: 'datetime'
      },
      tooltip: {
        enabled: true
      },
      legend: {
        visible: false
      },
      useAggregation: true,
      series: [{
        openValueField: 'Open',
        highValueField: 'High',
        lowValueField: 'Low',
        closeValueField: 'Close',
        argumentField: 'Date'
      }]
    };

    vm.rangeOptionsSecond = {
      size: {
        height: 100,
        width: 500
      },
      margin: {
        left: 10
      },
      scale: {
        minorTickCount:'day',
        valueType: 'date',
        tickInterval: 'day'
      },
      dataSource: vm.dataSourceSecond,
      chart: {
        series: {
          type: 'line',
          valueField: 'Open',
          argumentField: 'Date',
          placeholderHeight: 20
        },
        useAggregation: true,
        valueAxis: { valueType: 'numeric' }
      },

      behavior: {
        callSelectedRangeChanged: "onMoving",
        snapToTicks: false
      },
      onSelectedRangeChanged: function (e) {
        var zoomedChart = $("#zoomedContainerSecond #zoomedChartSecond").dxChart("instance");
        zoomedChart.zoomArgument(new Date(e.startValue), new Date(e.endValue));
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

    vm.state='';
    vm.selectCell = {
      dataSource: [
        {'name': 'White List'},
        {'name': 'Black List'},
        {'name': 'Suspended'}
      ],
      placeholder: 'Select a state',
      displayExpr: 'name',
      valueExpr: vm.state
    };


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
          caption: 'State',
          width: 300,
          columnIndex: 16,
          headerCellTemplate: 'headerCellTemplate',
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
                //console.log(e);
                var parentWhiteBtn = e.element[0].parentNode;
                //console.log(parentWhiteBtn);
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
      placement:{
        btn:'Placement',
        header:'Placement'
      },
      creativeId: {
        btn:'creative_id',
        header:'creative_id'},
      creativeSize: {
        btn:'creative_size',
        header:'creative_size'
      },
      viewability: {
        btn:'viewability',
        header:'viewability'
      },
      os: {
        btn:'OS',
        header:'Operating System used'
      },
      carrier: {
        btn:'carrier',
        header:'carrier'
      },
      networkSeller: {
        btn:'network(seller)',
        header:'network (seller)'
      },
      connectionType: {
        btn:'connection_type',
        header:'connection_type'
      },
      device: {
        btn:'device',
        header:'device'
      },
      extra: {
        btn:'extra',
        header:'extra'
      },
      publisher: {
        btn:'Publisher',
        header:'Publisher'
      }
    };
    vm.pieChartHeader = $localStorage.pieChartHeader || vm.ctrlBbtns.os.header;
    vm.btnsNodesArray = $('.label-container')[0].children;


    /** SELECT SECTION/BTN UNDER LOADING PAGE - START **/
    for(var key in vm.ctrlBbtns) {
      if (vm.ctrlBbtns[key].header == vm.pieChartHeader) {
        vm.selectedSection = vm.ctrlBbtns[key].btn
      }
    }

    Array.prototype.forEach.call(vm.btnsNodesArray, function(node) {
      if (node.name == vm.selectedSection) {
        node.classList.add('nav-btn-active');
      }
    });
    /** SELECT SECTION/BTN UNDER LOADING PAGE - END **/


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

    };

    if(!vm.targetCpa) {
      vm.targetCpa = $localStorage.targetCpa || 3;
      $localStorage.targetCpa = vm.targetCpa;
    }

    vm.backetsRanges = {
      first:{
        min: 0,
        max: Number(vm.targetCpa).toFixed(1)
      },
      second:{
        min:Number(vm.targetCpa).toFixed(1),
        max:Number(vm.targetCpa*2).toFixed(1)
      },
      third: {
        min: Number(vm.targetCpa * 2).toFixed(1),
        max: Number(vm.targetCpa * 3).toFixed(1)
      },
      fourth: {
        min: Number(vm.targetCpa * 3).toFixed(1),
        max: Number(vm.targetCpa * 1000).toFixed(1)
      }
    };

    vm.targetCpaChange = function($event) {
      var targetCpaInt = Number($event.currentTarget.value);
      $localStorage.targetCpa = targetCpaInt;
      vm.backetsRanges = {
        first: {
          min: 0,
          max: (targetCpaInt).toFixed(1)
        },
        second: {
          min: (targetCpaInt).toFixed(1),
          max: (targetCpaInt * 2).toFixed(1)
        },
        third: {
          min: (targetCpaInt * 2).toFixed(1),
          max: (targetCpaInt * 3).toFixed(1)
        },
        fourth: {
          min: (targetCpaInt * 3).toFixed(1),
          max: (targetCpaInt * 1000).toFixed(1)
        }
      };
      vm.cpaArrayFirst =  Camp.cpaBuckets(vm.backetsRanges.first.min, vm.backetsRanges.first.max);
      vm.cpaArraySecond =  Camp.cpaBuckets(vm.backetsRanges.second.min, vm.backetsRanges.second.max);
      vm.cpaArrayThird =  Camp.cpaBuckets(vm.backetsRanges.third.min, vm.backetsRanges.third.max);
      vm.cpaArrayFourth =  Camp.cpaBuckets(vm.backetsRanges.fourth.min, vm.backetsRanges.fourth.max);


      return vm.backetsRanges;
    };

    vm.cpaArrayFirst =  Camp.cpaBuckets(vm.backetsRanges.first.min, vm.backetsRanges.first.max);
    vm.cpaArraySecond =  Camp.cpaBuckets(vm.backetsRanges.second.min, vm.backetsRanges.second.max);
    vm.cpaArrayThird =  Camp.cpaBuckets(vm.backetsRanges.third.min, vm.backetsRanges.third.max);
    vm.cpaArrayFourth =  Camp.cpaBuckets(vm.backetsRanges.fourth.min, vm.backetsRanges.fourth.max);


    vm.pieChartAll = {
      title: {
        text: "All",
        font: {
          size: 20
        },
        margin: {
          bottom: 1
        }
      },
      dataSource: [{
        os: "Android",
        data: 60
      }, {
        os: "iOs",
        data: 30
      }, {
        os: "Windows",
        data: 10
      }],
      series: [{
        argumentField: "os",
        valueField: "data",
        label: {
          visible: true,
          connector: {
            visible: true,
            width: 0.5
          },
          format: "fixedPoint",
          customizeText: function (point) {
            return point.argumentText + ": " + point.valueText + "%";
          }
        },
        smallValuesGrouping: {
          mode: "smallValueThreshold",
          threshold: 4.5
        }
      }],
      legend: {
        horizontalAlignment: "center",
        verticalAlignment: "bottom"
      },
      size: {
        width:370,
        height:300
      }
    };

    vm.pieChartConversions = {
      title: {
        text: "Conversions",
        font: {
          size: 20
        },
        margin: {
          bottom: 1
        }
      },
      dataSource: [{
        os: "Android",
        data: 23
      }, {
        os: "iOs",
        data: 72
      }, {
        os: "Windows",
        data:5
      }],
      series: [{
        argumentField: "os",
        valueField: "data",
        label: {
          visible: true,
          connector: {
            visible: true,
            width: 0.5
          },
          format: "fixedPoint",
          customizeText: function (point) {
            return point.argumentText + ": " + point.valueText + "%";
          }
        },
        smallValuesGrouping: {
          mode: "smallValueThreshold",
          threshold: 4.5
        }
      }],
      legend: {
        horizontalAlignment: "center",
        verticalAlignment: "bottom"
      },
      size: {
        width:370,
        height:300
      }
    }
  }
})();
