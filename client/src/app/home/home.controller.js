(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('HomeController', HomeController);

  /** @ngInject */
  function HomeController($localStorage, $state, $stateParams, $cookies, $window, $scope, $rootScope) {
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
  /*  vm.campId = Campaign.id;*/


    /*vm.checked = function(value) {
      var wrapper = angular.element($window.document.querySelector("#wrapper"))[0];
      if(value) {
        wrapper.classList.add('hidden-menu');
       } else {
        wrapper.classList.remove('hidden-menu');
       }
    };*/
    //wrapper.classList.add('hidden-menu');
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
