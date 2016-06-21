(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController() {
    var vm = this;

    vm.checkboxData = [];

    vm.dataTotals = [{
      "TOTALS":"",
      "spend":"$1710",
      "conv":"13",
      "imp":"3,122,000 | 2000",
      "clicks":"$1.15 | $0.98",
      "cpc":"0.4%",
      "cpm":"0.9%",
      "CVR":"",
      "CTR":""
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



    vm.dataGridOptionsMultiple = {
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
      columns: ["Campaign", "spend", "conv", "imp", "clicks", "cpc", "cpm", "CVR", "CTR"]
      ,
      selection: {
          mode: "multiple"
        },
        onSelectionChanged: function(data) {
          vm.selectedItems = data.selectedRowsData;
          vm.disabled = !vm.selectedItems.length;
        }
    };

    vm.dataSource = [{
      day: "Sunday",
      hydro: 59.8,
      oil: 937.6,
      gas: 582,
      coal: 564.3,
      nuclear: 187.9
    }, {
      day: "Monday",
      hydro: 74.2,
      oil: 308.6,
      gas: 35.1,
      coal: 956.9,
      nuclear: 11.3
    }, {
      day: "Tuesday",
      hydro: 40,
      oil: 128.5,
      gas: 361.8,
      coal: 105,
      nuclear: 32.4
    }, {
      day: "Wednesday",
      hydro: 22.6,
      oil: 241.5,
      gas: 64.9,
      coal: 120.8,
      nuclear: 64.8
    }, {
      day: "Thursday",
      hydro: 19,
      oil: 119.3,
      gas: 28.9,
      coal: 204.8,
      nuclear: 3.8
    }, {
      day: "Friday",
      hydro: 6.1,
      oil: 123.6,
      gas: 77.3,
      coal: 85.7,
      nuclear: 37.8
    },
      {
        day: "Friday",
        hydro: 6.1,
        oil: 123.6,
        gas: 77.3,
        coal: 85.7,
        nuclear: 37.8
      }];
    vm.types = ["line", "stackedLine", "fullStackedLine"];

    vm.chartOptions = {
      size: {
        width: 500,
        height: 230
      },
      dataSource: vm.dataSource,
      commonSeriesSettings: {
        argumentField: "day",
        type: vm.types[0]
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
      series: [
        { valueField: "hydro", name: "Hydro-electric" },
        { valueField: "oil", name: "Oil" },
        { valueField: "gas", name: "Natural gas" },
        { valueField: "coal", name: "Coal" },
        { valueField: "nuclear", name: "Nuclear" }
      ],
      legend: {
        verticalAlignment: "bottom",
        horizontalAlignment: "center",
        itemTextPosition: "bottom"
      },
      // title: {
      //   text: "Energy Consumption in 2004",
      //   subtitle: {
      //     text: "(Millions of Tons, Oil Equivalent)"
      //   }
      // },
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          return {
            text: arg.valueText
          };
        }
      }
    };
    
  }
})();
