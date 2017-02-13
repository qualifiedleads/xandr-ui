(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('VideoMainController', VideoMainController);

  /** @ngInject */
  function VideoMainController($window, $state, $timeout, $localStorage, $translate, VideoMain, $rootScope) {
    var vm = this;
    vm.advertiser = $localStorage.advertiser;
    vm.VideoMain = VideoMain;
    vm.multipleTotalCount = 0;
    vm.Init = [];
    vm.by = ['imp', 'spend', 'ad_starts', 'fill_rate', 'profit_loss'];
    vm.selectedItems = [];
    vm.chartOptionsFuncgrid = [];
    vm.charIsUpdating = false;
    $rootScope.id = null;
    var LC = $translate.instant;
    /** LOCAL STORAGE CHECKBOX - START **/

    if ($localStorage.checkChartVideo == null) {
      $localStorage.checkChartVideo = {
        imp: true,
        ad_starts: false,
        fill_rate: false,
        profit_loss: false,
        spend: false
      };
    }

    var chartSeries = [
      { valueField: 'imp', name: 'Impressions', axis: 'imp', visible: $localStorage.checkChartVideo.imp },
      { valueField: 'ad_starts', name: 'ad_starts', axis: 'ad_starts', visible: $localStorage.checkChartVideo.ad_starts },
      { valueField: 'fill_rate', name: 'fill_rate', axis: 'fill_rate', visible: $localStorage.checkChartVideo.fill_rate },
      { valueField: 'profit_loss', name: 'profit_loss', axis: 'profit_loss', visible: $localStorage.checkChartVideo.profit_loss },
      { valueField: 'spend', name: 'Cost', axis: 'spend', visible: $localStorage.checkChartVideo.spend },
    ];

    /** DATE PIKER - START **/
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
      $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
      $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
      vm.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
      vm.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
    } else {
      if ($localStorage.dataStart == null || $localStorage.dataEnd == null) {
        $localStorage.SelectedTime = 0;
        $localStorage.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
        $localStorage.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
        vm.dataStart = $window.moment({ hour: '00' }).subtract(1, 'day').unix();
        vm.dataEnd = $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix();
      } else {
        vm.dataStart = $localStorage.dataStart;
        vm.dataEnd = $localStorage.dataEnd;
      }
    }

    var wrapper = angular.element($window.document.querySelector('#wrapper'))[0];
    wrapper.classList.add('hidden-menu');
    var products = [
      {
        ID: 0,
        Name: LC('MAIN.DATE_PICKER.YESTERDAY'),
        dataStart: $window.moment({ hour: '00' }).subtract(1, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).subtract(1, 'day').endOf('day').unix()
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(3, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(7, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(14, 'day').unix(),
        dataEnd: $window.moment({ hour: '00' }).unix()
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart: $window.moment({ hour: '00' }).subtract(21, 'day').unix(),
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
        if (checkTrue.length == 2 && checkFalse.length > 2) {
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

    function CheckLocalStorage() {
      for (var item in $localStorage.checkChartVideo) {
        if ($localStorage.checkChartVideo[item]) {
          if (item == 'imp') {
            vm.chartOptionsFunc.getSeriesByName('Impressions').show();
          }

          if (item == 'ad_starts') {
            vm.chartOptionsFunc.getSeriesByName('ad_starts').show();
          }

          if (item == 'fill_rate') {
            vm.chartOptionsFunc.getSeriesByName('fill_rate').show();
          }

          if (item == 'profit_loss') {
            vm.chartOptionsFunc.getSeriesByName('profit_loss').show();
          }

          if (item == 'spend') {
            vm.chartOptionsFunc.getSeriesByName('Cost').show();
          }
        } else {
          if (item == 'imp') {
            vm.chartOptionsFunc.getSeriesByName('Impressions').hide();
          }

          if (item == 'ad_starts') {
            vm.chartOptionsFunc.getSeriesByName('ad_starts').hide();
          }

          if (item == 'fill_rate') {
            vm.chartOptionsFunc.getSeriesByName('fill_rate').hide();
          }

          if (item == 'profit_loss') {
            vm.chartOptionsFunc.getSeriesByName('profit_loss').hide();
          }

          if (item == 'spend') {
            vm.chartOptionsFunc.getSeriesByName('Cost').hide();
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
      $localStorage.checkChartVideo[seriesShortName] = selected;
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

    vm.VideoMain.statsMap(vm.advertiser.id, vm.dataStart, vm.dataEnd)
      .then(function (res) {
        clicksByCountry = res;
        $window.$('#visualMap').dxVectorMap(vm.UI.vectorMapOptions);
      });

    vm.chartStore = VideoMain.chartStore(vm.advertiser.id, vm.dataStart, vm.dataEnd, ['imp', 'spend', 'ad_starts', 'fill_rate', 'profit_loss']);
    vm.multipleStore = VideoMain.multipleStore(vm.advertiser.id, vm.dataStart, vm.dataEnd, ['imp', 'spend', 'ad_starts', 'fill_rate', 'profit_loss']);
    vm.UI = {
      datePiker: {
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
      },
      dataGridOptionsMultiple: {
        bindingOptions: {
          dataSource: 'vmain.multipleStore'
        },
        onInitialized: function (data) {
          vm.dataGridOptionsMultipleFunc = data.component;
        },

        onContentReady: function () {
          var update = $window.$('<div />').dxButton({
            icon: 'upload',
            class: 'dx-icon dx-icon-export-excel-button ng-scope',
            disabled: false,
            onClick: function () {
              VideoMain.updateCampaign(vm.advertiser.id).then(function (res) {
                if (res == 200) {
                  $window.DevExpress.ui.notify(LC('MAIN.ADVERTISER_UPDATED'), 'success', 4000);
                  $state.reload();
                }
              });
            }
          });
          update.addClass('dx-datagrid-export-button dx-button dx-button-normal dx-widget dx-button-has-icon').appendTo('.dx-datagrid-header-panel');
        },

        loadPanel: {
          shadingColor: 'rgba(0,0,0,0.4)',
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false,
        },
        remoteOperations: true,
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
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
        showBorders: true,
        showRowLines: true,
        summary: {
          totalItems: [
            {
              column: 'campaign',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Count: ' + VideoMain.totalSummary.campaign;
                return data.valueText;
              }
            },
            {
              column: 'spent',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Spent: $' + VideoMain.totalSummary.spent.toFixed(2);
                return data.valueText;
              }
            },
            {
              column: 'sum_imps',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Imp: ' + VideoMain.totalSummary.sum_imps.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                return data.valueText;
              }
            },
            {
              column: 'cpm',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'CPM: $' + VideoMain.totalSummary.cpm.toFixed(2);
                return data.valueText;
              }
            },
            {
              column: 'ad_starts',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Ad starts: ' + VideoMain.totalSummary.ad_starts.toString().split(/(?=(?:\d{3})+(?!\d))/).join();;
                return data.valueText;
              }
            },
            {
              column: 'fill_rate',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Fill rate: ' + VideoMain.totalSummary.fill_rate.toFixed(4) + '%';
                return data.valueText;
              }
            },
            {
              column: 'profit_loss',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Profit loss: $' + VideoMain.totalSummary.profit_loss.toFixed(2);
                return data.valueText;
              }
            },
            {
              column: 'fill_rate_hour',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Delta fill rate: ' + VideoMain.totalSummary.fill_rate_hour.toFixed(4) + '%';
                return data.valueText;
              }
            },
            {
              column: 'profit_loss_hour',
              summaryType: 'sum',
              customizeText: function (data) {
                data.valueText = 'Delta profit loss: $'  + VideoMain.totalSummary.profit_loss_hour.toFixed(2);
                return data.valueText;
              }
            }
          ]
        },
        columns: [
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CAMPAIGN'),
            dataField: 'campaign',
            fixed: true,
            cellTemplate: function (container, options) {
              container.addClass('a-campaign');
              $window.angular.element('<a href="#/video/campaign/' + options.data.campaign_id + '">' + options.data.campaign_name + ' (' + options.data.campaign_id + ')</a>')
                .appendTo(container);
            },

            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'campaign_name');
              }
            },
            alignment: 'center'
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.SPENT') + ' ,$',
            dataField: 'spent',
            alignment: 'center',
            dataType: 'number',
            format: 'currency',
            allowFiltering: false,
            precision: 2,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'spent');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.IMP'),
            dataField: 'sum_imps',
            sortOrder: 'desc',
            alignment: 'center',
            format: 'fixedPoint',
            dataType: 'number',
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'sum_imps');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.CPM') + ' ,$',
            dataField: 'cpm',
            alignment: 'center',
            dataType: 'number',
            precision: 2,
            format: 'currency',
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'cpm');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.AD-STARTS'),
            dataField: 'ad_starts',
            alignment: 'center',
            format: 'fixedPoint',
            dataType: 'number',
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'ad_starts');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.FILL-RATE'),
            dataField: 'fill_rate',
            alignment: 'center',
            dataType: 'number',
            format: 'percent',
            precision: 2,
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'fill_rate');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.PROFIT-LOSS'),
            dataField: 'profit_loss',
            alignment: 'center',
            dataType: 'number',
            precision: 2,
            format: 'fixedPoint',
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'profit_loss');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.FILL-RATE-HOUR'),
            dataField: 'fill_rate_hour',
            alignment: 'center',
            dataType: 'number',
            format: 'percent',
            precision: 1,
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'fill_rate_hour');
              }
            }
          },
          {
            caption: LC('MAIN.CAMPAIGN.COLUMNS.PROFIT-LOSS-HOUR'),
            dataField: 'profit_loss_hour',
            alignment: 'center',
            dataType: 'number',
            precision: 2,
            format: 'currency',
            allowFiltering: false,
            headerFilter: {
              dataSource: function (source) {
                return headerFilterColumn(source, 'profit_loss_hour');
              }
            }
          },
          {
            width: 200,
            dataField: LC('MAIN.CAMPAIGN.COLUMNS.STATS'),
            allowFiltering: false,
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
                    { name: 'ad_starts' },
                    { name: 'fill_rate' },
                    { name: 'profit_loss' },
                    { name: 'spend' },
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
          }
        ],
        onSelectionChanged: function (data) {
          vm.selectedItems = data.selectedRowsData;
          vm.disabled = !vm.selectedItems.length;
        },
      },
      chartOptions: {
        onDone: function () {
          var chart = $('#chart').dxChart('instance');
          if (!vm.charIsUpdating) {
            var update = [];
            var flag = 'left';
            vm.UI.chartOptions.valueAxis.forEach(function (item, index) {
              var visible = $localStorage.checkChartVideo[item.name];
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
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.IMPRESSIONS') + '</span><br>' + this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                        case 'ad_starts':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.fill_rate') + '' + '</span><br>' + this.value + '';
                        case 'fill_rate':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + '' + LC('MAIN.CHECKBOX.fill_rate') + '</span><br>' + '' + this.value;
                        case 'profit_loss':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.profit_loss') + '</span><br>' + this.value;
                        case 'spend':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.COST') + '</span><br>' + '' + this.value;
                        default:
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + item.name + '</span><br>' + this.value;
                      }
                    }else {
                      switch (item.name) {
                        case 'imp':
                          return this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                        // case 'cvr':
                        //   return this.value+'%';
                        // case 'fill_rate':
                        //   return '$'+this.value;
                        // case 'spend':
                        //   return '$' + this.value;
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
          dataSource: 'vmain.chartStore'
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
            // if (arg.seriesName == 'Cost' || arg.seriesName == 'CPC') {
            //   return {
            //     text: '$' + arg.valueText
            //   };
            // }
            // if (arg.point.series.name == 'Impressions') {
            //   return {
            //     text: arg.valueText.toString().split(/(?=(?:\d{3})+(?!\d))/).join()}
            // }
            //
            // if ((arg.seriesName == 'CTR') || (arg.seriesName == 'CVR')) {
            //   return {
            //     text: arg.valueText + '%'
            //   };
            // }
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
            }
          },
          {
            name: 'ad_starts',
            position: 'left'
          },
          {
            name: 'fill_rate',
            position: 'left',
          },
          {
            name: 'spend',
            position: 'left'
          },
          {
            name: 'profit_loss',
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
        value: $localStorage.checkChartVideo.imp,
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
      ad_starts: {
        text: LC('MAIN.CHECKBOX.ad_starts'),
        value: $localStorage.checkChartVideo.ad_starts,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('ad_starts', 'ad_starts', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      fill_rate: {
        text: LC('MAIN.CHECKBOX.fill_rate'),
        value: $localStorage.checkChartVideo.fill_rate,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('fill_rate', 'fill_rate', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      profit_loss: {
        text: LC('MAIN.CHECKBOX.profit_loss'),
        value: $localStorage.checkChartVideo.profit_loss,
        onInitialized: function (data) {
          vm.Init.push(data.component);
        },

        onValueChanged: function (e) {
          vm.updateCharts('profit_loss', 'profit_loss', e.value);
          vm.onlyTwo(e.value);
          vm.charIsUpdating = false;
          vm.UI.chartOptions.onDone();
          CheckLocalStorage();
        }
      },
      cost: {
        text: LC('MAIN.CHECKBOX.COST'),
        value: $localStorage.checkChartVideo.spend,
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
      vectorMapOptions: {
        size: {
          height: 320
        },
        layers: [{
          name: 'areas',
          dataSource: $window.DevExpress.viz.map.sources.world,
          palette: 'blue',
          colorGroups: [0, 100, 10000000],
          colorGroupingField: 'imps',
          label: {
            enabled: true,
            dataField: 'name'
          },
          customize: function (elements) {
            elements.forEach(function (element) {
              var name = element.attribute('name');
              var clicks = clicksByCountry[name];
              if (clicks) {
                element.attribute('imps', clicks);
              }
            });
          }
        }],
        tooltip: {
          enabled: true,
          customizeTooltip: function (arg) {
            if (arg.attribute('imps')) {
              return { text: arg.attribute('name') + ': ' + arg.attribute('imps') };
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
            return arg.start + ' to ' + arg.end + ' impressions';
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

      if (checkTrue.length >= 2 && checkFalse.length > 2) {
        for (i = 0; i < checkFalse.length; i++) {
          checkFalse[i].option('disabled', true);
        }
      }
    });

  }
})();
