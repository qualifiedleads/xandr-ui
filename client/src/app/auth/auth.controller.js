(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('AuthController', AuthController);

  /** @ngInject */
  function AuthController($window, $state, $localStorage, $translate,  Auth) {
    var vm = this;
    var LC = $translate.instant;
    vm.Auth = Auth;

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

      $('.reg-form-wrapper')[0].classList.add('hide');
      $('.advertiser-wrapper')[0].classList.add('show');
    }



    vm.submitForm = submitForm;
  }
})();
