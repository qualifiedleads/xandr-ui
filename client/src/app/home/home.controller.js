(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('HomeController', HomeController);

  /** @ngInject */
  function HomeController($localStorage, $state, $cookies, $window) {
    var vm = this;
    vm.advertiser = {};
    vm.a = 123;

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


    if($localStorage.advertiser == null){
      $state.go('auth');
    } else {
      vm.advertiser.name = $localStorage.advertiser.name;
    }

    vm.checked = function(value) {
      var wrapleft = angular.element($window.document.querySelector(".left-nav"))[0];
      var wrapmain = angular.element($window.document.querySelector(".main-nav"))[0];
      if(value === true){
        wrapleft.classList.add('left-menu-close');
        wrapmain.style.width = '100%';
        wrapmain.style.marginLeft = 0;
       } else if (value === false) {
        wrapleft.classList.remove('left-menu-close');
        wrapmain.style.width = '';
        wrapmain.style.marginLeft = '';
       }
    };

    function goToAdminPanel() {
      $state.go('admin');
    }

    vm.goToAdminPanel = goToAdminPanel;

  }
})();
