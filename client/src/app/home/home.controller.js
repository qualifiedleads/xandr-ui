(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('HomeController', HomeController);

  /** @ngInject */
  function HomeController($localStorage, $cookies, $window, AdminService, Home) {
    var vm = this;
    vm.advertiser = {};
    vm.isEven = false;
    vm.userAuth = false;
    vm.bannerText = '';
    vm.video = false;
    vm.usual = false;
    vm.advertiser.name = Home.AdverInfo.advertiser_name;
    vm.advertiser.id = Home.AdverInfo.advertiser_id;
    vm.id = Home.AdverInfo.id;
    vm.name = Home.AdverInfo.campaign;

    if ($localStorage.advertiser.ad_type === 'videoAds') {
      vm.video = true;
    }

    if ($localStorage.advertiser.ad_type === 'usualAds' || $localStorage.advertiser.ad_type === null) {
      vm.usual = true;
    }

    AdminService.bannerTextReturn().then(function (res) {
      if (res.status == true) {
        vm.bannerText = res.text || '';
      }
    });

    vm.hideBanner = function () {
      vm.banner = $window.$('#techBanner');
      vm.banner.addClass('non-visible');
    };

    if (($cookies.get('token')) &&
      (($cookies.get('permission') == 'adminfull') || $cookies.get('permission') == 'adminread')) {
      vm.isEven = true;
      vm.userAuth = true;
    }

    if (($cookies.get('token')) &&
      (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
      vm.isEven = false;
      vm.userAuth = true;
    }

    vm.checked = function (value) {
      var wrapper = angular.element($window.document.querySelector('#wrapper'))[0];
      if (wrapper.classList.add('hidden-menu')) {
        wrapper.classList.remove('hidden-menu');
      }
    };

  }
})();
