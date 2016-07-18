(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('AuthController', AuthController);

  /** @ngInject */
  function AuthController($window, $state, $localStorage, $translate,  Auth, $cookies) {
    var vm = this;
    var LC = $translate.instant;
    vm.Auth = Auth;


    if ($cookies.get('token') && $cookies.get('role')=='adminfull'){
      $('.reg-form-wrapper')[0].classList.add('hide');
      $('.advertiser-wrapper')[0].classList.add('show');
      $('.admin-btn')[0].classList.add('show');
      $('.admin-btn')[1].classList.add('show');
    }

    if ($cookies.get('token') && $cookies.get('role')=='userfull'){
      $('.reg-form-wrapper')[0].classList.add('hide');
      $('.advertiser-wrapper')[0].classList.add('show');
      $('.admin-btn')[0].classList.remove('show');
      $('.admin-btn')[1].classList.add('show');
    }

    vm.admin = {
      id: 1,
      email:"admin@admin",
      password:"admin"
  //    permission:"adminfull"
    };


    vm.addButton={
      text: LC('AUTH.GO_BUTTON'),
      onClick: function () {
        $localStorage.advertiser = vm.selectedService;
        $state.go('home.main');
      }
    };

    vm.selectAdvertisersStore = new $window.DevExpress.data.CustomStore({
      totalCount: function () {
        return 0;
      },
      load: function () {
        return vm.Auth.advertisersList()
          .then(function (result) {
            return result;
          });
      }
    });

    vm.selectAdvertisers = {
      bindingOptions: {
        dataSource: 'auth.selectAdvertisersStore',
        value: 'auth.selectedService'
      },
      displayExpr: 'name',
      width: '200px'
    };

    function submitForm (user) {
      if(user) {
        $('.reg-form-wrapper')[0].classList.add('hide');
        $('.advertiser-wrapper')[0].classList.add('show');
        $('.admin-btn')[1].classList.remove('hide');
        if(user.login === vm.admin.login && user.password === vm.admin.password) {
          $('.admin-btn')[0].classList.remove('hide');
          $cookies.put('token', 'token');
          $cookies.put('role', 'adminfull');
        } else {
          $cookies.put('token', 'token');
          $cookies.put('role', 'userfull');
        }
      }

    }

    function goToAdminPanel() {
      $state.go('admin', {"id":vm.admin.id});
    }

    function logout() {
      $cookies.remove('role');
      $cookies.remove('token');
      $state.reload();
    }


    vm.goToAdminPanel = goToAdminPanel;
    vm.logout = logout;
    vm.submitForm = submitForm;
  }
})();
