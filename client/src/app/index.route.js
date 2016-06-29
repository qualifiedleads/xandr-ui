(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'main'
      })
      .state('campaign', {
        url: '/campaign/:id',
        templateUrl: 'app/campaign/camp.html',
        controller: 'CampaignController',
        controllerAs: 'camp'
      });

    $urlRouterProvider.otherwise('/');
  }

})();
