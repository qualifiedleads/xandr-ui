(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('CampaignOptimiserController', CampaignOptimiserController);

  /** @ngInject */
  function CampaignOptimiserController($window, $state, $localStorage, $translate, Campaign, CampaignOptimiser) {
    var vm = this;
	  vm.CampaignOptimiser = CampaignOptimiser;
    vm.campName = Campaign.campaign;
    vm.campId = Campaign.id;
    var LC = $translate.instant;
    /**
     *  Top navigator
     * */
    vm.navCamp = {
      text: LC('CO.CAMPAIGN-HOME'),
      onClick: function () {
        $state.go('home.campaign.details',{"id":vm.campId});
      }
    };

    vm.navView = {
      text: LC('CO.OPTIMIZER-VIEW'),
      onClick: function () {
        $state.go('home.campaignoptimiser',{"id":vm.campId});
      }
    };

    vm.navList = {
      text: LC('CO.SUSPEND-LIST'),
      onClick: function () {
        $state.go('CO.campaignoptimiser',{"id":vm.campId});
      }
    };

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






	  /** MULTIPLE 2 - START **/

	  vm.state='';
	  vm.selectCell = {
		  dataSource: [
			  {'name': 'White List',
				  'state':'whiteList'},
			  {'name': 'Black List',
				  'state':'blackList'},
			  {'name': 'Suspended',
				  'state':'suspended'}
		  ],
		  disabled:true,
		  placeholder: 'Select a state',
		  displayExpr: 'name',
		  valueExpr: vm.state,
		  onSelectionChanged: function(e) {
			  var selectedRows = $('#gridContainer2')[0].querySelectorAll('[aria-selected="true"]');
			  var stateSelected = e.selectedItem.state;
			  console.log(stateSelected);
			  if(selectedRows[0]) {
				  var selectedArr = [];
				  for (var i=0; i<selectedRows.length; i++){
					  selectedArr.push(selectedRows[i].firstChild.innerText);
				  }
				  console.log(selectedArr);

			  }
		  }
	  };


	  vm.gridStore = new $window.DevExpress.data.CustomStore({
		  totalCount: function () {
			  return 0;
		  },
		  load: function (loadOptions) {
			  return vm.CampaignOptimiser.campaignDomains(vm.campId, vm.dataEnd, vm.dataStart, loadOptions.skip,
				  loadOptions.take, loadOptions.sort, loadOptions.order,loadOptions.filter)
			  .then(function (result) {
				  //$localStorage.gridStore = result;
				  return result;
			  });
		  }
	  });

	  vm.selectedItems = [];
	  vm.chartOptionsFuncgrid = [];
	  if ($localStorage.boxPlotData == null){
		  $localStorage.boxPlotData = vm.boxPlotData;
	  }

	  vm.state='';
	  vm.selectCell = {
		  dataSource: [
			  {'name': 'White List',
				  'state':'whiteList'},
			  {'name': 'Black List',
				  'state':'blackList'},
			  {'name': 'Suspended',
				  'state':'suspended'}
		  ],
		  disabled:true,
		  placeholder: 'Select a state',
		  displayExpr: 'name',
		  valueExpr: vm.state,
		  onSelectionChanged: function(e) {
			  var selectedRows = $('#gridContainer2')[0].querySelectorAll('[aria-selected="true"]');
			  var stateSelected = e.selectedItem.state;
			  console.log(stateSelected);
			  if(selectedRows[0]) {
				  var selectedArr = [];
				  for (var i=0; i<selectedRows.length; i++){
					  selectedArr.push(selectedRows[i].firstChild.innerText);
				  }
				  console.log(selectedArr);

			  }
		  }
	  };

	  vm.dataGridOptionsCampaign = {
	    onInitialized: function (data) {
		    vm.dataGridOptionsMultipleFunc = data.component;
		    vm.dataGridOptionsMultipleFunc._controllers.columns._commandColumns[1].visibleIndex = 9;
	    },
	    onRowPrepared: function(data) {
		    vm.objectData = data;
		    if(vm.objectData.rowType == 'data') {
			    //console.log(vm.objectData);
			    var allRowBtns = data.rowElement[0].childNodes[9];
			    var state = data.data.state;
			    if(state.whiteList == "true"){
				    allRowBtns.classList.add('active-white');
			    }
			    if(state.blackList == "true"){
				    allRowBtns.classList.add('active-black');
			    }
			    if(state.suspended == "true"){
				    allRowBtns.classList.add('active-suspended');
			    }
		    }
	    },
	    showBorders: true,
	    alignment: 'left',
	    headerFilter: {
		    visible: true
	    },
		  editing: {
	    	allowUpdating: true,
			  mode: "batch"
	    },
	    bindingOptions: {
		    dataSource: 'CO.gridStore',
		    allowColumnResizing: 'true'
	    },
	    pager: {
		    showPageSizeSelector: true,
		    allowedPageSizes: [10, 30, 50],
		    visible: true,
		    showNavigationButtons: true
	    },
	    howBorders: true,
	    showRowLines: true,
	    columns: [
		    {
			    caption: LC('MAIN.CAMPAIGN.COLUMNS.PLACEMENT'),
			    dataField: 'placement',
			    allowEditing: false
		    },
		    {
			    caption: LC('MAIN.CAMPAIGN.COLUMNS.NETWORK'),
			    dataField: 'NetworkPublisher',
			    allowEditing: false
		    },
		    {
			    caption: LC('MAIN.CAMPAIGN.COLUMNS.CONV'),
			    dataField: 'conv',
			    allowEditing: false
		    }, {
			    caption:  LC('MAIN.CAMPAIGN.COLUMNS.IMP'),
			    dataField: 'imp',
			    allowEditing: false
		    }, {
			    caption:  LC('MAIN.CAMPAIGN.COLUMNS.CLICKS'),
			    dataField: 'clicks',
			    allowEditing: false
		    }, {
			    caption:  LC('MAIN.CAMPAIGN.COLUMNS.CPC'),
			    dataField: 'cpc',
			    allowEditing: false
		    },
		    {
			    caption: LC('MAIN.CAMPAIGN.COLUMNS.CPM'),
			    dataField: 'cpm',
			    allowEditing: false
		    },
		    {
			    caption: LC('MAIN.CAMPAIGN.COLUMNS.CVR'),
			    dataField: 'cvr',
			    allowEditing: true
		    },
		    {
			    caption: LC('MAIN.CAMPAIGN.COLUMNS.CTR'),
			    dataField: 'ctr',
			    allowEditing: true
		    },
		    {
			    caption: 'State',
			    width: 300,
			    columnIndex: 16,
			    headerCellTemplate: 'headerCellTemplate',
			    cellTemplate: function (container, options) {
				    $("<div />").dxButton({
					    text: 'white list',
					    height:30,
					    width: 89,
					    disabled: true,
					    onClick: function (e) {
						    console.log(options.data);
						    var parentWhiteBtn = e.element[0].parentNode;
						    console.log(parentWhiteBtn);
						    if (parentWhiteBtn.classList.contains('active-white')) {
							    parentWhiteBtn.classList.remove('active-white');
							    parentWhiteBtn.classList.add('unactive-white');
							    options.data.state.whiteList = 'false';
						    } else if (!parentWhiteBtn.classList.contains('active-white')){
							    parentWhiteBtn.classList.remove('unactive-white');
							    parentWhiteBtn.classList.add('active-white');
							    options.data.state.whiteList = 'true';
							    options.data.state.suspended = 'false';
							    options.data.state.blackList = 'false';
							    parentWhiteBtn.classList.remove('active-black');
							    parentWhiteBtn.classList.remove('active-suspended');
						    }

					    }
				    }).addClass('white-list').appendTo(container);

				    $("<div />").dxButton({
					    text: 'black list',
					    height:30,
					    width: 89,
					    disabled: true,
					    onClick: function (e) {
						    //console.log(e);
						    var parentWhiteBtn = e.element[0].parentNode;
						    //console.log(parentWhiteBtn);
						    if (parentWhiteBtn.classList.contains('active-black')) {
							    parentWhiteBtn.classList.remove('active-black');
							    parentWhiteBtn.classList.add('unactive-black');
							    options.data.state.blackList = 'false';
						    } else if (!parentWhiteBtn.classList.contains('active-black')){
							    parentWhiteBtn.classList.remove('unactive-black');
							    parentWhiteBtn.classList.add('active-black');
							    options.data.state.blackList = 'true';
							    options.data.state.suspended = 'false';
							    options.data.state.whiteList = 'false';
							    parentWhiteBtn.classList.remove('active-white');
							    parentWhiteBtn.classList.remove('active-suspended');
						    }

					    }
				    }).addClass('black-list').appendTo(container);

				    $("<div />").dxButton({
					    text: 'suspended',
					    height:30,
					    width: 95,
					    disabled: true,
					    onClick: function (e) {
						    //console.log(e);
						    var parentWhiteBtn = e.element[0].parentNode;
						    //console.log(parentWhiteBtn);
						    if (parentWhiteBtn.classList.contains('active-suspended')) {
							    parentWhiteBtn.classList.remove('active-suspended');
							    parentWhiteBtn.classList.add('unactive-suspended');
							    options.data.state.suspended = 'false';
						    } else if (!parentWhiteBtn.classList.contains('active-suspended')){
							    parentWhiteBtn.classList.remove('unactive-suspended');
							    parentWhiteBtn.classList.add('active-suspended');
							    options.data.state.suspended = 'true';
							    options.data.state.whiteList = 'false';
							    options.data.state.blackList = 'false';
							    parentWhiteBtn.classList.remove('active-white');
							    parentWhiteBtn.classList.remove('active-black');

						    }

					    }
				    }).addClass('suspended').appendTo(container);
			    }
		    }
	    ],
	    selection: {
		    mode: 'multiple',
		    showCheckBoxesMode: 'always'
	    },
	    onSelectionChanged: function (data) {
		    vm.selectedItems = data.selectedRowsData;
		    vm.disabled = !vm.selectedItems.length;
	    }
    };
	  /** MULTIPLE - END **/


	  /** MULTIPLE 3 - START **/

	  vm.state3='';
	  vm.selectCell3 = {
		  dataSource: [
			  {'name': 'White List',
				  'state':'whiteList'},
			  {'name': 'Black List',
				  'state':'blackList'},
			  {'name': 'Suspended',
				  'state':'suspended'}
		  ],
		  disabled:true,
		  placeholder: 'Select a state',
		  displayExpr: 'name',
		  valueExpr: vm.state,
		  onSelectionChanged: function(e) {
			  var selectedRows = $('#gridContainer3')[0].querySelectorAll('[aria-selected="true"]');
			  var stateSelected = e.selectedItem.state;
			  console.log(stateSelected);
			  if(selectedRows[0]) {
				  var selectedArr = [];
				  for (var i=0; i<selectedRows.length; i++){
					  selectedArr.push(selectedRows[i].firstChild.innerText);
				  }
				  console.log(selectedArr);

			  }
		  }
	  };


	  vm.gridStore3 = new $window.DevExpress.data.CustomStore({
		  totalCount: function () {
			  return 0;
		  },
		  load: function (loadOptions) {
			  return vm.CampaignOptimiser.campaignDomains(vm.campId, vm.dataEnd, vm.dataStart, loadOptions.skip,
				  loadOptions.take, loadOptions.sort, loadOptions.order,loadOptions.filter)
			  .then(function (result) {
				  //$localStorage.gridStore = result;
				  return result;
			  });
		  }
	  });

	  vm.selectedItems = [];
	  vm.chartOptionsFuncgrid = [];
	  if ($localStorage.boxPlotData == null){
		  $localStorage.boxPlotData = vm.boxPlotData;
	  }

	  vm.state='';
	  vm.selectCell = {
		  dataSource: [
			  {'name': 'White List',
				  'state':'whiteList'},
			  {'name': 'Black List',
				  'state':'blackList'},
			  {'name': 'Suspended',
				  'state':'suspended'}
		  ],
		  disabled:true,
		  placeholder: 'Select a state',
		  displayExpr: 'name',
		  valueExpr: vm.state,
		  onSelectionChanged: function(e) {
			  var selectedRows = $('#gridContainer3')[0].querySelectorAll('[aria-selected="true"]');
			  var stateSelected = e.selectedItem.state;
			  console.log(stateSelected);
			  if(selectedRows[0]) {
				  var selectedArr = [];
				  for (var i=0; i<selectedRows.length; i++){
					  selectedArr.push(selectedRows[i].firstChild.innerText);
				  }
				  console.log(selectedArr);

			  }
		  }
	  };

	  vm.dataGridOptionsCampaign3 = {
		  onInitialized: function (data) {
			  vm.dataGridOptionsMultipleFunc3 = data.component;
			  vm.dataGridOptionsMultipleFunc3._controllers.columns._commandColumns[1].visibleIndex = 9;
		  },
		  onRowPrepared: function(data) {
			  vm.objectData = data;
			  if(vm.objectData.rowType == 'data') {
				  //console.log(vm.objectData);
				  var allRowBtns = data.rowElement[0].childNodes[9];
				  var state = data.data.state;
				  if(state.whiteList == "true"){
					  allRowBtns.classList.add('active-white');
				  }
				  if(state.blackList == "true"){
					  allRowBtns.classList.add('active-black');
				  }
				  if(state.suspended == "true"){
					  allRowBtns.classList.add('active-suspended');
				  }
			  }
		  },
		  showBorders: true,
		  alignment: 'left',
		  headerFilter: {
			  visible: true
		  },
		  bindingOptions: {
			  dataSource: 'CO.gridStore3',
			  allowColumnResizing: 'true'
		  },
		  pager: {
			  showPageSizeSelector: true,
			  allowedPageSizes: [10, 30, 50],
			  visible: true,
			  showNavigationButtons: true
		  },
		  howBorders: true,
		  showRowLines: true,
		  columns: [
			  {
				  caption: LC('MAIN.CAMPAIGN.COLUMNS.PLACEMENT'),
				  dataField: 'placement'
			  },
			  {
				  caption: LC('MAIN.CAMPAIGN.COLUMNS.NETWORK'),
				  dataField: 'NetworkPublisher'
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
				  caption: 'State',
				  width: 207,
				  columnIndex: 16,
				  headerCellTemplate: 'headerCellTemplate',
				  cellTemplate: function (container, options) {
					  $("<div />").dxButton({
						  text: 'white list',
						  height:30,
						  width: 89,
						  disabled: true,
						  onClick: function (e) {
							  console.log(options.data);
							  var parentWhiteBtn = e.element[0].parentNode;
							  console.log(parentWhiteBtn);
							  if (parentWhiteBtn.classList.contains('active-white')) {
								  parentWhiteBtn.classList.remove('active-white');
								  parentWhiteBtn.classList.add('unactive-white');
								  options.data.state.whiteList = 'false';
							  } else if (!parentWhiteBtn.classList.contains('active-white')){
								  parentWhiteBtn.classList.remove('unactive-white');
								  parentWhiteBtn.classList.add('active-white');
								  options.data.state.whiteList = 'true';
								  options.data.state.suspended = 'false';
								  options.data.state.blackList = 'false';
								  parentWhiteBtn.classList.remove('active-black');
								  parentWhiteBtn.classList.remove('active-suspended');
							  }

						  }
					  }).addClass('white-list').appendTo(container);


					  $("<div />").dxButton({
						  text: 'suspended',
						  height:30,
						  width: 95,
						  disabled: true,
						  onClick: function (e) {
							  //console.log(e);
							  var parentWhiteBtn = e.element[0].parentNode;
							  //console.log(parentWhiteBtn);
							  if (parentWhiteBtn.classList.contains('active-suspended')) {
								  parentWhiteBtn.classList.remove('active-suspended');
								  parentWhiteBtn.classList.add('unactive-suspended');
								  options.data.state.suspended = 'false';
							  } else if (!parentWhiteBtn.classList.contains('active-suspended')){
								  parentWhiteBtn.classList.remove('unactive-suspended');
								  parentWhiteBtn.classList.add('active-suspended');
								  options.data.state.suspended = 'true';
								  options.data.state.whiteList = 'false';
								  options.data.state.blackList = 'false';
								  parentWhiteBtn.classList.remove('active-white');
								  parentWhiteBtn.classList.remove('active-black');

							  }

						  }
					  }).addClass('suspended').appendTo(container);
				  }
			  }
		  ],
		  selection: {
			  mode: 'multiple',
			  showCheckBoxesMode: 'always'
		  },
		  onSelectionChanged: function (data) {
			  vm.selectedItems = data.selectedRowsData;
			  vm.disabled = !vm.selectedItems.length;
		  }
	  };
	  /** MULTIPLE - END **/



	  /** MULTIPLE 4 - START **/

	  vm.state4='';
	  vm.selectCell4 = {
		  dataSource: [
			  {'name': 'White List',
				  'state':'whiteList'},
			  {'name': 'Black List',
				  'state':'blackList'},
			  {'name': 'Suspended',
				  'state':'suspended'}
		  ],
		  disabled:true,
		  placeholder: 'Select a state',
		  displayExpr: 'name',
		  valueExpr: vm.state,
		  onSelectionChanged: function(e) {
			  var selectedRows = $('#gridContainer4')[0].querySelectorAll('[aria-selected="true"]');
			  var stateSelected = e.selectedItem.state;
			  console.log(stateSelected);
			  if(selectedRows[0]) {
				  var selectedArr = [];
				  for (var i=0; i<selectedRows.length; i++){
					  selectedArr.push(selectedRows[i].firstChild.innerText);
				  }
				  console.log(selectedArr);

			  }
		  }
	  };


	  vm.gridStore4 = new $window.DevExpress.data.CustomStore({
		  totalCount: function () {
			  return 0;
		  },
		  load: function (loadOptions) {
			  return vm.CampaignOptimiser.campaignDomains(vm.campId, vm.dataEnd, vm.dataStart, loadOptions.skip,
				  loadOptions.take, loadOptions.sort, loadOptions.order,loadOptions.filter)
			  .then(function (result) {
				  //$localStorage.gridStore = result;
				  return result;
			  });
		  }
	  });

	  vm.selectedItems = [];
	  vm.chartOptionsFuncgrid = [];
	  if ($localStorage.boxPlotData == null){
		  $localStorage.boxPlotData = vm.boxPlotData;
	  }

	  vm.state='';
	  vm.selectCell = {
		  dataSource: [
			  {'name': 'White List',
				  'state':'whiteList'},
			  {'name': 'Black List',
				  'state':'blackList'},
			  {'name': 'Suspended',
				  'state':'suspended'}
		  ],
		  disabled:true,
		  placeholder: 'Select a state',
		  displayExpr: 'name',
		  valueExpr: vm.state,
		  onSelectionChanged: function(e) {
			  var selectedRows = $('#gridContainer4')[0].querySelectorAll('[aria-selected="true"]');
			  var stateSelected = e.selectedItem.state;
			  console.log(stateSelected);
			  if(selectedRows[0]) {
				  var selectedArr = [];
				  for (var i=0; i<selectedRows.length; i++){
					  selectedArr.push(selectedRows[i].firstChild.innerText);
				  }
				  console.log(selectedArr);

			  }
		  }
	  };

	  vm.dataGridOptionsCampaign4 = {
		  onInitialized: function (data) {
			  vm.dataGridOptionsMultipleFunc4 = data.component;
			  vm.dataGridOptionsMultipleFunc4._controllers.columns._commandColumns[1].visibleIndex = 9;
		  },
		  onRowPrepared: function(data) {
			  vm.objectData = data;
			  if(vm.objectData.rowType == 'data') {
				  //console.log(vm.objectData);
				  var allRowBtns = data.rowElement[0].childNodes[9];
				  var state = data.data.state;
				  if(state.whiteList == "true"){
					  allRowBtns.classList.add('active-white');
				  }
				  if(state.blackList == "true"){
					  allRowBtns.classList.add('active-black');
				  }
				  if(state.suspended == "true"){
					  allRowBtns.classList.add('active-suspended');
				  }
			  }
		  },
		  showBorders: true,
		  alignment: 'left',
		  headerFilter: {
			  visible: true
		  },
		  bindingOptions: {
			  dataSource: 'CO.gridStore3',
			  allowColumnResizing: 'true'
		  },
		  pager: {
			  showPageSizeSelector: true,
			  allowedPageSizes: [10, 30, 50],
			  visible: true,
			  showNavigationButtons: true
		  },
		  howBorders: true,
		  showRowLines: true,
		  columns: [
			  {
				  caption: LC('MAIN.CAMPAIGN.COLUMNS.PLACEMENT'),
				  dataField: 'placement'
			  },
			  {
				  caption: LC('MAIN.CAMPAIGN.COLUMNS.NETWORK'),
				  dataField: 'NetworkPublisher'
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
				  caption: 'State',
				  width: 207,
				  columnIndex: 16,
				  headerCellTemplate: 'headerCellTemplate',
				  cellTemplate: function (container, options) {


					  $("<div />").dxButton({
						  text: 'black list',
						  height:30,
						  width: 89,
						  disabled: true,
						  onClick: function (e) {
							  //console.log(e);
							  var parentWhiteBtn = e.element[0].parentNode;
							  //console.log(parentWhiteBtn);
							  if (parentWhiteBtn.classList.contains('active-black')) {
								  parentWhiteBtn.classList.remove('active-black');
								  parentWhiteBtn.classList.add('unactive-black');
								  options.data.state.blackList = 'false';
							  } else if (!parentWhiteBtn.classList.contains('active-black')){
								  parentWhiteBtn.classList.remove('unactive-black');
								  parentWhiteBtn.classList.add('active-black');
								  options.data.state.blackList = 'true';
								  options.data.state.suspended = 'false';
								  options.data.state.whiteList = 'false';
								  parentWhiteBtn.classList.remove('active-white');
								  parentWhiteBtn.classList.remove('active-suspended');
							  }

						  }
					  }).addClass('black-list').appendTo(container);

					  $("<div />").dxButton({
						  text: 'suspended',
						  height:30,
						  width: 95,
						  disabled: true,
						  onClick: function (e) {
							  //console.log(e);
							  var parentWhiteBtn = e.element[0].parentNode;
							  //console.log(parentWhiteBtn);
							  if (parentWhiteBtn.classList.contains('active-suspended')) {
								  parentWhiteBtn.classList.remove('active-suspended');
								  parentWhiteBtn.classList.add('unactive-suspended');
								  options.data.state.suspended = 'false';
							  } else if (!parentWhiteBtn.classList.contains('active-suspended')){
								  parentWhiteBtn.classList.remove('unactive-suspended');
								  parentWhiteBtn.classList.add('active-suspended');
								  options.data.state.suspended = 'true';
								  options.data.state.whiteList = 'false';
								  options.data.state.blackList = 'false';
								  parentWhiteBtn.classList.remove('active-white');
								  parentWhiteBtn.classList.remove('active-black');

							  }

						  }
					  }).addClass('suspended').appendTo(container);
				  }
			  }
		  ],
		  selection: {
			  mode: 'multiple',
			  showCheckBoxesMode: 'always'
		  },
		  onSelectionChanged: function (data) {
			  vm.selectedItems = data.selectedRowsData;
			  vm.disabled = !vm.selectedItems.length;
		  }
	  };
	  /** MULTIPLE - END **/

  }
})();
