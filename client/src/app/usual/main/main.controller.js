(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($window, $state, $timeout, $localStorage, $translate, Main, $rootScope, VideoMain) {
    var vm = this;
    var buttonIndicator;
    vm.advertiser = $localStorage.advertiser;
    vm.Main = Main;
    vm.multipleTotalCount = 0;
    vm.Init = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';
    vm.selectedItems = [];
    vm.chartOptionsFuncgrid = [];
    vm.charIsUpdating = false;
    $rootScope.id = null;
    var LC = $translate.instant;

    /** LOCAL STORAGE CHECKBOX - START **/
    if ($localStorage.checkChart == null) {
      $localStorage.checkChart = {
        imp: true,
        cvr: false,
        cpc: false,
        clicks: false,
        spend: false,
        conv: false,
        ctr: false
      };
    }

    var chartSeries = [
      { valueField: 'imp', name: 'Impressions', axis: 'imp', visible: $localStorage.checkChart.imp },
      { valueField: 'cvr', name: 'CVR', axis: 'cvr', visible: $localStorage.checkChart.cvr },
      { valueField: 'cpc', name: 'CPC', axis: 'cpc', visible: $localStorage.checkChart.cpc },
      { valueField: 'clicks', name: 'Clicks', axis: 'clicks', visible: $localStorage.checkChart.clicks },
      { valueField: 'spend', name: 'Cost', axis: 'spend', visible: $localStorage.checkChart.spend },
      { valueField: 'conv', name: 'Conversions', axis: 'conv', visible: $localStorage.checkChart.conv },
      { valueField: 'ctr', name: 'CTR', axis: 'ctr', visible: $localStorage.checkChart.ctr }
    ];

    /** DATE PIKER - START **/
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
      $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
      $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
      $localStorage.type = 'yesterday';
      vm.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
      vm.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
      vm.type = 'yesterday';
    } else {
      if (!$localStorage.dataStart || !$localStorage.dataEnd || !$localStorage.type) {
        $localStorage.SelectedTime = 0;
        $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
        $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
        $localStorage.type = 'yesterday';
        vm.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
        vm.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
        vm.type = 'yesterday';
      } else {
        vm.dataStart = $localStorage.dataStart;
        vm.dataEnd = $localStorage.dataEnd;
        vm.type = $localStorage.type;
      }
    }

    var wrapper = angular.element($window.document.querySelector('#wrapper'))[0];
    wrapper.classList.add('hidden-menu');
    var products = [
      {
        ID: 0,
        Name: LC('MAIN.DATE_PICKER.YESTERDAY'),
        dataStart: $window.moment({ hour: '00' }).subtract(1, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix(),
        type: 'yesterday'
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(3, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix(),
        type: 'last_3_days'
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(7, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix(),
        type: 'last_7_days'
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(14, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix(),
        type: 'last_14_days'
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(21, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix(),
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
        dataEnd: $window.moment().subtract(1, 'month').endOf('month').unix(),
        type: 'last_month'
      }, {
        ID: 7,
        Name: LC('MAIN.DATE_PICKER.LAST_90_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(90, 'day').unix(),
        dataEnd: $window.moment().unix(),
        type: 'last_90_days'
      }, {
        ID: 8,
        Name: LC('MAIN.DATE_PICKER.ALL_TIME'),
        dataStart: 0,
        dataEnd: $window.moment().unix(),
        type: 'all'
      }];

    /** TOTALS - START **/
    vm.totals = [];
    vm.Main.statsTotals(vm.advertiser.id, vm.dataStart, vm.dataEnd)
      .then(function (result) {
        vm.totals.imp = result.imp.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
        vm.totals.spent = result.spend.toFixed(2);
        vm.totals.conv = result.conv;
        vm.totals.cpc = result.cpc;
        vm.totals.cpm = result.cpm;
        vm.totals.cvr = result.cvr;
        vm.totals.ctr = result.ctr;
      });

    vm.checkBoxState = true;

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
      for (var item in $localStorage.checkChart) {
        if ($localStorage.checkChart[item]) {
          if (item == 'imp') {
            vm.chartOptionsFunc.getSeriesByName('Impressions').show();
          }

          if (item == 'cvr') {
            vm.chartOptionsFunc.getSeriesByName('CVR').show();
          }

          if (item == 'cpc') {
            vm.chartOptionsFunc.getSeriesByName('CPC').show();
          }

          if (item == 'clicks') {
            vm.chartOptionsFunc.getSeriesByName('Clicks').show();
          }

          if (item == 'spend') {
            vm.chartOptionsFunc.getSeriesByName('Cost').show();
          }

          if (item == 'conv') {
            vm.chartOptionsFunc.getSeriesByName('Conversions').show();
          }

          if (item == 'ctr') {
            vm.chartOptionsFunc.getSeriesByName('CTR').show();
          }
        } else {
          if (item == 'imp') {
            vm.chartOptionsFunc.getSeriesByName('Impressions').hide();
          }

          if (item == 'cvr') {
            vm.chartOptionsFunc.getSeriesByName('CVR').hide();
          }

          if (item == 'cpc') {
            vm.chartOptionsFunc.getSeriesByName('CPC').hide();
          }

          if (item == 'clicks') {
            vm.chartOptionsFunc.getSeriesByName('Clicks').hide();
          }

          if (item == 'spend') {
            vm.chartOptionsFunc.getSeriesByName('Cost').hide();
          }

          if (item == 'conv') {
            vm.chartOptionsFunc.getSeriesByName('Conversions').hide();
          }

          if (item == 'ctr') {
            vm.chartOptionsFunc.getSeriesByName('CTR').hide();
          }
        }
      }
    }

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
        for (i = 0; i < gridCharts.length; i++) {
          $window.$(gridCharts[i]).dxChart('instance').getSeriesByName(seriesName).show();
        }
      } else {
        vm.chartOptionsFunc.getSeriesByName(seriesName).hide();
        gridCharts = $window.$('.chartMulti');
        for (i = 0; i < gridCharts.length; i++) {
          $window.$(gridCharts[i]).dxChart('instance').getSeriesByName(seriesName).hide();
        }
      }
    };

    var clicksByCountry = {};

    vm.Main.statsMap(vm.advertiser.id, vm.dataStart, vm.dataEnd)
      .then(function (res) {
        clicksByCountry = res;
        $window.$('#visualMap').dxVectorMap(vm.UI.vectorMapOptions);
      });

    vm.chartStore = Main.chartStore(vm.advertiser.id, vm.dataStart, vm.dataEnd, vm.by);
    vm.multipleStore = Main.multipleStore(vm.advertiser.id, vm.dataStart, vm.dataEnd, vm.by, vm.type);
    vm.UI = {
      datePiker: {
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
      },
      update: {
        text: LC('MAIN.UPDATE_CAMPAIGN'),
        template: function (data, container) {
          $("<div class='button-indicator' style='float: left;'></div><span class='dx-button-text' style='float: left;'>&nbsp;" + data.text + '</span>').appendTo(container);
          buttonIndicator = container.find('.button-indicator').dxLoadIndicator({
              visible: false,
              height: 15,
              width: 15
            }).dxLoadIndicator('instance');
        },

        onClick: function (data) {
          data.component.option('text', LC('MAIN.UPDATE_CAMPAIGN'));
          buttonIndicator.option('visible', true);
          VideoMain.updateCampaign(vm.advertiser.id).then(function (res) {
            if (res == 200) {
              buttonIndicator.option('visible', false);
              data.component.option('text', LC('MAIN.UPDATE_CAMPAIGN'));
              $window.DevExpress.ui.notify(LC('MAIN.ADVERTISER_UPDATED'), 'success', 4000);
              $state.reload();
            } else {
              buttonIndicator.option('visible', false);
              data.component.option('text', LC('MAIN.UPDATE_CAMPAIGN'));
            }

          });
        }
      },
      dataGridOptionsMultiple: {
        bindingOptions: {
          dataSource: 'main.multipleStore'
        },
        onInitialized: function (data) {
          vm.dataGridOptionsMultipleFunc = data.component;
          /*vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 15;*/
        },

        loadPanel: {
          shadingColor: 'rgba(0,0,0,0.4)',
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false,
        },
        alignment: 'left',
        headerFilter: {
          visible: true
        },
        filterRow: {
          visible: true,
          applyFilter: 'auto'
        },
        export: {
          enabled: true,
          fileName: 'Employees'
        },
        allowColumnReordering: true,
        allowColumnResizing: true,
        columnAutoWidth: true,
        wordWrapEnabled: true,
        loadingIndicator: {
          show: false
        },
        columnChooser: {
          enabled: true
        },
        columnFixing: {
          enabled: true
        },
        paging: {
          pageSize: 10
        },
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
        },
        showBorders: true,
        showRowLines: true,
        columns: [
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CAMPAIGN'),
            dataField: 'campaign',
            fixed: true,
            cellTemplate: function (container, options) {
              container.addClass('a-campaign');
              $window.angular.element('<a href="#/campaign/' + options.data.id + '">' + options.data.campaign + '</a>')
                .appendTo(container);
            },

            alignment: 'center'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.SPENT') + ' ,$',
            dataField: 'spend',
            alignment: 'center',
            dataType: 'number',
            format: 'currency',
            precision: 4,
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CONV'),
            dataField: 'conv',
            alignment: 'center',
            dataType: 'number'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.IMP'),
            dataField: 'imp',
            sortOrder: 'desc',
            alignment: 'center',
            format: 'fixedPoint',
            dataType: 'number'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CLICKS'),
            dataField: 'clicks',
            alignment: 'center',
            dataType: 'number'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CPC') + ' ,$',
            dataField: 'cpc',
            alignment: 'center',
            dataType: 'number',
            precision: 4,
            format: 'currency'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CPM') + ' ,$',
            dataField: 'cpm',
            alignment: 'center',
            dataType: 'number',
            precision: 4,
            format: 'currency'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CVR') + ' ,%',
            dataField: 'cvr',
            alignment: 'center',
            dataType: 'number',
            precision: 2,
            format: 'percent'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CTR') + ' ,%',
            dataField: 'ctr',
            alignment: 'center',
            dataType: 'number',
            precision: 2,
            format: 'percent'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.IMPS_VIEWED'),
            dataField: 'imps_viewed',
            alignment: 'center',
            width: 90,
            dataType: 'number',
            format: 'fixedPoint',

          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.VIEW_MEASURED_IMPS'),
            dataField: 'view_measured_imps',
            alignment: 'center',
            width: 100,
            dataType: 'number',
            format: 'fixedPoint',

          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.VIEW_MEASUREMENT_RATE') + ' ,%',
            dataField: 'view_measurement_rate',
            alignment: 'center',
            width: 120,
            dataType: 'number',
            precision: 2,
            format: 'percent'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.VIEW_RATE') + ' ,%',
            dataField: 'view_rate',
            alignment: 'center',
            width: 80,
            dataType: 'number',
            precision: 2,
            format: 'percent',

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
                    { name: 'imp' },
                    { name: 'cvr' },
                    { name: 'cpc' },
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
                  series: chartSeries,
                  legend: {
                    visible: false
                  },
                  tooltip: {
                    enabled: true,
                    customizeTooltip: function (arg) {
                      if (arg.seriesName == 'Cost' || arg.seriesName == 'CPC') {
                        return {
                          text: '$' + arg.valueText + ' ' + arg.seriesName
                        };
                      }

                      if (arg.seriesName == 'Impressions') {
                        return {
                          text: arg.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join()
                        };
                      }

                      if (arg.seriesName == 'CTR' || arg.seriesName == 'CVR') {
                        return {
                          text: arg.valueText + '%' + ' ' + arg.seriesName
                        };

                      } else {
                        return {
                          text: arg.valueText + ' ' + arg.seriesName
                        };
                      }
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
        onSelectionChanged: function (data) {
          vm.selectedItems = data.selectedRowsData;
          vm.disabled = !vm.selectedItems.length;
        }
      },
      chartOptions: {
        onDone: function () {
          var chart = $('#chart').dxChart('instance');
          if (!vm.charIsUpdating) {
            var update = [];
            var flag = 'left';
            vm.UI.chartOptions.valueAxis.forEach(function (item, index) {
              var visible = $localStorage.checkChart[item.name];
              update.push({
                name: item.name,
                position: flag,
                label: {
                  format: 'percent',
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
                        case 'imp':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.IMPRESSIONS') +
                            '</span><br>' + this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                        case 'cvr':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.CVR') + '%' + '</span><br>' + this.value + '%';
                        case 'cpc':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + '$' + LC('MAIN.CHECKBOX.CPC') + '</span><br>' + '$' + this.value;
                        case 'clicks':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.CLICKS') + '</span><br>' + this.value;
                        case 'spend':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.COST') + '</span><br>' + '$' + this.value;
                        case 'conv':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.CONVERSIONS') + '</span><br>' + this.value;
                        case 'ctr':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.CTR') + '%' + '</span><br>' + this.value + '%';
                        default:
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + item.name + '</span><br>' + this.value;
                      }
                    }else {
                      switch (item.name) {
                        case 'imp':
                          return this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                        case 'cvr':
                          return this.value + '%';
                        case 'cpc':
                          return '$' + this.value;
                        case 'spend':
                          return '$' + this.value;
                        case 'ctr':
                          return this.value + '%';
                      }}

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
          vm.chartOptionsFunc = data.component;
        },

        series: chartSeries,
        bindingOptions: {
          dataSource: 'main.chartStore'
        },
        commonSeriesSettings: {
          argumentField: 'day',
          type: 'Line',
          point: {
            size: 6,
            hoverStyle: {
              border: {
                visible: true,
                width: 2
              },
              size: 5
            }
          }
        },
        tooltip: {
          enabled: true,

          customizeTooltip: function (arg) {
            //console.log(arg);
            if (arg.seriesName == 'Cost' || arg.seriesName == 'CPC') {
              return {
                text: '$' + arg.valueText
              };
            }

            if (arg.point.series.name == 'Impressions') {
              return {
                text: arg.valueText.toString().split(/(?=(?:\d{3})+(?!\d))/).join() };
            }

            if ((arg.seriesName == 'CTR') || (arg.seriesName == 'CVR')) {
              return {
                text: arg.valueText + '%'
              };
            }

            return {
              text: arg.valueText
            };
          },

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
                if (arg.point.series.name == 'Cost' || arg.point.series.name == 'CPC') {
                  return '$' + this.value;
                }

                if (arg.point.series.name == 'Impressions')  {
                  return this. value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                }

                if ((arg.point.series.name == 'CTR') || (arg.point.series.name == 'CVR')) {
                  return this.value + '%';
                }
              },
            },
          },
          verticalLine: {
            label: {
              visible: true
            }
          }

        },
        commonAxisSettings: {
          valueMarginsEnabled: true,

        },
        margin: {
          bottom: 20
        },
        argumentAxis: {
          //valueMarginsEnabled: false,
          discreteAxisDivisionMode: 'crossLabels',

          grid: {
            visible: true
          }
        },

        valueAxis: [
          {
            name: 'imp',
            position: 'left',
            label: {
              format: 'percent',
            },
          },
          {
            name: 'cvr',
            position: 'left'
          },
          {
            name: 'cpc',
            position: 'left',
            label: { format: 'currency' },

          },
          {
            name: 'clicks',
            position: 'left',

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
        ],
        legend: {
          verticalAlignment: 'bottom',
          horizontalAlignment: 'center',
          itemTextPosition: 'bottom'
        },

      },
      impressions: {
        text: LC('MAIN.CHECKBOX.IMPRESSIONS'),
        value: $localStorage.checkChart.imp,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('Impressions', 'imp', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      CVR: {
        text: LC('MAIN.CHECKBOX.CVR'),
        value: $localStorage.checkChart.cvr,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('CVR', 'cvr', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      CPC: {
        text: LC('MAIN.CHECKBOX.CPC'),
        value: $localStorage.checkChart.cpc,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('CPC', 'cpc', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      clicks: {
        text: LC('MAIN.CHECKBOX.CLICKS'),
        value: $localStorage.checkChart.clicks,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('Clicks', 'clicks', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      cost: {
        text: LC('MAIN.CHECKBOX.COST'),
        value: $localStorage.checkChart.spend,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('Cost', 'spend', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      conversions: {
        text: LC('MAIN.CHECKBOX.CONVERSIONS'),
        value: $localStorage.checkChart.conv,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('Conversions', 'conv', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      CTR: {
        text: LC('MAIN.CHECKBOX.CTR'),
        value: $localStorage.checkChart.ctr,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('CTR', 'ctr', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      vectorMapOptions: {
        size: {
          height: 320
        },
        layers: [{
          name: 'areas',
          dataSource: $window.DevExpress.viz.map.sources.world,
          palette: 'blue',
          colorGroups: [0, 100, 10000000],
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
              return { text: arg.attribute('name') + ': ' + arg.attribute('clicks') };
            } else {
              return { text: arg.attribute('name') };
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
      }
    };

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

  }
})();
