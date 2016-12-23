(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('HomeController', HomeController);

  /** @ngInject */
  function HomeController($localStorage, $state, $cookies, $window, $rootScope, AdminService) {
    var vm = this;
    vm.advertiser = {};
    vm.isEven = false;
    vm.userAuth = false;
    vm.bannerText = '';

    AdminService.bannerTextReturn().then(function (res) {
      if (res.status == true) {
        vm.bannerText = res.text || '';
      }
    });

    vm.hideBanner = function () {
      vm.banner = $window.$('#techBanner');
      vm.banner.addClass('non-visible');
    };

    if (($rootScope.id == null) && ($rootScope.name == null) && ($localStorage.campaign != null)) {
      $rootScope.id = $localStorage.campaign.id;
      $rootScope.name = $localStorage.campaign.name;
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') =='adminfull') || $cookies.get('permission') =='adminread')){
      vm.isEven = true;
      vm.userAuth =true;
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') =='userfull') || $cookies.get('permission') =='userread')){
      vm.isEven = false;
      vm.userAuth = true;
    }

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


  }
})();
