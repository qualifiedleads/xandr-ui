(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CampaignDetailsController', CampaignDetailsController);

  /** @ngInject */
  function CampaignDetailsController($window, $state, $localStorage, $translate, CampDetails, Campaign) {
    var vm = this;
    vm.Camp = CampDetails;
    vm.multipleTotalCount = 0;
    vm.checkChart = [];
    vm.by = 'imp,cvr,cpc,clicks,spend,conv,ctr';
    var LC = $translate.instant;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;



    vm.detailsStoreAll = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.detailsStoreAll(vm.campId, vm.dataStart, vm.dataEnd,$localStorage.selectedSection)
          .then(function (result) {
            return result.all;
          });
      }
    });

    vm.detailsStoreConversion = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.detailsStoreAll(vm.campId, vm.dataStart, vm.dataEnd,vm.by)
          .then(function (result) {
            return result.conversions;
          });
      }
    });

    vm.cpaBucketRequestFirst = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.bucketsCpa(vm.campId, vm.dataStart, vm.dataEnd)
          .then(function (result) {
            var arrFirst = [];
            for(var i=0; i<result.length; i++) {
              if(+result[i].cpa>=vm.backetsRanges.first.min && +result[i].cpa<vm.backetsRanges.first.max) {
                arrFirst.push(result[i]);
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
        return vm.Camp.bucketsCpa(vm.campId, vm.dataStart, vm.dataEnd)
          .then(function (result) {
            var arrFirst = [];
            for(var i=0; i<result.length; i++) {
              if(+result[i].cpa>=vm.backetsRanges.second.min && +result[i].cpa<vm.backetsRanges.second.max) {
                arrFirst.push(result[i]);
              }
            }
            return arrFirst;
          });
      }
    });

    vm.cpaBucketRequestThird = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.bucketsCpa(vm.campId, vm.dataStart, vm.dataEnd)
          .then(function (result) {
            var arrFirst = [];
            for(var i=0; i<result.length; i++) {
              if(+result[i].cpa>=vm.backetsRanges.third.min && +result[i].cpa<vm.backetsRanges.third.max) {
                arrFirst.push(result[i]);
              }
            }
            return arrFirst;
          });
      }
    });

    vm.cpaBucketRequestFourth = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Camp.bucketsCpa(vm.campId, vm.dataStart, vm.dataEnd)
          .then(function (result) {
            var arrFirst = [];
            for(var i=0; i<result.length; i++) {
              if(+result[i].cpa>=vm.backetsRanges.fourth.min && +result[i].cpa<vm.backetsRanges.fourth.max) {
                arrFirst.push(result[i]);
              }
            }
            return arrFirst;
          });
      }
    });


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
      viewability: {
        btn:'viewability',
        header:'viewability'
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

      Array.prototype.forEach.call(vm.btnsNodesArray, function(node) {
        if(node.classList.contains('nav-btn-active')){
          node.classList.remove('nav-btn-active');
        }
      });
      $localStorage.pieChartHeader = vm.pieChartHeader;
      $event.currentTarget.classList.add('nav-btn-active');

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

    // vm.cpaArrayFirst =  CampDetails.cpaBuckets(vm.backetsRanges.first.min, vm.backetsRanges.first.max);
    // vm.cpaArraySecond =  CampDetails.cpaBuckets(vm.backetsRanges.second.min, vm.backetsRanges.second.max);
    // vm.cpaArrayThird =  CampDetails.cpaBuckets(vm.backetsRanges.third.min, vm.backetsRanges.third.max);
    // vm.cpaArrayFourth =  CampDetails.cpaBuckets(vm.backetsRanges.fourth.min, vm.backetsRanges.fourth.max);


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
        dataSource: 'campdetails.detailsStoreAll'
      },
      resolveLabelOverlapping: 'shift',
      series: [{
        argumentField: 'section',
        valueField: 'data',
        label: {
          visible: true,
          connector: {
            visible: true,
            width: 0.5
          },
          format: "fixedPoint",
          customizeText: function (point) {
            return point.argumentText + ': <spend style="color: black; font-weight: bold"> ' + point.valueText + '</spend>';
          }
        },
        smallValuesGrouping: {
          mode: "smallValueThreshold",
          threshold: 4.5
        }
      }],
      legend: {
        horizontalAlignment: "center",
        verticalAlignment: "bottom"
      }
      // size: {
      //   width:370,
      //   height:300
      // }
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
      series: [{
        argumentField: "section",
        valueField: "data",
        label: {
          visible: true,
          connector: {
            visible: true,
            width: 0.5
          },
          format: "fixedPoint",
          customizeText: function (point) {
            return point.argumentText + ": " + point.valueText + "%";
          }
        },
        smallValuesGrouping: {
          mode: "smallValueThreshold",
          threshold: 4.5
        }
      }],
      legend: {
        horizontalAlignment: "center",
        verticalAlignment: "bottom"
      }
      // size: {
      //   width:370,
      //   height:300
      // }
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
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsCreativeSize =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsViewability =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsOs =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsCarrier =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsNetworkSeller =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsConnectionType =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];
    vm.columnsDevice =  [{
      caption: 'sellername',
      dataField: 'sellername'
    }];

    if ($localStorage.selectedSection == "Placement") {
      vm.columnsSelected = vm.columnsPlacement;
    } else if ($localStorage.selectedSection == "creative_id") {
      vm.columnsSelected = vm.columnsCreativeId;
    }else if ($localStorage.selectedSection == "creative_size") {
      vm.columnsSelected = vm.columnsCreativeSize;
    }else if ($localStorage.selectedSection == "viewability") {
      vm.columnsSelected = vm.columnsViewability;
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

