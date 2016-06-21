'use strict';

angular
  .module('pjtLayout')
  .controller('RootController', RootController);

/** @ngInject */
function RootController() {
  var vm = this;

  vm.advertiser = {"name":"Adam"};

}
