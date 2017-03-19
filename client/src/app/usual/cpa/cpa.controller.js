(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CPAController', CPAController);

  /** @ngInject */
  function CPAController($window, $state, $localStorage, $translate, CPA, ChartDetails, CpaBucketsAll, Campaign, Home) {
    var vm = this;
    vm.Camp = CPA;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';
    var LC = $translate.instant;
    vm.campName = Home.AdverInfo.campaign;
    vm.campId = Home.AdverInfo.id;
    vm.line_item = Home.AdverInfo.line_item;
    vm.line_item_id = Home.AdverInfo.line_item_id;
    vm.cpaResult = [];
    vm.selectedSection = $localStorage.selectedSection;

    vm.detailsStoreAll = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return ChartDetails.all;
      }
    });

    vm.detailsStoreConversion = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return ChartDetails.conversions;
      }
    });

    vm.cpaBucketRequestFirst = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
            vm.cpaResult = CpaBucketsAll;
            var arrFirst = [];
            for(var i=0; i<vm.cpaResult.length; i++) {
              if(+vm.cpaResult[i].cpa>=vm.backetsRanges.first.min && +vm.cpaResult[i].cpa<vm.backetsRanges.first.max) {
                arrFirst.push(vm.cpaResult[i]);
              }
            }
            return arrFirst;
          }});


    vm.cpaBucketRequestSecond = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
            var arrFirst = [];
            for(var i=0; i<vm.cpaResult.length; i++) {
              if(+vm.cpaResult[i].cpa>=vm.backetsRanges.second.min && + vm.cpaResult[i].cpa<vm.backetsRanges.second.max) {
                arrFirst.push(vm.cpaResult[i]);
              }
            }
            return arrFirst;

      }
    });

    vm.cpaBucketRequestThird = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {

            var arrFirst = [];
            for(var i=0; i<vm.cpaResult.length; i++) {
              if(+vm.cpaResult[i].cpa>=vm.backetsRanges.third.min && +vm.cpaResult[i].cpa<vm.backetsRanges.third.max) {
                arrFirst.push(vm.cpaResult[i]);
              }
            }
            return arrFirst;

      }
    });

    vm.cpaBucketRequestFourth = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {

            var arrFirst = [];
            for(var i=0; i<vm.cpaResult.length; i++) {
              if(+vm.cpaResult[i].cpa>=vm.backetsRanges.fourth.min && +vm.cpaResult[i].cpa<vm.backetsRanges.fourth.max) {
                arrFirst.push(vm.cpaResult[i]);
              }
            }
            return arrFirst;

      }
    });


