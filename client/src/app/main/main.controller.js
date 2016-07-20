(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('MainController', MainController);

  /** @ngInject */
  function MainController($window, $state, $timeout, $localStorage, $translate, Main) {
    var vm = this;
    vm.advertiser = $localStorage.advertiser;
    vm.Main = Main;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.Init = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';
    var LC = $translate.instant;
    /** LOCAL STORAGE CHECKBOX - START **/


    if ($localStorage.checkChart == null ) {
      $localStorage.checkChart = {
        'imp': true,
        'cvr': false,
        'cpc': false,
        'clicks': false,
        'spend': false,
        'conv': false,
        'ctr': false
      };
    }
    vm.chartSeries = [
      { valueField: 'imp', name: 'Impressions', axis:'imp', visible: $localStorage.checkChart.imp }, //yes
      { valueField: 'cvr', name: 'CVR', axis:'cvr', visible: $localStorage.checkChart.cvr },  //NET
      { valueField: 'cpc', name: 'CPC', axis:'CPC', visible: $localStorage.checkChart.cpc },  //yes
      { valueField: 'clicks', name: 'clicks', axis:'clicks', visible: $localStorage.checkChart.clicks }, //yes
      { valueField: 'spend', name: 'media', axis:'spend', visible: $localStorage.checkChart.spend },//yes
      { valueField: 'conv', name: 'conversions', axis:'conv', visible: $localStorage.checkChart.conv },//yes
      { valueField: 'ctr', name: 'CTR', axis:'ctr', visible: $localStorage.checkChart.ctr } //yes
    ];
    /** LOCAL STORAGE CHECKBOX - END **/



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

    /** BINDING OPTIONS - START **/
    vm.totals = [];

    vm.chartStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Main.statsChart(vm.advertiser.id, vm.dataStart, vm.dataEnd,vm.by)
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
        return vm.Main.statsCampaigns(vm.advertiser.id, vm.dataStart, vm.dataEnd, loadOptions.skip,
          loadOptions.take, loadOptions.sort, loadOptions.order,
          vm.by ,loadOptions.filter)
        .then(function (result) {
          vm.multipleTotalCount = result.totalCount;
          return result.campaigns;
        });
      }
    });



    /** BINDING OPTIONS - END **/

    /** TOTALS - START **/
    vm.Main.statsTotals(vm.advertiser.id, vm.dataStart, vm.dataEnd)
    .then(function (result) {
      vm.totals.imp = result.imp.toString().split( /(?=(?:\d{3})+(?!\d))/ ).join();
      vm.totals.spent = result.spend.toFixed(2);
      vm.totals.conv = result.conv;
      vm.totals.cpc = result.cpc;
      vm.totals.cpm = result.cpm;
      vm.totals.cvr = result.cvr;
      vm.totals.ctr = result.ctr;
    });
    /** TOTALS - END **/

    /** MULTIPLE - START **/
    vm.selectedItems = [];
    vm.chartOptionsFuncgrid = [];
    vm.dataGridOptionsMultiple = {
      bindingOptions: {
        dataSource: 'main.multipleStore'
      },
      onInitialized: function (data) {
        vm.dataGridOptionsMultipleFunc = data.component;
        /*vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 15;*/
      },
      showBorders: true,
      alignment: 'left',
      headerFilter: {
        visible: true
      },
      filterRow: {
        visible: true,
        applyFilter: "auto"
      },
      export: {
        enabled: true,
        fileName: "Employees"
      },
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      columnChooser: {
        enabled: true
      },
      columnFixing: {
        enabled: true
      },
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
          caption: LC('MAIN.CAMPAIGN.COLUMNS.CAMPAIGN'),
          dataField: 'campaign',
          fixed: true,
          cellTemplate: function (container, options) {
            container.addClass('a-campaign');
            $window.angular.element('<a href="#/home/campaign/'+ options.data.id +'">' + options.data.campaign + '</a>')
            .appendTo(container);
          }
        },
        {
          caption: LC('MAIN.CAMPAIGN.COLUMNS.SPENT'),
          dataField: 'spend'
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
          width: 200,
          dataField: LC('MAIN.CAMPAIGN.COLUMNS.STATS'),
          cellTemplate: function (container, options) {
            if (options.data.chart) {
              var chartOptions = {
                onInitialized: function (data) {
                  vm.chartOptionsFuncgrid[options.rowIndex] = data.component;
                },
                dataSource: options.data.chart,
                size: {
                  height: 80,
                  width: 185
                },
                commonSeriesSettings: {
                  argumentField: 'day',
                  type: 'line',
                  point: {
                    size: 2,
                    hoverStyle: {
                      border: {
                        visible: true,
                        width: 1
                      },
                      size: 4
                    }
                  }
                },
                commonAxisSettings: {
                  label: {
                    visible: false
                  },
                  grid: { visible: false }
                },
                valueAxis: [
                  { name: 'imp'},
                  { name: 'cvr'},
                  { name: 'CPC' },
                  { name: 'clicks' },
                  { name: 'spend' },
                  { name: 'conv' },
                  { name: 'ctr' }
                ],
                argumentAxis: {
                  valueMarginsEnabled: false,
                  discreteAxisDivisionMode: 'crossLabels',
                  grid: {
                    visible: false
                  },
                  label: {
                    visible: false
                  },
                  minorGrid: {
                    visible: false
                  },
                  minorTick: {
                    visible: false
                  },
                  tick: {
                    visible: false
                  }
                },
                series: vm.chartSeries,
                legend: {
                  visible: false
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
              container.addClass('img-container');
              var chart = $window.$('<div class="chartMulti" ></div>');
              chart.dxChart(chartOptions);
              chart.appendTo(container);
            } else {
              container.addClass('img-container');
              $window.$('<div id="chartMulti" ></div>')

              //.attr("src", options.value)
              .appendTo(container);
            }


          }
        }],
      // selection: {
      //   mode: 'multiple'
      // },
      onSelectionChanged: function (data) {
        vm.selectedItems = data.selectedRowsData;
        vm.disabled = !vm.selectedItems.length;
      }
    };
    /** MULTIPLE - END **/

    /** BIG DIAGRAM  - START **/
    vm.types = ['line', 'stackedLine', 'fullStackedLine'];

    vm.chartOptions = {
      onInitialized: function (data) {
        vm.chartOptionsFunc = data.component;
      },
      series: vm.chartSeries,
      bindingOptions: {
        dataSource: 'main.chartStore'
      },
      commonSeriesSettings: {
        argumentField: 'day',
        type: 'Line',
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
      },crosshair: {
        enabled: true,
        color: 'deepskyblue',
        label: {
          visible: true
        }
      },
      commonAxisSettings:{
        valueMarginsEnabled: true
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
      valueAxis: [
        { name: 'imp',
          position: 'left'
        },
        { name: 'cvr',
          position: 'left'},
        { name: 'CPC',
          position: 'left' },
        { name: 'clicks',
          position: 'left' },
        { name: 'spend',
          position: 'left' },
        { name: 'conv',
          position: 'left'},
        { name: 'ctr',
          position:'left' }
      ],
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

    /**
     * @param seriesName {string}
     * @param seriesShortName {string}
     * @param selected {boolean}
     */
    vm.updateCharts = function (seriesName, seriesShortName, selected) {
      var gridCharts = {};
      $localStorage.checkChart[seriesShortName] = selected;
      var i = 0;
      if (selected) {
        vm.chartOptionsFunc.getSeriesByName(seriesName).show();
        gridCharts = $window.$('.chartMulti');
        for(i = 0; i < gridCharts.length; i++) {
          $window.$(gridCharts[i]).dxChart('instance').getSeriesByName(seriesName).show();
        }
      } else {
        vm.chartOptionsFunc.getSeriesByName(seriesName).hide();
        gridCharts = $window.$('.chartMulti');
        for(i = 0; i < gridCharts.length; i++) {
          $window.$(gridCharts[i]).dxChart('instance').getSeriesByName(seriesName).hide();
        }
      }
    };

    /** CHECKBOX CHART - START **/

    vm.onlyTwo = function(value) {
      var i=0;
      var checkTrue = [];
      var checkFalse = [];
      for(i = 0; i < vm.Init.length; i++) {
        if (vm.Init[i]._options.value == true) {
          checkTrue.push(vm.Init[i]);
        } else {
          checkFalse.push(vm.Init[i]);
        }
      }
      if (value == true) {
        if (checkTrue.length == 2 && checkFalse.length>4) {
          for(i = 0; i < checkFalse.length; i++) {
            checkFalse[i].option('disabled', true);
          }
        }
      } else {
        if (checkTrue.length <= 2) {
          for(i = 0; i < checkFalse.length; i++) {
            checkFalse[i].option('disabled', false);
          }
        }
      }
    };

    function CheckLocalStorage () {
      for (var i in $localStorage.checkChart) {
        if ($localStorage.checkChart[i] == true) {
          if (i == 'imp') {
            vm.chartOptionsFunc.getSeriesByName('Impressions').show();
          }else if (i == 'cvr') {
            vm.chartOptionsFunc.getSeriesByName('CVR').show();
          } else if (i == 'cpc') {
            vm.chartOptionsFunc.getSeriesByName('CPC').show();
          } else if (i == 'clicks') {
            vm.chartOptionsFunc.getSeriesByName('clicks').show();
          } else if (i == 'spend') {
            vm.chartOptionsFunc.getSeriesByName('media').show();
          } else if (i == 'conv') {
            vm.chartOptionsFunc.getSeriesByName('conversions').show();
          } else if (i == 'ctr') {
            vm.chartOptionsFunc.getSeriesByName('CTR').show();
          }
        } else if ($localStorage.checkChart[i] == false) {
          if (i == 'imp') {
            vm.chartOptionsFunc.getSeriesByName('Impressions').hide();
          }else if (i == 'cvr') {
            vm.chartOptionsFunc.getSeriesByName('CVR').hide();
          } else if (i == 'cpc') {
            vm.chartOptionsFunc.getSeriesByName('CPC').hide();
          } else if (i == 'clicks') {
            vm.chartOptionsFunc.getSeriesByName('clicks').hide();
          } else if (i == 'spend') {
            vm.chartOptionsFunc.getSeriesByName('media').hide();
          } else if (i == 'conv') {
            vm.chartOptionsFunc.getSeriesByName('conversions').hide();
          } else if (i == 'ctr') {
            vm.chartOptionsFunc.getSeriesByName('CTR').hide();
          }
        }
      }
    }


    vm.impressions = {
      text: LC('MAIN.CHECKBOX.IMPRESSIONS'),
      value: $localStorage.checkChart.imp,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        //vm.updateCharts('Impressions', 'imp', e.value);
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'right'
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'CPC',
            position: 'left'
          },
          {
            name: 'clicks',
            position: 'left'
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'conv',
            position: 'left'
          },
          {
            name: 'ctr',
            position: 'left'
          }
        ]);

        vm.updateCharts('Impressions', 'imp', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };

    vm.CPA = {
      text: LC('MAIN.CHECKBOX.CPA'),
      value: $localStorage.checkChart.cvr,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'left'
          },
          {
            name: 'cvr',
            position: 'right'
          },
          {
            name: 'CPC',
            position: 'left'
          },
          {
            name: 'clicks',
            position: 'left'
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'conv',
            position: 'left'
          },
          {
            name: 'ctr',
            position: 'left'
          }
        ]);

        vm.updateCharts('CVR', 'cvr', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };

    vm.CPC = {
      text: LC('MAIN.CHECKBOX.CPC'),
      value: $localStorage.checkChart.cpc,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'left'
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'CPC',
            position: 'right'
          },
          {
            name: 'clicks',
            position: 'left'
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'conv',
            position: 'left'
          },
          {
            name: 'ctr',
            position: 'left'
          }
        ]);
        vm.updateCharts('CPC', 'cpc', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };
    vm.clicks = {
      text: LC('MAIN.CHECKBOX.CLICKS'),
      value: $localStorage.checkChart.clicks,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'left'
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'CPC',
            position: 'left'
          },
          {
            name: 'clicks',
            position: 'right'
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'conv',
            position: 'left'
          },
          {
            name: 'ctr',
            position: 'left'
          }
        ]);
        vm.updateCharts('clicks', 'clicks', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };
    vm.media = {
      text: LC('MAIN.CHECKBOX.MEDIA_SPENT'),
      value: $localStorage.checkChart.spend,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'left'
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'CPC',
            position: 'left'
          },
          {
            name: 'clicks',
            position: 'left'
          },
          {
            name: 'spend',
            position: 'right'
          },
          {
            name: 'conv',
            position: 'left'
          },
          {
            name: 'ctr',
            position: 'left'
          }
        ]);
        vm.updateCharts('media', 'spend', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };
    vm.conversions = {
      text: LC('MAIN.CHECKBOX.CONVERSIONS'),
      value: $localStorage.checkChart.conv,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'left'
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'CPC',
            position: 'left'
          },
          {
            name: 'clicks',
            position: 'left'
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'conv',
            position: 'right'
          },
          {
            name: 'ctr',
            position: 'left'
          }
        ]);
        vm.updateCharts('conversions', 'conv', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };
    vm.CTR = {
      text: LC('MAIN.CHECKBOX.CTR'),
      value: $localStorage.checkChart.ctr,
      onInitialized: function (data) {
        vm.Init.push(data.component);
      },
      onValueChanged: function (e) {
        var chart = $('#chart').dxChart('instance');
        chart.option('valueAxis', [
          {
            name: 'imp',
            position: 'left'
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'CPC',
            position: 'left'
          },
          {
            name: 'clicks',
            position: 'left'
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'conv',
            position: 'left'
          },
          {
            name: 'ctr',
            position: 'right'
          }
        ]);
        vm.updateCharts('CTR', 'ctr', e.value);
        vm.onlyTwo(e.value);
        CheckLocalStorage();
      }
    };

    $timeout(function(){
      var i = 0;
      var checkTrue = [];
      var checkFalse = [];
      for(i= 0; i < vm.Init.length; i++) {
        if (vm.Init[i]._options.value == true) {
          checkTrue.push(vm.Init[i]);
        } else {
          checkFalse.push(vm.Init[i]);
        }
      }
      if (checkTrue.length >= 2 && checkFalse.length>4) {
        for(i = 0; i < checkFalse.length; i++) {
          checkFalse[i].option('disabled', true);
        }
      }

  });

