'use strict';

angular
  .module('pjtLayout')
  .controller('RootController', RootController);

/** @ngInject */
function RootController($window, $state, $translate, $translateLocalStorage,$cookies, $scope) {
  var vm = this;

  if (($cookies.get('token')) &&
    (($cookies.get('permission') =='adminfull') || $cookies.get('permission') =='adminread')){
    vm.isEven = true;
    //$window.$('#homeAdm').show();
  } 

  if (($cookies.get('token')) &&
    (($cookies.get('permission') =='userfull') || $cookies.get('permission') =='userread')){
    vm.isEven = false;
    //$window.$('#homeAdm').hide();
  }

    //return false;




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


  function goToAdminPanel() {
    $state.go('admin');
  }

  vm.goToAdminPanel = goToAdminPanel;
  vm.logout = logout;

}