/** DATE PIKER **/
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
      }
    ];

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
          $state.reload();
        }
      }
    };



    /** PIE CHART CONTAINER - START **/
    vm.ctrlBbtns = {
      placement:{
        btn:'Placement',
        header:'Placement'
      },
      creativeId: {
        btn:'creative_id',
        header:'creative_id'
      },
      creativeSize: {
        btn:'creative_size',
        header:'creative_size'
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
      }
    };
    vm.pieChartHeader = $localStorage.pieChartHeader || vm.ctrlBbtns.placement.header;
    vm.btnsNodesArray = $window.$('.label-container')[0].children;


    /** SELECT SECTION/BTN UNDER LOADING PAGE - START **/
    for(var key in vm.ctrlBbtns) {
      if (vm.ctrlBbtns[key].header == vm.pieChartHeader) {
        vm.selectedSection = vm.ctrlBbtns[key].btn;
        $localStorage.selectedSection = vm.selectedSection;
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
      //vm.selectedSection = $localStorage.selectedSection;
      Array.prototype.forEach.call(vm.btnsNodesArray, function(node) {
        if(node.classList.contains('nav-btn-active')){
          node.classList.remove('nav-btn-active');
        }
      });
      $localStorage.pieChartHeader = vm.pieChartHeader;
      $event.currentTarget.classList.add('nav-btn-active');

      for(var key in vm.ctrlBbtns) {
        if (vm.ctrlBbtns[key].header == vm.pieChartHeader) {
          $localStorage.selectedSection = vm.ctrlBbtns[key].btn;
        }
      }

      $state.reload();
    };

    if(!vm.targetCpa) {
      vm.targetCpa = $localStorage.targetCpa || 1;
      $localStorage.targetCpa = vm.targetCpa;
    }

    vm.backetsRanges = {
      first:{
        min: 0,
        max: Number(vm.targetCpa).toFixed(2)
      },
      second:{
        min:Number(vm.targetCpa).toFixed(2),
        max:Number(vm.targetCpa*2).toFixed(2)
      },
      third: {
        min: Number(vm.targetCpa * 2).toFixed(2),
        max: Number(vm.targetCpa * 3).toFixed(2)
      },
      fourth: {
        min: Number(vm.targetCpa * 3).toFixed(2),
        max: Number(vm.targetCpa * 100000).toFixed(2)
      }
    };

    vm.targetCpaChange = function($event) {
      var targetCpaInt = Number($event.currentTarget.value);
      $localStorage.targetCpa = targetCpaInt;
      vm.backetsRanges = {
        first: {
          min: 0,
          max: (targetCpaInt).toFixed(2)
        },
        second: {
          min: (targetCpaInt).toFixed(2),
          max: (targetCpaInt * 2).toFixed(2)
        },
        third: {
          min: (targetCpaInt * 2).toFixed(2),
          max: (targetCpaInt * 3).toFixed(2)
        },
        fourth: {
          min: (targetCpaInt * 3).toFixed(2),
          max: (targetCpaInt * 100000).toFixed(2)
        }
      };

      $window.$('#backets-1').dxDataGrid('instance').refresh();
      $window.$('#backets-2').dxDataGrid('instance').refresh();
      $window.$('#backets-3').dxDataGrid('instance').refresh();
      $window.$('#backets-4').dxDataGrid('instance').refresh();

      return vm.backetsRanges;
    };

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
      bindingOptions: {
        dataSource: 'cpa.detailsStoreAll'
      },
      legend: {
        visible: false
      },
      tooltip: {
        enabled: true,
        format: {
          type: "millions",
          percentPrecision: 2
        },
        customizeTooltip: function (arg) {
          return {
            text: arg.argument + " - " + arg.value + '%'
          };
        }
      },
      series: [{
        argumentField: 'section',
        valueField: 'data',
        smallValuesGrouping: {
          mode: "topN",
          topCount: 25
        }
      }]
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
      bindingOptions: {
        dataSource: 'cpa.detailsStoreConversion'
      },
      legend: {
        visible: false
      },
      tooltip: {
        enabled: true,
        customizeTooltip: function (arg) {
          return {
            text: arg.argument + " - " + arg.value + '%'
          };
        }
      },
      series: [{
        argumentField: "section",
        valueField: "data",
        smallValuesGrouping: {
          mode: "topN",
          topCount: 25
        }
      }]
    };


    vm.columnsPlacement = [
      {
        caption: 'sellerid',
        dataField: 'sellerid'
      },
      {
        caption: 'sellername',
        dataField: 'sellername'
      },
      {
        caption: 'placementid',
        dataField: 'placementid'
      }, {
        caption:  'placementname',
        dataField: 'placementname'
      },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }
    ];

    vm.columnsCreativeId =  [{
      caption: 'creative id',
      dataField: 'creative'
    },{
      caption: 'creative name',
      dataField: 'creative_name'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];

    vm.columnsCreativeSize =  [{
      caption: 'size',
      dataField: 'size'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];

    vm.columnsOs =  [{
      caption: 'operating system id',
      dataField: 'operating_system'
    },{
      caption: 'operating system',
      dataField: 'operating_system_name'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];

    vm.columnsCarrier =  [{
      caption: 'carrier id',
      dataField: 'carrier'
    },{
      caption: 'carrier name',
      dataField: 'carrier_name'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];


    vm.columnsNetworkSeller =  [{
      caption: 'seller member',
      dataField: 'seller_member'
    },{
      caption: 'seller member name',
      dataField: 'seller_member_name'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];

    vm.columnsConnectionType =  [{
      caption: 'connection type',
      dataField: 'connection_type'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];
    vm.columnsDevice =  [{
      caption: 'device model',
      dataField: 'device_model'
    },{
      caption: 'device model name',
      dataField: 'device_model_name'
    },
      {
        caption:  'cpa, $',
        dataField: 'cpa',
        sortOrder: 'desc'
      }];

    if ($localStorage.selectedSection == "Placement") {
      vm.columnsSelected = vm.columnsPlacement;
    } else if ($localStorage.selectedSection == "creative_id") {
      vm.columnsSelected = vm.columnsCreativeId;
    }else if ($localStorage.selectedSection == "creative_size") {
      vm.columnsSelected = vm.columnsCreativeSize;
    }else if ($localStorage.selectedSection == "OS") {
      vm.columnsSelected = vm.columnsOs;
    }else if ($localStorage.selectedSection == "carrier") {
      vm.columnsSelected = vm.columnsCarrier;
    }else if ($localStorage.selectedSection == "network(seller)") {
      vm.columnsSelected = vm.columnsNetworkSeller;
    }else if ($localStorage.selectedSection == "connection_type") {
      vm.columnsSelected = vm.columnsConnectionType;
    }else if ($localStorage.selectedSection == "device") {
      vm.columnsSelected = vm.columnsDevice;
    }

    vm.cpaBucketFirst = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'cpa.cpaBucketRequestFirst'
      },
      howBorders: true,
      showRowLines: true,
      paging: {
        enabled: true,
        pageSize:10
      },
      remoteOperations: false,
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      columns: vm.columnsSelected,
      export: {
        enabled: true,
        fileName: "cpa_first"
      }
    };

    vm.cpaBucketSecond = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'cpa.cpaBucketRequestSecond'
      },
      howBorders: true,
      showRowLines: true,
      paging: {
        enabled: true,
        pageSize:10
      },
      remoteOperations: false,
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      columns: vm.columnsSelected,
      export: {
        enabled: true,
        fileName: "cpa_second"
      }
    };


    vm.cpaBucketThird = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'cpa.cpaBucketRequestThird'
      },
      howBorders: true,
      showRowLines: true,
      paging: {
        enabled: true,
        pageSize:10
      },
      remoteOperations: false,
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      columns: vm.columnsSelected,
      export: {
        enabled: true,
        fileName: "cpa_third"
      }
    };


    vm.cpaBucketFourth = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'cpa.cpaBucketRequestFourth'
      },
      howBorders: true,
      showRowLines: true,
      paging: {
        enabled: true,
        pageSize:10
      },
      remoteOperations: false,
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      columns: vm.columnsSelected,
      export: {
        enabled: true,
        fileName: "cpa_fourth"
      }
    };


  }
})();

