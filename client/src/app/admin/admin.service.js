(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .service('AdminService', AdminService);

  /** @ngInject */
  function AdminService($http, $cookies, $window) {
    var _this = this;
    var _totalCount = 0;

    function selectNexusUsersStore() {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return _totalCount;
        },
        load: function () {
          return _appNexusUser();
        }
      });
    }

    function _appNexusUser() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/appnexus/user'
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }
    // .then(function (result) {
    //   return result;
    // })

    function techRecordStore() {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },
        load: function () {
          return _techRecord();
        }
      });
    }

    function _techRecord() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/technicalwork'
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }


    function usersStore() {
      return new $window.DevExpress.data.CustomStore({
        totalCount: function () {
          return 0;
        },
        load: function () {
          return _usersList()
            .then(function (result) {
              return result;
            });
        },
        remove: function (user) {
          return _usersRemove(user.id);
        }
      });
    }

    function _usersList() {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/user/'
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function _usersRemove(id) {
      return $http({
        method: 'DELETE',
        url: '/api/v1/user/' + id,
        headers: { 'Authorization': 'Token ' + $cookies.get('token') }
      })
        .then(function (response) {
          return response.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function addUser(user) {
      return $http({
        method: 'POST',
        url: '/api/v1/user/',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        data: user
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function bannerTextReturn() {
      return  'Этот текст будет показан при проведении технических работ';
      // $http({
      //   method: 'GET',
      //   headers: { 'Authorization': 'Token ' + $cookies.get('token') },
      //   url: '/api/v1/baner/show'
      // })
      //   .then(function (res) {
      //     return res.data;
      //   })
      //   .catch(function (err) {
      //     //$window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      //     'Этот текст будет показан'
      //   });
    }

    function bannerTextRecord (text) {
      return $http({
        method: 'POST',
        url: '/api/v1/user/',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        data: text
      });
      // .then(function (res) {
      //   return res.data;
      // })
      // .catch(function (err) {
      //   $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      // });
    }

    function statusTech (status) {
      return $http({
        method: 'POST',
        url: '/api/v1/technicalwork',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        data: status
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function getValueOfTech () {
      return $http({
        method: 'GET',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        url: '/api/v1/technicalwork/last'
      })
        .then(function (res) {
          return res.data;
        })
        .catch(function (err) {
          $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
        });
    }

    function bannerTextClean (clean) {
      return $http({
        method: 'POST',
        url: '/api/v1/user/',
        headers: { 'Authorization': 'Token ' + $cookies.get('token') },
        data: clean
      });
      // .then(function (res) {
      //   return res.data;
      // })
      // .catch(function (err) {
      //   $window.DevExpress.ui.notify(err.data.detail, "error", 4000);
      // });
    }


    _this.selectNexusUsersStore = selectNexusUsersStore;
    _this.usersStore = usersStore;
    _this.addUser = addUser;
    _this.bannerTextReturn = bannerTextReturn;
    _this.techRecordStore = techRecordStore;
    _this.bannerTextRecord = bannerTextRecord;
    _this.statusTech = statusTech;
    _this.getValueOfTech = getValueOfTech;
    _this.bannerTextClean = bannerTextClean;
  }
})();
