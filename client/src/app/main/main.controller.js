(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($window) {
    var vm = this;
    var products = [{
      "ID": 0,
      "Name": "Last day",
      "dataStart": '',
      "dataEnd": ''
    }, {
      "ID": 1,
      "Name": "Current week"
    }, {
      "ID": 2,
      "Name": "Last week"
    }, {
      "ID": 3,
      "Name": "Current month"
    }, {
      "ID": 4,
      "Name": "Last month"
    }];

    vm.datePiker = {
      dataSource: new DevExpress.data.ArrayStore({
        data: products,
        key: "ID"
      }),
      displayExpr: "Name",
      valueExpr: "ID",
      value: products[0].ID
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
        //console.log(data.component.series.length);
      },
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
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[0].visible", true);
        } else {
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
        } else {
          vm.chartOptionsFunc.option("series[1].visible", false);
        }
      }
    };

    vm.CPC = {
      text: "CPC",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[2].visible", true);
        } else {
          vm.chartOptionsFunc.option("series[2].visible", false);
        }
      }
    };

    vm.clicks = {
      text: "clicks",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[3].visible", true);
        } else {
          vm.chartOptionsFunc.option("series[3].visible", false);
        }
      }
    };

    vm.media = {
      text: "media spend",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[4].visible", true);
        } else {
          vm.chartOptionsFunc.option("series[4].visible", false);
        }
      }
    };

    vm.conversions = {
      text: "conversions",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[5].visible", true);
        } else {
          vm.chartOptionsFunc.option("series[5].visible", false);
        }
      }
    };

    vm.CTR = {
      text: "CTR",
      value: true,
      onValueChanged: function (e) {
        if (e.value == true) {
          vm.chartOptionsFunc.option("series[6].visible", true);
        } else {
          vm.chartOptionsFunc.option("series[6].visible", false);
        }
      }
    };


    //console.log(vm.chartOptions);
    //console.log(vm.personalCountersGrid);




  }
})();
