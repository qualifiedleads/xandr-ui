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


    vm.admin = {
      login:"admin",
      password:"admin"
    };

/*    vm.appNexusUsers =  [{
      "id": "1",
      "login":"cnm@gmail.com",
      "name":"CNM"
    },{
      "id": "2",
      "login":"BBC@gmail.com",
      "name":"BBC"
    },{
      "id": "3",
      "login":"Discovery@gmail.com",
      "name":"Discovery"
    },{
      "id": "4",
      "login":"HTB@gmail.com",
      "name":"HTB"
    },{
      "id": "5",
      "login":"ICTV@gmail.com",
      "name":"ICTV"
    }];*/



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
            //$localStorage.usersList = result;
            return result;
          });
      }
    });
/*    if (!$localStorage.usersList){
      $localStorage.usersList = vm.users;
    }*/

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
        },  {
          caption:  'appnexus',
          dataField: 'name'
        }, {
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
      displayExpr: 'name'
    };



    function submitForm(user) {
      //$localStorage.usersList.push(user);
        vm.user = {};
        vm.userForm.$setPristine(gulp);
        console.log(vm.selectedService);
        $('#usersList').dxDataGrid('instance').refresh();
    }

    function logout() {
      $cookies.remove('role');
      $cookies.remove('token');
      $state.go('auth');
    }


    vm.logout = logout;
    vm.submitForm = submitForm;
    vm.goToMainPage = goToMainPage;
  }
})();
