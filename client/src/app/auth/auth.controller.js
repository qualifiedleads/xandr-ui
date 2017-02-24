(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('AuthController', AuthController);

  /** @ngInject */
  function AuthController($window, $state, $localStorage, $translate, Auth, $cookies, AdminService) {
    var vm = this;
    var LC = $translate.instant;
    vm.bannerShow = false;
    vm.userLogOut = false;
    vm.adminPanel = false;
    if (($cookies.get('token')) &&
      (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
      AdminService.getValueOfTech()
        .then(function (res) {
          if (res == 'on') {
            vm.bannerShow = true;
            return AdminService.bannerTextReturn().then(function (res) {
              vm.bannerText = res.text;
            });
          }
        });
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') == 'adminfull') || $cookies.get('permission') == 'adminread')) {
      $window.$('.reg-form-wrapper')[0].classList.add('hide');
      $window.$('.advertiser-wrapper')[0].classList.add('show');
      vm.userLogOut = true;
      vm.adminPanel = true;
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
      $window.$('.reg-form-wrapper')[0].classList.add('hide');
      $window.$('.advertiser-wrapper')[0].classList.add('show');
      vm.userLogOut = true;
      vm.adminPanel = false;
    }

    vm.selectAdvertisersStore = Auth.selectAdvertisersStore();

    vm.submitForm = function (user) {
      if (user != undefined && user.email != undefined && user.password != undefined) {
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
              vm.userLogOut = true;
              vm.adminPanel = true;
            }

            if ((res.data.token) && ((res.data.permission == 'userfull') || (res.data.permission == 'userread'))) {
              $window.$('.reg-form-wrapper')[0].classList.add('hide');
              $window.$('.advertiser-wrapper')[0].classList.add('show');
              vm.userLogOut = true;
              vm.adminPanel = false;
              AdminService.getValueOfTech()
                .then(function (res) {
                  if (res == 'on') {
                    vm.bannerShow = true;
                    return AdminService.bannerTextReturn().then(function (res) {
                      vm.bannerText = res.text;
                    });
                  }
                });
            }
          } else {
            $cookies.remove('permission');
            $cookies.remove('token');
          }
        });
      } else {
        $window.DevExpress.ui.notify(LC('AUTH.EMAIL-OR-PASSWORD-EMPTY'), 'error', 4000);
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
          if (vm.selectedService.ad_type === 'usualAds' || vm.selectedService.ad_type === null) {
            $state.go('home.main');
          }

          if (vm.selectedService.ad_type == 'videoAds') {
            $state.go('home.videomain');
          }

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
