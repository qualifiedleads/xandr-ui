(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('AdminController', AdminController);

  /** @ngInject */
  function AdminController($window, $state,  $translate, AdminService, $localStorage ) {
    var vm = this;
    var LC = $translate.instant;

    vm.goToMainPage = function () {
      $state.go('auth');
    };

    vm.bannerText = AdminService.bannerTextReturn();
    if (!$localStorage.bannerText) {
      $localStorage.bannerText = vm.bannerText;
    }

    vm.submitBannerText = function (bannerText) {
      $localStorage.bannerText = bannerText;
      vm.newTextBaner = {
        text: bannerText,
        date: new Date()
      };
      AdminService.bannerTextRecord(vm.newTextBaner);
    };

    vm.cleanBannerText = function () {
      vm.bannerText = '';
      vm.bannerText.$setPristine();
      AdminService.bannerTextClean(vm.bannerText);
    };

    vm.changeTechWork = function (val) {
      vm.status = {
        value: val,
        date: new Date()
      };
      $localStorage.valueOfTech = val;
      AdminService.statusTech(vm.status);
      $window.$('#techRecords').dxDataGrid('instance').refresh();
    };

    AdminService.getValueOfTech().then(function (data) {
      vm.name = data;
    });

    if(!$localStorage.button) {
      $localStorage.button = 'first';
    }

    if($localStorage.button) {
      if($localStorage.button === 'second'){
        $window.$('.post-first').addClass('non-active');
        $window.$('.post-second').removeClass('non-active');
        $window.$('.link-first').removeClass('btn-success');
        $window.$('.link-first').addClass('btn-default');
        $window.$('.link-second').addClass('btn-success');
        $localStorage.button = null;
        $localStorage.button = 'second';
      }
      if($localStorage.button === 'first'){
        $window.$('.post-first').removeClass('non-active');
        $window.$('.post-first').addClass('active');
        $window.$('.post-second').addClass('non-active');
        $window.$('.link-first').addClass('btn-success');
        $window.$('.link-second').removeClass('btn-success');
        $localStorage.button = null;
        $localStorage.button = 'first';
      }
    }

    vm.valueOfTech = function (name) {
      $localStorage.valueOfTech = null;
      $localStorage.valueOfTech = name;
    };


    vm.changeTab = function(value) {
      if (value ==="first") {
        $window.$('.post-first').removeClass('non-active');
        $window.$('.post-first').addClass('active');
        $window.$('.post-second').addClass('non-active');
        $window.$('.link-first').addClass('btn-success');
        $window.$('.link-second').removeClass('btn-success');
        $localStorage.button = null;
        $localStorage.button = value;
      }
      if (value ==='second') {
        $window.$('.post-first').addClass('non-active');
        $window.$('.post-second').removeClass('non-active');
        $window.$('.link-first').removeClass('btn-success');
        $window.$('.link-first').addClass('btn-default');
        $window.$('.link-second').addClass('btn-success');
        $localStorage.button = null;
        $localStorage.button = value;
      }
    };


    vm.submitForm = function (user) {
      if (vm.selectedService) {
        user.apnexus_user = vm.selectedService.id;
        user.apnexusname = vm.selectedService.userxtname;
      } else {
        user.apnexus_user = null;
        user.apnexusname = null;
      }
      if ( user.permission == 'adminfull' || user.permission == 'adminread' ){
        user.apnexus_user = null;
      }
      user.username = user.email;
      return AdminService.addUser(user)
        .then(function () {
          vm.user = {};
          vm.userForm.$setPristine();
          $window.$('#usersList').dxDataGrid('instance').refresh();
        });
    };

    vm.usersStore = AdminService.usersStore();
    vm.selectNexusUsersStore = AdminService.selectNexusUsersStore();
    vm.techRecordStore = AdminService.techRecordStore();



    vm.techRecords = {
      remoteOperations: false,
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'admin.techRecordStore'
      },
      headerFilter: {
        visible: true
      },
      filterRow: {
        visible: true,
        applyFilter: "auto"
      },
      pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [10, 30, 50],
        visible: true,
        showNavigationButtons: true
      },
      allowColumnReordering: true,
      allowColumnResizing: true,
      columnAutoWidth: true,
      wordWrapEnabled: true,
      howBorders: true,
      showRowLines: true,
      align: 'left',
      loadPanel: {
        shadingColor: "rgba(0,0,0,0.4)",
        visible: false,
        showIndicator: true,
        showPane: true,
        shading: true,
        closeOnOutsideClick: false
      },
      editing: {
        allowDeleting: false,
        allowDragging: true
      },
      columns: [
        {
          caption: 'date',
          dataField: 'date',
          alignment: 'center'

        },
        {
          caption: 'status',
          dataField: 'status',
          alignment: 'center'
        }
      ]
    };
    // selectAppNexusUser: {
    //   bindingOptions: {
    //     dataSource: 'admin.selectNexusUsersStore',
    //     value: 'admin.selectedService'
    //   },
    //   placeholder: LC('ADMIN.ANU.SELECT-NEXUS-USER'),
    //   displayExpr: 'username'
    // }


    vm.UI = {
      listOfUsers: {
        remoteOperations: false,
        showBorders: true,
        alignment: 'left',
        bindingOptions: {
          dataSource: 'admin.usersStore'
        },
        headerFilter: {
          visible: true
        },
        filterRow: {
          visible: true,
          applyFilter: "auto"
        },
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
        },
        allowColumnReordering: true,
        allowColumnResizing: true,
        columnAutoWidth: true,
        wordWrapEnabled: true,
        howBorders: true,
        showRowLines: true,
        align: 'left',
        loadPanel: {
          shadingColor: "rgba(0,0,0,0.4)",
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false
        },
        editing: {
          allowDeleting: true
        },
        columns: [
          {
            caption: 'id',
            dataField: 'id',
            alignment: 'center'

          },
          {
            caption: LC('ADMIN.LIST-USER.EMAIL'),
            dataField: 'email',
            alignment: 'center'
          },
          {
            caption: LC('ADMIN.LIST-USER.FIRST-NAME'),
            dataField: 'first_name',
            alignment: 'center'
          },
          {
            caption: LC('ADMIN.LIST-USER.LAST-NAME'),
            dataField: 'last_name',
            alignment: 'center'
          },
          {
            caption:  LC('ADMIN.LIST-USER.APNEXUS-ID'),
            dataField: 'apnexusname',
            alignment: 'center'
          },
          {
            caption:  LC('ADMIN.LIST-USER.APNEXUS-NAME'),
            dataField: 'apnexus_user',
            alignment: 'center'
          },
          {
            caption:  LC('ADMIN.LIST-USER.PERMISSION'),
            dataField: 'permission',
            alignment: 'center'
          }
        ]
      },
      selectAppNexusUser: {
        bindingOptions: {
          dataSource: 'admin.selectNexusUsersStore',
          value: 'admin.selectedService'
        },
        placeholder: LC('ADMIN.ANU.SELECT-NEXUS-USER'),
        displayExpr: 'username'
      }
    };
  }
})();
