(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('AdminController', AdminController);

  /** @ngInject */
  function AdminController($window, $state,  $translate, AdminService) {
    var vm = this;
    var LC = $translate.instant;

    vm.goToMainPage = function () {
      $state.go('auth');
    };

    vm.submitForm = function (user) {
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
      return AdminService.addUser(user)
      .then(function () {
        vm.user = {};
        vm.userForm.$setPristine();
        $window.$('#usersList').dxDataGrid('instance').refresh();
      });
    };

    vm.usersStore = AdminService.usersStore();
    vm.selectNexusUsersStore = AdminService.selectNexusUsersStore();

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
