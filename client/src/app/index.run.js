(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .run(runBlock);

  /** @ngInject */
  function runBlock($log, $state,$http,$rootScope,$stateParams,$localStorage,$window, $cookies) {

    //security watcher
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
    var stateChange = $rootScope.$on('$stateChangeStart', function (event, toState) {
      if (toState.name != 'auth') {
        if (!$cookies.get('token') && !$cookies.get('permission')){
          $localStorage.$reset();
          $window.location = "/";
        }
      }
      if (toState.name == 'admin') {
        if ((($cookies.get('permission') =='userfull') || $cookies.get('permission') =='userread')){
          $localStorage.$reset();
          $window.location = "/";
        }
      }
    });
    $rootScope.$on('$destroy', stateChange);

    $log.debug('runBlock end');
  }

})();
