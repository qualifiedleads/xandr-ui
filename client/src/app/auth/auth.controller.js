(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('AuthController', AuthController);

  /** @ngInject */
  function AuthController($window, $state, $localStorage, $translate, Auth, $cookies) {
    var vm = this;
    var LC = $translate.instant;

    if (($cookies.get('token')) &&
        (($cookies.get('permission') == 'adminfull') || $cookies.get('permission') == 'adminread')) {
      $window.$('.reg-form-wrapper')[0].classList.add('hide');
      $window.$('.advertiser-wrapper')[0].classList.add('show');
      $window.$('.admin-btn')[0].classList.add('show');
      $window.$('.admin-btn')[1].classList.add('show');
    }

    if (($cookies.get('token')) &&
        (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
      $window.$('.reg-form-wrapper')[0].classList.add('hide');
      $window.$('.advertiser-wrapper')[0].classList.add('show');
      $window.$('.admin-btn')[0].classList.remove('show');
      $window.$('.admin-btn')[1].classList.add('show');
    }

    vm.selectAdvertisersStore = Auth.selectAdvertisersStore();

    vm.submitForm = function (user) {
      if (user!= undefined && user.email != undefined && user.password != undefined) {
        $cookies.remove('permission');
        $cookies.remove('token');
        return Auth.authorization(user).then(function (res) {
          if (res.status == 200) {
            $localStorage.$reset();
            $cookies.put('token', res.data.token);
            $cookies.put('permission', res.data.permission);
            if ((res.data.token) && ((res.data.permission == 'adminfull') || (res.data.permission == 'adminread'))) {
              $window.$('.reg-form-wrapper')[0].classList.add('hide');
              $window.$('.advertiser-wrapper')[0].classList.add('show');
              $window.$('.admin-btn')[0].classList.add('show');
              $window.$('.admin-btn')[1].classList.add('show');
            }
            if ((res.data.token) && ((res.data.permission == 'userfull') || (res.data.permission == 'userread'))) {
              $window.$('.reg-form-wrapper')[0].classList.add('hide');
              $window.$('.advertiser-wrapper')[0].classList.add('show');
              $window.$('.admin-btn')[0].classList.remove('show');
              $window.$('.admin-btn')[1].classList.add('show');
            }
          } else {
            $cookies.remove('permission');
            $cookies.remove('token');
          }
        });
      } else {
        $window.DevExpress.ui.notify(LC('AUTH.EMAIL-OR-PASSWORD-EMPTY'), "error", 4000);
      }
    };

    vm.goToAdminPanel = function () {
      $state.go('admin');
    };

    vm.logout = function () {
      $cookies.remove('permission');
      $cookies.remove('token');
      $state.reload();
    };

    vm.UI = {
      addButton: {
        text: LC('AUTH.GO_BUTTON'),
        onClick: function () {
          $localStorage.advertiser = vm.selectedService;
          $state.go('home.main');
        }
      },
      selectAdvertisers: {

        bindingOptions: {

          dataSource: 'auth.selectAdvertisersStore',
          value: 'auth.selectedService'
        },
        displayExpr: 'name',
        width: '200px'
      }
    };

  }
})();
