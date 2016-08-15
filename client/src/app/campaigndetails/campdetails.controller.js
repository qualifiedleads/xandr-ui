(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CampaignDetailsController', CampaignDetailsController);

  /** @ngInject */
  function CampaignDetailsController($window, $state, $localStorage, $translate, CampDetails, ChartDetails, Campaign) {
    var vm = this;
    vm.Camp = CampDetails;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';
    var LC = $translate.instant;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    vm.cpaResult = [];

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
        return vm.Camp.bucketsCpa(vm.campId, $localStorage.dataStart, $localStorage.dataEnd, $localStorage.selectedSection)
          .then(function (result) {
            vm.cpaResult = result;
            var arrFirst = [];
            for(var i=0; i<vm.cpaResult.length; i++) {
              if(+vm.cpaResult[i].cpa>=vm.backetsRanges.first.min && +vm.cpaResult[i].cpa<vm.backetsRanges.first.max) {
                arrFirst.push(vm.cpaResult[i]);
              }
            }
            return arrFirst;
          });
      }
    });

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
      vm.targetCpa = $localStorage.targetCpa || 3;
      $localStorage.targetCpa = vm.targetCpa;
    }

    vm.backetsRanges = {
      first:{
        min: 0,
        max: Number(vm.targetCpa).toFixed(1)
      },
      second:{
        min:Number(vm.targetCpa).toFixed(1),
        max:Number(vm.targetCpa*2).toFixed(1)
      },
      third: {
        min: Number(vm.targetCpa * 2).toFixed(1),
        max: Number(vm.targetCpa * 3).toFixed(1)
      },
      fourth: {
        min: Number(vm.targetCpa * 3).toFixed(1),
        max: Number(vm.targetCpa * 1000).toFixed(1)
      }
    };

    vm.targetCpaChange = function($event) {
      var targetCpaInt = Number($event.currentTarget.value);
      $localStorage.targetCpa = targetCpaInt;
      vm.backetsRanges = {
        first: {
          min: 0,
          max: (targetCpaInt).toFixed(1)
        },
        second: {
          min: (targetCpaInt).toFixed(1),
          max: (targetCpaInt * 2).toFixed(1)
        },
        third: {
          min: (targetCpaInt * 2).toFixed(1),
          max: (targetCpaInt * 3).toFixed(1)
        },
        fourth: {
          min: (targetCpaInt * 3).toFixed(1),
          max: (targetCpaInt * 1000).toFixed(1)
        }
      };
      // vm.cpaArrayFirst =  CampDetails.cpaBuckets(vm.backetsRanges.first.min, vm.backetsRanges.first.max);
      // vm.cpaArraySecond =  CampDetails.cpaBuckets(vm.backetsRanges.second.min, vm.backetsRanges.second.max);
      // vm.cpaArrayThird =  CampDetails.cpaBuckets(vm.backetsRanges.third.min, vm.backetsRanges.third.max);
      // vm.cpaArrayFourth =  CampDetails.cpaBuckets(vm.backetsRanges.fourth.min, vm.backetsRanges.fourth.max);

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
        dataSource: 'campdetails.detailsStoreAll',
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
        },
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
        dataSource: 'campdetails.detailsStoreConversion'
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
      }
    ];

    vm.columnsCreativeId =  [{
      caption: 'creative id',
      dataField: 'creative'
    },{
      caption: 'creative name',
      dataField: 'creative_name'
    }];

    vm.columnsCreativeSize =  [{
      caption: 'size',
      dataField: 'size'
    }];

    vm.columnsOs =  [{
      caption: 'operating system id',
      dataField: 'operating_system'
    },{
      caption: 'operating system',
      dataField: 'operating_system_name'
    }];

    vm.columnsCarrier =  [{
      caption: 'carrier id',
      dataField: 'carrier'
    },{
      caption: 'carrier name',
      dataField: 'carrier_name'
    }];


    vm.columnsNetworkSeller =  [{
      caption: 'seller member',
      dataField: 'seller_member'
    },{
      caption: 'seller member name',
      dataField: 'seller_member_name'
    }];

    vm.columnsConnectionType =  [{
      caption: 'connection type',
      dataField: 'connection_type'
    }];
    vm.columnsDevice =  [{
      caption: 'device model',
      dataField: 'device_model'
    },{
      caption: 'device model name',
      dataField: 'device_model_name'
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
        dataSource: 'campdetails.cpaBucketRequestFirst'
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
      columns: vm.columnsSelected
    };

    vm.cpaBucketSecond = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'campdetails.cpaBucketRequestSecond'
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
      columns: vm.columnsSelected
    };


    vm.cpaBucketThird = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'campdetails.cpaBucketRequestThird'
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
      columns: vm.columnsSelected
    };


    vm.cpaBucketFourth = {
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'campdetails.cpaBucketRequestFourth'
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
      columns: vm.columnsSelected
    };


  }
})();

