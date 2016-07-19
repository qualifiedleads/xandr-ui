(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('AdminController', AdminController);

  /** @ngInject */
  function AdminController($window, $state, $localStorage, $translate, $cookies,  AdminService) {
    var vm = this;
    //var LC = $translate.instant;
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
      showBorders: true,
      alignment: 'left',
      bindingOptions: {
        dataSource: 'admin.users'
      },
      howBorders: true,
      showRowLines: true,
      align: 'left',
      editing: {
        allowDeleting: true
      },
      columns: [
        {
          caption: 'id',
          dataField: 'id'
        },
        {
          caption: 'email',
          dataField: 'email'
        },
        {
          caption: 'username',
          dataField: 'username'
        },
        {
          caption: 'first_name',
          dataField: 'first_name'
        },
        {
          caption: 'last_name',
          dataField: 'last_name'
        },
        {
          caption:  'apnexusname',
          dataField: 'apnexusname'
        },
        {
          caption:  'apnexus user id',
          dataField: 'apnexus_user'
        },
        {
          caption:  'permission',
          dataField: 'permission'
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
      placeholder:'Select the appnexus user',
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
