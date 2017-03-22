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
        templateUrl: 'app/home/home.html',
        controller: 'HomeController',
        controllerAs: 'home'
      })
      .state('home.main', {
        url: '/main/:id',
        templateUrl: 'app/usual/main/main.html',
        controller: 'MainController',
        controllerAs: 'main',
        resolve: {
          advertiserParams: function(Auth,$stateParams, $state, Home){
            if (!$stateParams.id) {
              $state.go('/');
            }

            return Auth.advertiser($stateParams.id)
              .then(function (res) {
                if (res == undefined) {
                  $state.go('/');
                }
                Home.AdverInfo.advertiser_name = res.name;
                return res;
              });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.videomain', {
        url: '/video/main/:id',
        templateUrl: 'app/video/main/videomain.html',
        controller: 'VideoMainController',
        controllerAs: 'vmain',
        resolve: {
          advertiserParams: function(Auth,$stateParams, $state, Home){
            if (!$stateParams.id) {
              $state.go('/');
            }

            return Auth.advertiser($stateParams.id)
              .then(function (res) {
                if (res == undefined) {
                  $state.go('/');
                }
                Home.AdverInfo.advertiser_name = res.name;
                return res;
              });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.videocampaign', {
        url: '/video/campaign/:id',
        templateUrl: 'app/video/campaign/videocampaign.html',
        controller: 'VideoCampaignController',
        controllerAs: 'videocamp',
        resolve: {
          Campaign: function (CampMain, $stateParams, $state, Home) {
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              Home.AdverInfo = res;
              return res;
            });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.automaticcpm', {
        url: '/video/automatic/CPM/:id',
        templateUrl: 'app/video/automaticcpm/acpmc.html',
        controller: 'AutomaticCpmController',
        controllerAs: 'acpmc',
        resolve: {
          Campaign: function (CampMain, $stateParams, $state, Home) {
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              Home.AdverInfo = res;
              return res;
            });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.campaign', {
        url: '/campaign/:id',
        templateUrl: 'app/usual/campaign/campaign.html',
        controller: 'CampaignMainController',
        controllerAs: 'campmain',
        resolve: {
          Campaign: function (CampMain, $stateParams, $state, Home) {
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              Home.AdverInfo = res;
              return res;
            });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.optimiser', {
        url: '/optimiser/:id',
        templateUrl: 'app/usual/optimiser/optimiser.html',
        controller: 'CampaignOptimiserController',
        controllerAs: 'CO',
        resolve: {
          Campaign:  function(CampMain,$stateParams, $state, Home){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return Home.AdverInfo = res;
            });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.valuationByExpert', {
        url: '/valuationByExpert/',
        templateUrl: 'app/valuationByExpert/valuationByExpert.html',
        controller: 'valuationByExpertController',
        controllerAs: 'VBE',
        resolve: {
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('admin', {
        url: '/admin/',
        templateUrl: 'app/admin/admin.html',
        controller: 'AdminController',
        controllerAs: 'admin'
      })
      .state('home.rules', {
        url: '/rules/:id',
        templateUrl: 'app/usual/rules/rules.html',
        controller: 'rulesController',
        controllerAs: 'rulesC',
        resolve: {
          Campaign:  function(CampMain,$stateParams, $state, Home){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return Home.AdverInfo = res;
            });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.bcc', {
        url: '/video/bcc/:id',
        templateUrl: 'app/video/bcc/bcc.html',
        controller: 'BCCController',
        controllerAs: 'bcc',
        resolve: {
          Campaign:  function(CampMain,$stateParams, $state){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return res
            });
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      })
      .state('home.cpa', {
        url: '/cpa/:id',
        templateUrl: 'app/usual/cpa/cpa.html',
        controller: 'CPAController',
        controllerAs: 'cpa',
        resolve: {
          Campaign:  function(CampMain,$stateParams, $state,Home){
            if (!$stateParams.id) {
              $state.go('home.main');
            }
            return CampMain.nameCampaigns($stateParams.id).then(function (res) {
              return Home.AdverInfo = res;
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
          },
          TWStatus: function (AdminService, $stateParams, $state, $cookies) {
            return AdminService.getValueOfTech().then(function (res) {
              if ((res == "on") &&
                ($cookies.get('token')) &&
                (($cookies.get('permission') == 'userfull') || $cookies.get('permission') == 'userread')) {
                $state.go('auth');
              }
            });
          }
        }
      });

    $urlRouterProvider.otherwise('/');
  }

})();
