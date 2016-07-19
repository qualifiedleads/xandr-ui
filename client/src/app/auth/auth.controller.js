(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('AuthController', AuthController);

  /** @ngInject */
  function AuthController($log, $window, $state, $localStorage, $translate,  Auth, $cookies) {
    var vm = this;
    var LC = $translate.instant;
    vm.Auth = Auth;


    if (($cookies.get('token')) &&
      (($cookies.get('permission') =='adminfull') || $cookies.get('permission') =='adminread')){
      $window.$('.reg-form-wrapper')[0].classList.add('hide');
      $window.$('.advertiser-wrapper')[0].classList.add('show');
      $window.$('.admin-btn')[0].classList.add('show');
      $window.$('.admin-btn')[1].classList.add('show');
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') =='userfull') || $cookies.get('permission') =='userread')){
      $window.$('.reg-form-wrapper')[0].classList.add('hide');
      $window.$('.advertiser-wrapper')[0].classList.add('show');
      $window.$('.admin-btn')[0].classList.remove('show');
      $window.$('.admin-btn')[1].classList.add('show');
    }

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
      if(user || user.email && user.password) {
        return vm.Auth.authorization(user).then(function (res) {
          $cookies.put('token', res.token);
          $cookies.put('permission', res.permission);
          if ((res.token) && ((res.permission =='adminfull') || (res.permission =='adminread'))){
            $window.$('.reg-form-wrapper')[0].classList.add('hide');
            $window.$('.advertiser-wrapper')[0].classList.add('show');
            $window.$('.admin-btn')[0].classList.add('show');
            $window.$('.admin-btn')[1].classList.add('show');
          }
          if ((res.token) && ((res.permission =='userfull') || (res.permission =='userread'))){
            $window.$('.reg-form-wrapper')[0].classList.add('hide');
            $window.$('.advertiser-wrapper')[0].classList.add('show');
            $window.$('.admin-btn')[0].classList.remove('show');
            $window.$('.admin-btn')[1].classList.add('show');
          }
        }).catch(function (err) {
          $log(err);
        })
      }
    }

    function goToAdminPanel() {
      $state.go('admin');
    }

    function logout() {
      $cookies.remove('permission');
      $cookies.remove('token');
      $state.reload();
    }


    vm.goToAdminPanel = goToAdminPanel;
    vm.logout = logout;
    vm.submitForm = submitForm;
  }
})();
