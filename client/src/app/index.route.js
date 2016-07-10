(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('auth', {
        url: '/',
        templateUrl: 'app/auth/auth.html',
        controller: 'AuthController',
        controllerAs: 'auth'
      })
      .state('home', {
        url: '/home',
        templateUrl: 'app/home/home.html',
        controller: 'HomeController',
        controllerAs: 'home'
      })
      .state('home.main', {
        url: '/main',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'main'
      })
      .state('home.campaign', {
        url: '/campaign/:id',
        templateUrl: 'app/campaign/camp.html',
        controller: 'CampaignController',
        controllerAs: 'camp',
        resolve:{
          Campaign:  function(Camp,$stateParams){
            if (!$stateParams.id) {
              $stat.go(home.main)
            }
            return Camp.nameCampaigns($stateParams.id).then(function (res) {
              return res
            });
          }
        }
      });

    $urlRouterProvider.otherwise('/');
  }

})();
