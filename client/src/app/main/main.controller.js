(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($window,$state) {
    var vm = this;
    var products = [{
      "ID": 0,
      "Name": "Last day",
      "dataStart": moment({hour: "00"}).toDate(),
      "dataEnd": moment().toDate()
    }, {
      "ID": 1,
      "Name": "Current week",
      "dataStart": moment().startOf('week').toDate(),
      "dataEnd": moment().toDate()
    }, {
      "ID": 2,
      "Name": "Last week",
      "dataStart": moment().startOf('week').subtract(1,'week').toDate(),
      "dataEnd": moment().startOf('week').toDate()
    }, {
      "ID": 3,
      "Name": "Current month",
      "dataStart": moment().startOf('month').toDate(),
      "dataEnd": moment().toDate()
    }, {
      "ID": 4,
      "Name": "Last month",
      "dataStart": moment().subtract(1,'month').startOf('month').toDate(),
      "dataEnd": moment().subtract(1,'month').endOf('month').toDate(),
    }];

    vm.datePiker = {
      dataSource: new DevExpress.data.ArrayStore({
        data: products,
        key: "ID"
      }),
      displayExpr: "Name",
      valueExpr: "ID",
      value: products[0],
      onInitialized: function (e) {
        //console.log(e);
      },
      onValueChanged:function (e) {
        // Запрос на бэкЭнд

        console.log(e);
        $state.reload();
      }
    };

    vm.checkboxData = [];

    vm.dataTotals = [{
      "TOTALS":"",
      "spend":"$1710",
      "conv":"13",
      "imp":"3,122,000 | 2000",
      "clicks":"$1.15 | $0.98",
      "cpc":"0.4%",
      "cpm":"0.9%",
      "CVR":"2",
      "CTR":"2"
    }
    ];

    vm.dataCampaign = [{
      "Campaign":"Campaign1",
      "spend":"$410",
      "conv":"8",
      "imp":"5500",
      "clicks":"21",
      "cpc":"$0.31",
      "cpm":"$1.38",
      "CVR":"1",
      "CTR":"2"
    },
      {
        "Campaign":"Campaign2",
        "spend":"$710",
        "conv":"3",
        "imp":"5500",
        "clicks":"21",
        "cpc":"$0.31",
        "cpm":"$1.38",
        "CVR":"1",
        "CTR":"2"
      },
      {
        "Campaign":"Campaign3",
        "spend":"$10",
        "conv":"1",
        "imp":"5500",
        "clicks":"21",
        "cpc":"$0.31",
        "cpm":"$1.38",
        "CVR":"1",
        "CTR":"2"
      },
      {
        "Campaign":"Campaign4",
        "spend":"$1010",
        "conv":"1",
        "imp":"5500",
        "clicks":"21",
        "cpc":"$0.31",
        "cpm":"$1.38",
        "CVR":"1",
        "CTR":"2"
      }
    ];

    vm.dataGridOptionsSingle = {
      dataSource: vm.dataTotals,
      showBorders: true,
      alignment:"left",
      paging: {
        pageSize: 10
      },
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [5, 10, 20],
        showInfo: true
      },
      howBorders: true,
      columns: ["TOTALS", "spend", "conv", "imp", "clicks", "cpc", "cpm", "CVR", "CTR" ]
    };
    vm.selectedItems = [];


    vm.chartOptionsFuncgrid = [];
    vm.dataGridOptionsMultiple = {
      onInitialized: function (data) {
        vm.dataGridOptionsMultipleFunc = data.component;
        vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 15;
      },
      dataSource: vm.dataCampaign,
      showBorders: true,
      alignment:"left",
      headerFilter: {
        visible: true
      },
      paging: {
        pageSize: 10
      },
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [5, 10, 20],
        showInfo: true
      },
      howBorders: true,
      showRowLines: true,
      columns: ["Campaign", "spend", "conv", "imp", "clicks", "cpc", "cpm", "CVR", "CTR",
        {
          width: 200,
          dataField: "Stats",
          cellTemplate: function (container, options) {

            var types = ["line", "stackedLine", "fullStackedLine"];

            var chartOptions = {
              onInitialized: function (data) {
                vm.chartOptionsFuncgrid[options.rowIndex] = data.component;
              },

              dataSource: vm.dataSource,
              size:{
                height:80
              },
              commonSeriesSettings: {
                argumentField: "day",
                type: vm.types[0],
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
                label:{
                  visible: false
                },
                grid: { visible: false }
              },
              argumentAxis: {
                valueMarginsEnabled: false,
                discreteAxisDivisionMode: "crossLabels",
                grid: {
                  visible: false
                },
                label:{
                  visible: false
                },
                minorGrid:{
                  visible: false
                },
                minorTick:{
                  visible: false
                },
                tick: {
                  visible: false
                }
              },
              series: [
                { valueField: "impressions", name: "Impressions"},
                { valueField: "CPA", name: "CPA" },
                { valueField: "CPC", name: "CPC" },
                { valueField: "clicks", name: "clicks" },
                { valueField: "media", name: "media" },
                { valueField: "conversions", name: "conversions" },
                { valueField: "CTR", name: "CTR" }
              ],
              legend: {
                verticalAlignment: "bottom",
                horizontalAlignment: "center",
                itemTextPosition: "bottom"
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



            container.addClass("img-container");
            $('<div id="chartMulti'+options.rowIndex+'" ></div>')
            //.attr("src", options.value)
              .appendTo(container);
            $("#chartMulti"+options.rowIndex).dxChart(chartOptions).dxChart("instance");
          }
        }],
      selection: {
        mode: "multiple"
      },
      onSelectionChanged: function(data) {
        //console.log(vm.dataGridOptionsMultiple);
        vm.selectedItems = data.selectedRowsData;
        vm.disabled = !vm.selectedItems.length;
      }
    };

    vm.dataSource = [{
      day: "Sunday",
      impressions: 0,
      CPA: 0,
      CPC: 0,
      clicks: 0,
      media: 0,
      conversions: 0,
      CTR: 0
    },{
      day: "Monday",
      impressions: 159.8,
      CPA: 837.6,
      CPC: 482,
      clicks: 464.3,
      media: 87.9,
      conversions: 287.9,
      CTR: 287.9
    }, {
      day: "Tuesday",
      impressions: 259.8,
      CPA: 537.6,
      CPC: 782,
      clicks: 264.3,
      media: 887.9,
      conversions: 187.9,
      CTR: 87.9
    }, {
      day: "Wednesday",
      impressions: 159.8,
      CPA: 237.6,
      CPC: 482,
      clicks: 364.3,
      media: 587.9,
      conversions: 687.9,
      CTR: 787.9
    }, {
      day: "Thursday",
      impressions: 359.8,
      CPA: 737.6,
      CPC: 482,
      clicks: 364.3,
      media: 187.9,
      conversions: 187.9,
      CTR: 187.9
    }, {
      day: "Friday",
      impressions: 59.8,
      CPA: 937.6,
      CPC: 582,
      clicks: 564.3,
      media: 287.9,
      conversions: 387.9,
      CTR: 487.9
    },
      { day: "Saturday",
        impressions: 159.8,
        CPA: 837.6,
        CPC: 282,
        clicks: 164.3,
        media: 187.9,
        conversions: 187.9,
        CTR: 287.9
      }];
    vm.types = ["line", "stackedLine", "fullStackedLine"];



    var series = [
      { valueField: "impressions", name: "Impressions"},
      { valueField: "CPA", name: "CPA" },
      { valueField: "CPC", name: "CPC" },
      { valueField: "clicks", name: "clicks" },
      { valueField: "media", name: "media" },
      { valueField: "conversions", name: "conversions" },
      { valueField: "CTR", name: "CTR" }
    ];

    vm.chartOptions = {
      onInitialized: function (data) {
        vm.chartOptionsFunc = data.component;
      },
      size: {
        width: 500,
        height: 230
      },
      dataSource: vm.dataSource,
      commonSeriesSettings: {
        argumentField: "day",
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
        discreteAxisDivisionMode: "crossLabels",
        grid: {
          visible: true
        }
      },
      series: series,
      legend: {
        verticalAlignment: "bottom",
        horizontalAlignment: "center",
        itemTextPosition: "bottom"
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
      text: "Impressions",
      value: true,
      onValueChanged: function (e) {
        console.log(vm.chartOptionsFuncgrid);
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[0].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[0].visible", true);
          });
        } else {
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[0].visible", false);
          });
          vm.chartOptionsFunc.option("series[0].visible", false);
        }
      }
    };

    vm.CPA = {
      text: "CPA",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[1].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[1].visible", true);
          });
        } else {
          vm.chartOptionsFunc.option("series[1].visible", false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[1].visible", false);
          });
        }
      }
    };

    vm.CPC = {
      text: "CPC",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[2].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[2].visible", true);
          });
        } else {
          vm.chartOptionsFunc.option("series[2].visible", false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[2].visible", false);
          });
        }
      }
    };

    vm.clicks = {
      text: "clicks",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[3].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[3].visible", true);
          });
        } else {
          vm.chartOptionsFunc.option("series[3].visible", false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[3].visible", false);
          });
        }
      }
    };

    vm.media = {
      text: "media spend",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[4].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[4].visible", true);
          });
        } else {
          vm.chartOptionsFunc.option("series[4].visible", false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[4].visible", false);
          });
        }
      }
    };

    vm.conversions = {
      text: "conversions",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[5].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[5].visible", true);
          });
        } else {
          vm.chartOptionsFunc.option("series[5].visible", false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[5].visible", false);
          });
        }
      }
    };

    vm.CTR = {
      text: "CTR",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[6].visible", true);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[6].visible", true);
          });
        } else {
          vm.chartOptionsFunc.option("series[6].visible", false);
          vm.chartOptionsFuncgrid.forEach(function (col) {
            col.option("series[6].visible", false);
          });
        }
      }
    };

    /** map **/
    var clicksByCountry = {
      "China": 19,
      "India": 123,
      "United States": 3000,
      "Indonesia": 200,
      "Brazil": 5000,
      "Nigeria": 30000,
      "Bangladesh": 4000,
      "Russia": 1000,
      "Japan": 4,
      "Mexico": 40,
      "Philippines": 600,
      "Germany": 3000,
      "France": 20000,
      "Thailand": 1000,
      "United Kingdom": 200,
      "Italy": 222,
      "Ukraine": 600,
      "Canada": 50
    };

    vm.vectorMapOptions = {
      layers: [{
        name: "areas",
        dataSource: $window.DevExpress.viz.map.sources.world,
        palette:"blue",
        colorGroups: [0, 100, 1000, 10000],
        colorGroupingField: "clicks",
        label: {
          enabled: true,
          dataField: "name"
        },
        customize: function (elements) {
          elements.forEach(function (element) {
            var name = element.attribute("name"),
              clicks = clicksByCountry[name];
            if (clicks) {
              element.attribute("clicks", clicks);
            }
          });
        }
      }],
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          return { text: arg.attribute("text") };
        }
      },
      legends: [{
        source: { layer: "areas", grouping: "color" },
        horizontalAlignment: "left",
        verticalAlignment: "bottom",
        customizeText: function (arg) {
          return arg.start + " to " + arg.end + " clicks";
        }
      }],
      bounds: [-180, 85, 180, -75]
    };

  }
})();
