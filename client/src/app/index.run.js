(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log, $state,$http,$rootScope,$stateParams,$localStorage,$window, $cookies) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
    $rootScope.$on('$stateChangeStart', function (event, toState) {
/*      $http.get("/api/user/me")
      .catch(function (error) {
        console.log(error.status);
        if (error.status == 401) {
          $localStorage.$reset();
          $http.get("/logout")
          .then(function (response) {
            $window.location = "/";
          })
        }
      });*/
/*      if (!$cookies.get('token') && !$cookies.get('role')){
        $cookies.remove('role');
        $cookies.remove('token');
        $window.location = "/";
      }*/

/*      if ($window.location != "/") {
        if (!$cookies.get('token') && !$cookies.get('role')){
          $cookies.remove('role');
          $cookies.remove('token');
          $window.location = "/";
        }
      }*/

/*      if (toState.name != 'head') {
        if (localStorage.getItem('ngStorage-options') == null) {
          $localStorage.$reset();
          $http.get("/logout")
          .then(function (response) {
            $window.location = "/";
          })
          .catch(function (error) {
            console.log(error);
          });
        }
      }*/
    })

    $log.debug('runBlock end');
  }

})();
