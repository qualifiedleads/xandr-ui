(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($window, $state, $localStorage, $translate, Main) {
    var vm = this;
    vm.advertiser = $localStorage.advertiser;
    vm.Main = Main;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.by = '';
    var LC = $translate.instant;
    /** LOCAL STORAGE CHECKBOX - START **/

    var index;
    if ($localStorage.series == null ){
      $localStorage.series = [
        { valueField: 'imp', name: 'Impressions' }, //yes
        { valueField: 'cvr', name: 'CVR' },  //NET
        { valueField: 'cpc', name: 'CPC' },  //yes
        { valueField: 'clicks', name: 'clicks' }, //yes
        { valueField: 'spend', name: 'media' },//yes
        { valueField: 'conv', name: 'conversions' },//yes
        { valueField: 'ctr', name: 'CTR' } //yes
      ];
    }
    //$localStorage.checkChart = null;
    var tempIndex = [];
    if ($localStorage.checkChart == null ) {
      $localStorage.checkChart = {
        'imp': true,
        'cvr': true,
        'cpc':true,
        'clicks': true,
        'spend': true,
        'conv': true,
        'ctr': true
      };
      tempIndex = [];
      for(index in $localStorage.checkChart) {
        if ($localStorage.checkChart[index] == true) {
          tempIndex.push(index);
        }
      }
      vm.by = tempIndex.join();
    } else {
      tempIndex = [];
      for(index in $localStorage.checkChart) {
        if ($localStorage.checkChart[index] == true) {
          tempIndex.push(index);
        }
      }
      vm.by = tempIndex.join();
    }
    vm.chartSeries = [
      { valueField: 'imp', name: 'Impressions', visible: $localStorage.checkChart.imp }, //yes
      { valueField: 'cvr', name: 'CVR', visible: $localStorage.checkChart.cvr },  //NET
      { valueField: 'cpc', name: 'CPC', visible: $localStorage.checkChart.cpc },  //yes
      { valueField: 'clicks', name: 'clicks', visible: $localStorage.checkChart.clicks }, //yes
      { valueField: 'spend', name: 'media', visible: $localStorage.checkChart.spend },//yes
      { valueField: 'conv', name: 'conversions', visible: $localStorage.checkChart.conv },//yes
      { valueField: 'ctr', name: 'CTR', visible: $localStorage.checkChart.ctr } //yes
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

    vm.gridCharts = [];
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
            vm.gridCharts = [];
            for (var i = 0; i < result.campaigns.length; i++) {
              vm.gridCharts.push(result.campaigns[i].chart);
            }
            return result.campaigns;
          });
      }
    });
    /** BINDING OPTIONS - END **/

    /** TOTALS - START **/
    vm.Main.statsTotals(vm.advertiser.id, vm.dataStart, vm.dataEnd)
      .then(function (result) {
        vm.totals.spent = result.spend;
        vm.totals.conv = result.conv;
        vm.totals.imp = result.imp;
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
        vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 15;
      },
      showBorders: true,
      alignment: 'left',
      headerFilter: {
        visible: true
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
        allowedPageSizes: [3, 30, 50],
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
            console.log(vm.gridCharts)
            if (options.data.chart) {
            var chartOptions = {
              onInitialized: function (data) {
                vm.chartOptionsFuncgrid[options.rowIndex] = data.component;
              },
              bindingOptions: {
                dataSource: '$parent.$parent.main.chartStore'//options.data.chart
              },
              size: {
                height: 80
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
      selection: {
        mode: 'multiple'
      },
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
      size: {
        width: 500,
        height: 230
      },
      bindingOptions: {
        dataSource: 'main.chartStore'
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

    /** CHECKBOX CHART - START **/
    vm.impressions = {
      text: LC('MAIN.CHECKBOX.IMPRESSIONS'),
      value: $localStorage.checkChart.imp,
      onValueChanged: function (e) {
        vm.updateCharts('Impressions', 'imp', e.value);
      }
    };

    vm.CPA = {
      text: LC('MAIN.CHECKBOX.CPA'),
      value: $localStorage.checkChart.cvr,
      onValueChanged: function (e) {
        vm.updateCharts('CVR', 'cvr', e.value);
      }
    };

    vm.CPC = {
      text: LC('MAIN.CHECKBOX.CPC'),
      value: $localStorage.checkChart.cpc,
      onValueChanged: function (e) {
        vm.updateCharts('CPC', 'cpc', e.value);
      }
    };
    vm.clicks = {
      text: LC('MAIN.CHECKBOX.CLICKS'),
      value: $localStorage.checkChart.clicks,
      onValueChanged: function (e) {
        vm.updateCharts('clicks', 'clicks', e.value);
      }
    };
    vm.media = {
      text: LC('MAIN.CHECKBOX.MEDIA_SPENT'),
      value: $localStorage.checkChart.spend,
      onValueChanged: function (e) {
        vm.updateCharts('media', 'spend', e.value);
      }
    };
    vm.conversions = {
      text: LC('MAIN.CHECKBOX.CONVERSIONS'),
      value: $localStorage.checkChart.conv,
      onValueChanged: function (e) {
        vm.updateCharts('conversions', 'conv', e.value);
      }
    };
    vm.CTR = {
      text: LC('MAIN.CHECKBOX.CTR'),
      value: $localStorage.checkChart.ctr,
      onValueChanged: function (e) {
        vm.updateCharts('CTR', 'ctr', e.value);
      }
    };
    /** CHECKBOX CHART - END **/

	  /**
     * @param seriesName {string}
     * @param seriesShortName {string}
     * @param selected {boolean}
     */
    vm.updateCharts = function (seriesName, seriesShortName, selected) {
      vm.chartStore.load();
      $localStorage.checkChart[seriesShortName] = selected;
      if (selected) {
        vm.chartOptionsFunc.getSeriesByName(seriesName).show();
        var gridCharts = $window.$('.chartMulti');
        for(var i = 0; i < gridCharts.length; i++) {
          $window.$(gridCharts[i]).dxChart('instance').getSeriesByName(seriesName).show();
        }
      } else {
        $localStorage.checkChart.imp = false;
        vm.chartOptionsFunc.getSeriesByName(seriesName).hide();
        var gridCharts = $window.$('.chartMulti');
        for(var i = 0; i < gridCharts.length; i++) {
          $window.$(gridCharts[i]).dxChart('instance').getSeriesByName(seriesName).hide();
        }
      }
    };

    /** MAP CLICKS - START **/
    var clicksByCountry = {};

    vm.Main.statsMap(vm.advertiser.id, vm.dataStart, vm.dataEnd).then(function (res) {
      clicksByCountry = res;
      $window.$('#visualMap').dxVectorMap(vm.vectorMapOptions);
    });

    vm.vectorMapOptions = {
      size: {
        width: 500,
        height: 350
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
          return { text: arg.attribute('text') };
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