/** CHECKBOX CHART - END **/

    /** MAP CLICKS - START **/
    var clicksByCountry = {};

    vm.Main.statsMap(vm.advertiser.id, vm.dataStart, vm.dataEnd).then(function (res) {
      clicksByCountry = res;
      $window.$('#visualMap').dxVectorMap(vm.vectorMapOptions);
    });

    vm.vectorMapOptions = {
      size: {
        height: 320
      },
      layers: [{
        name: 'areas',
        dataSource: $window.DevExpress.viz.map.sources.world,
        palette: 'blue',
        colorGroups: [0, 100, 1000, 10000],
        colorGroupingField: 'clicks',
        label: {
          enabled: true,
          dataField: 'name'
        },
        customize: function (elements) {
          elements.forEach(function (element) {
            var name = element.attribute('name');
            var clicks = clicksByCountry[name];
            if (clicks) {
              element.attribute('clicks', clicks);
            }
          });
        }
      }],
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          if (arg.attribute('clicks')) {
            return { text: arg.attribute('name') + ": " + arg.attribute('clicks')};
          } else {
            return { text: arg.attribute('name')};
          }
        }
      },
      legends: [{
        source: { layer: 'areas', grouping: 'color' },
        horizontalAlignment: 'left',
        verticalAlignment: 'bottom',
        customizeText: function (arg) {
          return arg.start + ' to ' + arg.end + ' clicks';
        }
      }],
      bounds: [-180, 85, 180, -75]
    };
    /** MAP CLICKS - START **/

  }
})();
