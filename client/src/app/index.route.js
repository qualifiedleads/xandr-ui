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
        templateUrl:  'app/campaign/camp.html',
        abstract: true
      })
      .state('home.campaign.details', {
        url: '/campaign/:id',
        views: {
          details: {
            templateUrl: 'app/campaignmain/campmain.html',
            controller: 'CampaignControllerMain',
            controllerAs: 'campmain',
            resolve: {
              Campaign:  function(CampMain,$stateParams, $state){
                if (!$stateParams.id) {
                  $state.go(home.main)
                }
                return CampMain.nameCampaigns($stateParams.id).then(function (res) {
                  return res
                });
              }
            }
          },
          info: {
            templateUrl: 'app/campaigndetails/campdetails.html',
            controller: 'CampaignDetails',
            controllerAs: 'campdetails',
            resolve: {
              Campaign:  function(CampMain,$stateParams, $state){
                if (!$stateParams.id) {
                  $state.go(home.main)
                }
                return CampMain.nameCampaigns($stateParams.id).then(function (res) {
                  return res
                });
              }
            }
          }
        }
      });

    $urlRouterProvider.otherwise('/');
  }

})();
