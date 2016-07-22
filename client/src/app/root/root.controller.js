'use strict';

angular
  .module('pjtLayout')
  .controller('RootController', RootController);

/** @ngInject */
function RootController($window, $state, $translate, $translateLocalStorage,$cookies) {
  var vm = this;

  $window.Globalize.culture($translateLocalStorage.get('TRANSLATE_LANG_KEY'));
  vm.changeLang = function(langKey) {
    $translate.use(langKey);
    $window.Globalize.culture(langKey);
    $state.reload();
  };

  function logout() {
    $cookies.remove('permission');
    $cookies.remove('token');
    $state.go('auth');
  }


  vm.logout = logout;

}
