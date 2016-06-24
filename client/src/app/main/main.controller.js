(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($window, $state, $localStorage, $translate, $log, Main) {
    var vm = this;
    vm.Main = Main;
    var LC = $translate.instant;
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
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart:  $window.moment({ hour: '00' }).subtract(7, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.CURRENT_WEEK'),
        dataStart: $window.moment().startOf('week').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_WEEK'),
        dataStart: $window.moment().startOf('week').subtract(1, 'week').unix(),
        dataEnd: $window.moment().startOf('week').unix()
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.CURRENT_MONTH'),
        dataStart: $window.moment().startOf('month').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 5,
        Name: LC('MAIN.DATE_PICKER.LAST_MONTH'),
        dataStart: $window.moment().subtract(1, 'month').startOf('month').unix(),
        dataEnd: $window.moment().subtract(1, 'month').endOf('month').unix()
      }, {
        ID: 6,
        Name: LC('MAIN.DATE_PICKER.CUSTOM'),
        dataStart: '',
        dataEnd: ''
      }];
    vm.datePiker = {
      items: products,
      displayExpr: 'Name',
      valueExpr: 'ID',
      value: products[$localStorage.SelectedTime].ID,
      onValueChanged: function (e) {
        $log.info(products[e.value]);
        $localStorage.SelectedTime = e.value;
        $localStorage.dataStart = products[e.value].dataStart;
        $localStorage.dataEnd = products[e.value].dataEnd;

        //$('#gridContainer1').dxDataGrid('instance').refresh();
        //$('#gridContainer2').dxDataGrid('instance').refresh();
        $state.reload();
      }
    };

    vm.result = {};
    vm.totals = [];

    vm.totalsStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Main.statsTotals(vm.dataStart, vm.dataEnd)
          .then(function (result) {
            return [result];
          });
      }
    });

    vm.multipleStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Main.statsCampaigns(vm.dataStart, vm.dataEnd)
          .then(function (result) {
            return result.campaigns;
          });
      }
    });

    vm.chartStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Main.statsChart(vm.dataStart, vm.dataEnd)
          .then(function (result) {
            return result.statistics;
          });
      }
    });



    vm.checkboxData = [];

    vm.dataGridOptionsSingle = {
      bindingOptions: {
        dataSource: 'main.totalsStore'
      },
      showBorders: true,
      alignment: 'left',
      howBorders: true,
      columns: [
        {
          caption: LC('MAIN.TOTALS.COLUMNS.TOTALS'),
          dataField: 'TOTALS'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.SPENT'),
          dataField: 'spend'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.CONV'),
          dataField: 'conv'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.IMP'),
          dataField: 'imp'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.CLICKS'),
          dataField: 'clicks'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.CPC'),
          dataField: 'cpc'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.CPM'),
          dataField: 'cpm'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.CVR'),
          dataField: 'cvr'
        },
        {
          caption: LC('MAIN.TOTALS.COLUMNS.CTR'),
          dataField: 'ctr'
        }]
    };
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
      paging: {
        pageSize: 3
      },
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [3, 10, 20],
        showInfo: true
      },
      howBorders: true,
      showRowLines: true,

      columns: [{
        caption: LC('MAIN.CAMPAIGN.COLUMNS.CAMPAIGN'),
        dataField: 'campaign'
      }, {
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
            var chartOptions = {
              onInitialized: function (data) {
                vm.chartOptionsFuncgrid[options.rowIndex] = data.component;
              },
              dataSource: options.data.statistics,
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
              series: [
                { valueField: 'impressions', name: 'Impressions' },
                { valueField: 'cpa', name: 'CPA' },
                { valueField: 'cpc', name: 'CPC' },
                { valueField: 'clicks', name: 'clicks' },
                { valueField: 'media', name: 'media' },
                { valueField: 'conversions', name: 'conversions' },
                { valueField: 'ctr', name: 'CTR' }
              ],
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
            $window.angular.element('<div id="chartMulti' + options.rowIndex + '" ></div>')

            //.attr("src", options.value)
              .appendTo(container);
            $window.$('#chartMulti' + options.rowIndex).dxChart(chartOptions).dxChart('instance');
          }
        }],
      selection: {
        mode: 'multiple'
      },
      onSelectionChanged: function (data) {
        //console.log(vm.dataGridOptionsMultiple);
        vm.selectedItems = data.selectedRowsData;
        vm.disabled = !vm.selectedItems.length;
      }
    };

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
      series: series,
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
    /** CheckBox Chart **/
    vm.impressions = {
      text: LC('MAIN.CHECKBOX.IMPRESSIONS'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[0].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[0].visible', true);
          });
        } else {
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[0].visible', false);
          });

          vm.chartOptionsFunc.option('series[0].visible', false);
        }
      }
    };
    vm.CPA = {
      text: LC('MAIN.CHECKBOX.CPA'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[1].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[1].visible', true);
          });
        } else {
          vm.chartOptionsFunc.option('series[1].visible', false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[1].visible', false);
          });
        }
      }
    };
    vm.CPC = {
      text: LC('MAIN.CHECKBOX.CPC'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[2].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[2].visible', true);
          });
        } else {
          vm.chartOptionsFunc.option('series[2].visible', false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[2].visible', false);
          });
        }
      }
    };
    vm.clicks = {
      text: LC('MAIN.CHECKBOX.CLICKS'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[3].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[3].visible', true);
          });
        } else {
          vm.chartOptionsFunc.option('series[3].visible', false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[3].visible', false);
          });
        }
      }
    };
    vm.media = {
      text: LC('MAIN.CHECKBOX.MEDIA_SPENT'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[4].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[4].visible', true);
          });
        } else {
          vm.chartOptionsFunc.option('series[4].visible', false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[4].visible', false);
          });
        }
      }
    };
    vm.conversions = {
      text: LC('MAIN.CHECKBOX.CONVERSIONS'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[5].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[5].visible', true);
          });
        } else {
          vm.chartOptionsFunc.option('series[5].visible', false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[5].visible', false);
          });
        }
      }
    };
    vm.CTR = {
      text: LC('MAIN.CHECKBOX.CTR'),
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option('series[6].visible', true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[6].visible', true);
          });
        } else {
          vm.chartOptionsFunc.option('series[6].visible', false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option('series[6].visible', false);
          });
        }
      }
    };
    /** map **/
    var clicksByCountry = {};

    vm.Main.statsMap(vm.dataStart, vm.dataEnd).then(function (res) {
      clicksByCountry = res;
      $('#visualMap').dxVectorMap(vm.vectorMapOptions);
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
  }
})();
