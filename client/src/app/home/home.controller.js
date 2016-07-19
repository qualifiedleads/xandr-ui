(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('HomeController', HomeController);

  /** @ngInject */
  function HomeController($localStorage, $state, $document) {
    var vm = this;
    vm.advertiser = {};
    vm.a = 123;

    if($localStorage.advertiser == null){
      $state.go('auth');
    } else {
      vm.advertiser.name = $localStorage.advertiser.name;
    }

    vm.checked = function(value) {
      var wrapleft = angular.element($document.document.querySelector(".left-nav"))[0];
      var wrapmain = angular.element($document.document.querySelector(".main-nav"))[0];
      if(value === true){
        wrapleft.classList.add('left-menu-close');
        wrapmain.style.width = '100%';
       } else if (value === false) {
        wrapleft.classList.remove('left-menu-close');
        wrapmain.style.width = '';
       }
    };


  }
})();
