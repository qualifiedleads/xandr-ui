(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('AdminController', AdminController);

  /** @ngInject */
  function AdminController($window, $state, $localStorage, $translate, $cookies,  AdminService) {
    var vm = this;
    var LC = $translate.instant;
    vm.Admin = AdminService;

    function goToMainPage () {
      $state.go('auth');
    }

    vm.users = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Admin.usersList()
        .then(function (result) {
          return result;
        });
      },
      remove: function (user) {
        return vm.Admin.usersRemove(user.id);
      }
    });

    vm.listOfUsers = {
      remoteOperations: false,
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'admin.users'
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
/*        {
          caption: LC('ADMIN.LIST-USER.USER-NAME'),
          dataField: 'username',
          alignment: 'center'
        },*/
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
    };

    vm.selectNexusUsers = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Admin.appNexusUser()
        .then(function (result) {
          return result;
        });
      }
    });

    vm.selectAppNexusUser = {
      bindingOptions: {
        dataSource: 'admin.selectNexusUsers',
        value: 'admin.selectedService'
      },
      placeholder: LC('ADMIN.ANU.SELECT-NEXUS-USER'),
      displayExpr: 'username'
    };



    function submitForm(user) {
      if (vm.selectedService) {
        user.apnexus_user = vm.selectedService.id;
        user.apnexusname = vm.selectedService.username;
      } else {
        user.apnexus_user = null;
        user.apnexusname = null;
      }
      if ( user.permission == 'adminfull' || user.permission == 'adminread' ){
        user.apnexus_user = null;
      }
      user.username = user.email;
      return vm.Admin.addUser(user)
      .then(function () {
        vm.user = {};
        vm.userForm.$setPristine();
        $window.$('#usersList').dxDataGrid('instance').refresh();
      });

    }


    vm.submitForm = submitForm;
    vm.goToMainPage = goToMainPage;
  }
})();
