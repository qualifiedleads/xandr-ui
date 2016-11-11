(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('HomeController', HomeController);

  /** @ngInject */
  function HomeController($localStorage, $state, $cookies, $window, $rootScope) {
    var vm = this;
    vm.advertiser = {};
    vm.isEven = false;

    if (($rootScope.id == null) && ($rootScope.name == null) && ($localStorage.campaign != null)) {
      $rootScope.id = $localStorage.campaign.id;
      $rootScope.name = $localStorage.campaign.name;
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') =='adminfull') || $cookies.get('permission') =='adminread')){
      vm.isEven = true;
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') =='userfull') || $cookies.get('permission') =='userread')){
      vm.isEven = false;
    }

    vm.goToMainPage = function () {
      $state.go('auth');
    };

    if($localStorage.advertiser == null){
      $state.go('auth');
    } else {
      vm.advertiser.name = $localStorage.advertiser.name;
    }
    vm.checked = function(value) {
      var wrapper = angular.element($window.document.querySelector("#wrapper"))[0];
      if(wrapper.classList.add('hidden-menu')) {
        wrapper.classList.remove('hidden-menu');
      }
    };
    function goToAdminPanel() {
      $state.go('admin');
    }

    vm.goToAdminPanel = goToAdminPanel;

  }
})();
