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
        templateUrl: 'app/campaignmain/campmain.html',
        controller: 'CampaignMainController',
        controllerAs: 'campmain',
        resolve: {
          Campaign: function (CampMain, $stateParams, $state) {
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return res
            });
          }
        }
      })
      .state('home.optimiser', {
        url: '/optimiser/:id',
        templateUrl: 'app/campaignOptimiser/campaignOptimiser.html',
        controller: 'CampaignOptimiserController',
        controllerAs: 'CO',
        resolve: {
          Campaign:  function(CampMain,$stateParams, $state){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return res
            });
          }
        }
      })
      .state('home.valuationByExpert', {
        url: '/valuationByExpert/',
        templateUrl: 'app/valuationByExpert/valuationByExpert.html',
        controller: 'valuationByExpertController',
        controllerAs: 'VBE',
      })
      .state('admin', {
        url: '/admin/',
        templateUrl: 'app/admin/admin.html',
        controller: 'AdminController',
        controllerAs: 'admin'
      })
      .state('home.rules', {
        url: '/rules/:id',
        templateUrl: 'app/rules/rules.html',
        controller: 'rulesController',
        controllerAs: 'rulesC'
      })
      .state('home.cpa', {
        url: '/cpa/:id',
        templateUrl: 'app/cpa/cpa.html',
        controller: 'CPAController',
        controllerAs: 'cpa',
        resolve: {
          Campaign:  function(CampMain,$stateParams, $state){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return res
            });
          },
          ChartDetails:  function(CPA,$stateParams, $state,$localStorage){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CPA.detailsStoreAll(
              $stateParams.id,
              $localStorage.dataStart,
              $localStorage.dataEnd,
              $localStorage.selectedSection
            ).then(function (result) {
              return result;
            })
              .catch(function (err) {
                return err;
              });
          },
          CpaBucketsAll:  function(CPA,$stateParams, $state,$localStorage){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CPA.bucketsCpa(
              $stateParams.id,
              $localStorage.dataStart,
              $localStorage.dataEnd,
              $localStorage.selectedSection
            ).then(function (result) {
              return result;
            })
              .catch(function (err) {
                return err;
              });
          }
        }
      });

    $urlRouterProvider.otherwise('/');
  }

})();
