(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .controller('AuthController', AuthController);

  /** @ngInject */
  function AuthController($log, $window, $state, $localStorage, $translate, Auth, $cookies, $cookieStore) {
    var vm = this;
    var LC = $translate.instant;
    vm.Auth = Auth;


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

    vm.addButton = {
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

    function submitForm(user) {

      if (user || user.email && user.password) {
        $cookies.remove('csrftoken');
        $cookies.remove('sessionid');
        $cookies.remove('permission');
        return vm.Auth.authorization(user).then(function (res) {
          if (res.status == 200 ){
            $localStorage.$reset();
            $cookies.put('token', res.data.token);
            res.data.permission = 'adminfull';
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
            $cookies.remove('csrftoken');
            $cookies.remove('sessionid');
            $cookies.remove('permission');
            $cookies.remove('token');
            console.log(res.statusText);
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
      $cookies.remove('csrftoken');
      $cookies.remove('sessionid');
      $state.reload();
    }


    vm.goToAdminPanel = goToAdminPanel;
    vm.logout = logout;
    vm.submitForm = submitForm;
  }
})();
