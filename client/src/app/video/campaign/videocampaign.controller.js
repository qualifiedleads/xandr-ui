(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('VideoCampaignController', VideoCampaignController);

  /** @ngInject */
  function VideoCampaignController($window, $state, $localStorage, $translate, $timeout, VideoCampMain, Campaign, $rootScope) {
    var vm = this;
    var LC = $translate.instant;
    var dataSuspend = null;
    var tempSespendRow = {};
    var now = new Date();
    var oneSuspend = false;
    $rootScope.id = Campaign.id;
    $rootScope.name = Campaign.campaign;
    $rootScope.line_item = Campaign.line_item;
    $rootScope.line_item_id = Campaign.line_item_id;

    if ($localStorage.campaign == null) {
      $state.go('home.main');
    }

    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.line_item = Campaign.line_item;
    vm.line_item_id = Campaign.line_item_id;
    vm.Init = [];

    if ($localStorage.checkChartVideo == null) {
      $localStorage.checkChartVideo = {
        'imp': true,
        'ad_starts': false,
        'fill_rate': false,
        'profit_loss': false,
        'spend': false
      };
    }

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

    angular.element($window.document.querySelector("#wrapper"))[0].classList.remove('hidden-menu');

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

    var chartSeries = [
      {valueField: 'imp', name: 'Impressions', axis: 'imp', visible: $localStorage.checkChartVideo.imp},
      {valueField: 'ad_starts', name: 'ad_starts', axis: 'ad_starts', visible: $localStorage.checkChartVideo.ad_starts},
      {valueField: 'fill_rate', name: 'fill_rate', axis: 'fill_rate', visible: $localStorage.checkChartVideo.fill_rate},
      {valueField: 'profit_loss', name: 'profit_loss', axis: 'profit_loss', visible: $localStorage.checkChartVideo.profit_loss},
      {valueField: 'spend', name: 'Cost', axis: 'spend', visible: $localStorage.checkChartVideo.spend},
    ];

    vm.chartStore = VideoCampMain.getChartStore(Campaign.id, vm.dataStart, vm.dataEnd, ['imp', 'spend', 'ad_starts', 'fill_rate', 'profit_loss']);

    vm.UI = {
      datePiker:{
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
                  format:'percent',
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
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.IMPRESSIONS') +'</span><br>' + this.value.toString().split(/(?=(?:\d{3})+(?!\d))/).join();
                        case 'ad_starts':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.fill_rate') +'' + '</span><br>' + this.value+'';
                        case 'fill_rate':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + '' + LC('MAIN.CHECKBOX.fill_rate') + '</span><br>' + '' +this.value;
                        case 'profit_loss':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.profit_loss') + '</span><br>' + this.value;
                        case 'spend':
                          return '<span style="color:black; font-weight: bolder; text-decoration:underline;">' + LC('MAIN.CHECKBOX.COST') + '</span><br>' + '' +this.value;
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
          dataSource: 'videocamp.chartStore'
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
            label:{
              format:'percent',
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
      }
    }
  }
})();

