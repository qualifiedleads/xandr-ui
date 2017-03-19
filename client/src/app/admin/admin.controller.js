(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('AdminController', AdminController);

  /** @ngInject */
  function AdminController($window, $state,  $translate, AdminService, $localStorage) {
    var vm = this;
    var LC = $translate.instant;
    vm.first = true;
    vm.second = false;
    vm.third = false;
    vm.statusBanner = '';
    vm.goToMainPage = function () {
      $state.go('auth');
    };

    AdminService.bannerTextReturn().then(function (res) {
      vm.bannerText = res.text;
      if (res.status == true) {
        vm.statusBanner = 'ON';
      } else {
        vm.statusBanner = 'OFF';
      }

    });

    vm.submitBannerText = function (bannerText) {
      vm.newTextBaner = {
        text: bannerText,
        status: true
      };
      AdminService.bannerTextRecord(vm.newTextBaner).then(function (res) {
        if (res.status == true) {
          vm.statusBanner = 'ON';
        } else {
          vm.statusBanner = 'OFF';
        }
      });
    };

    vm.cleanBannerText = function () {
      return AdminService.bannerOff().then(function (res) {
        if (res.status == true) {
          vm.statusBanner = 'ON';
        } else {
          vm.statusBanner = 'OFF';
        }
      });
    };

    vm.changeTechWork = function (val) {
      vm.status = {
        value: val,
        date: new Date()
      };
      AdminService.statusTech(vm.status);
      $window.$('#techRecords').dxDataGrid('instance').refresh();
    };

    AdminService.getValueOfTech().then(function (data) {
      vm.name = data;
    });

    vm.changeTab = function (value) {
      $window.$('.link-second').removeClass('btn-success');
      $window.$('.link-first').removeClass('btn-success');
      $window.$('.link-third').removeClass('btn-success');
      vm.first = false;
      vm.second = false;
      vm.third = false;
      if (value === 'first') {
        vm.first = true;
        $window.$('.link-first').addClass('btn-success');
      }

      if (value === 'second') {
        $window.$('.link-second').addClass('btn-success');
        vm.second = true;
      }

      if (value === 'third') {
        $window.$('.link-third').addClass('btn-success');
        vm.third = true;
      }
    };

    vm.submitForm = function (user) {
      if (vm.selectedService) {
        user.apnexus_user = vm.selectedService.id;
        user.apnexusname = vm.selectedService.userxtname;
      } else {
        user.apnexus_user = null;
        user.apnexusname = null;
      }

      if (user.permission == 'adminfull' || user.permission == 'adminread') {
        user.apnexus_user = null;
      }

      user.username = user.email;
      return AdminService.addUser(user)
        .then(function () {
          vm.user = {};
          vm.userForm.$setPristine();
          $window.$('#usersList').dxDataGrid('instance').refresh();
        });
    };

    vm.usersStore = AdminService.usersStore();
    vm.advertiserListStore = AdminService.advertiserListStore();
    vm.selectNexusUsersStore = AdminService.selectNexusUsersStore();
    vm.techRecordStore = AdminService.techRecordStore();

    vm.UI = {
      listOfUsers: {
        remoteOperations: false,
        showBorders: true,
        alignment: 'left',
        bindingOptions: {
          dataSource: 'admin.usersStore'
        },
        headerFilter: {
          visible: true
        },
        filterRow: {
          visible: true,
          applyFilter: 'auto'
        },
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
        },
        allowColumnReordering: true,
        allowColumnResizing: true,
        wordWrapEnabled: true,
        howBorders: true,
        showRowLines: true,
        align: 'left',
        loadPanel: {
          shadingColor: 'rgba(0,0,0,0.4)',
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false
        },
        editing: {
          allowDeleting: true
        },
        columns: [
          {
            caption: 'id',
            dataField: 'id',
            alignment: 'center'

          },
          {
            caption: LC('ADMIN.LIST-USER.EMAIL'),
            dataField: 'email',
            alignment: 'center'
          },
          {
            caption: LC('ADMIN.LIST-USER.FIRST-NAME'),
            dataField: 'first_name',
            alignment: 'center'
          },
          {
            caption: LC('ADMIN.LIST-USER.LAST-NAME'),
            dataField: 'last_name',
            alignment: 'center'
          },
          {
            caption:  LC('ADMIN.LIST-USER.APNEXUS-ID'),
            dataField: 'apnexusname',
            alignment: 'center'
          },
          {
            caption:  LC('ADMIN.LIST-USER.APNEXUS-NAME'),
            dataField: 'apnexus_user',
            alignment: 'center'
          },
          {
            caption:  LC('ADMIN.LIST-USER.PERMISSION'),
            dataField: 'permission',
            alignment: 'center'
          }
        ]
      },
      selectAppNexusUser: {
        bindingOptions: {
          dataSource: 'admin.selectNexusUsersStore',
          value: 'admin.selectedService'
        },
        placeholder: LC('ADMIN.ANU.SELECT-NEXUS-USER'),
        displayExpr: 'username'
      },
      techRecords: {
        remoteOperations: false,
        showBorders: true,
        alignment: 'left',
        bindingOptions: {
          dataSource: 'admin.techRecordStore'
        },
        headerFilter: {
          visible: true
        },
        filterRow: {
          visible: true,
          applyFilter: 'auto'
        },
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
        },
        allowColumnReordering: true,
        allowColumnResizing: true,
        columnAutoWidth: true,
        wordWrapEnabled: true,
        howBorders: true,
        showRowLines: true,
        align: 'left',
        loadPanel: {
          shadingColor: 'rgba(0,0,0,0.4)',
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false
        },
        editing: {
          allowDeleting: false,
          allowDragging: true
        },
        columns: [
          {
            caption:  LC('ADMIN.TECHNICAL-WORK.TECH-DATE'),
            dataField: 'date',
            alignment: 'center',
            sortOrder: 'desc'
          },
          {
            caption: LC('ADMIN.TECHNICAL-WORK.TECH-STATUS'),
            dataField: 'status',
            alignment: 'center'
          }
        ]
      },
      advertiserList: {
        remoteOperations: false,
        showBorders: true,
        alignment: 'left',
        bindingOptions: {
          dataSource: 'admin.advertiserListStore'
        },
        headerFilter: {
          visible: true
        },
        filterRow: {
          visible: true,
          applyFilter: 'auto'
        },
        pager: {
          showPageSizeSelector: true,
          allowedPageSizes: [10, 30, 50],
          visible: true,
          showNavigationButtons: true
        },
        allowColumnReordering: true,
        allowColumnResizing: true,
        wordWrapEnabled: true,
        howBorders: true,
        showRowLines: true,
        align: 'left',
        loadPanel: {
          shadingColor: 'rgba(0,0,0,0.4)',
          visible: false,
          showIndicator: true,
          showPane: true,
          shading: true,
          closeOnOutsideClick: false
        },
        columns: [
          {
            caption: LC('ADMIN.ADVERTISER-LIST.ID'),
            dataField: 'id',
            alignment: 'left'
          },
          {
            caption: LC('ADMIN.ADVERTISER-LIST.NAME'),
            dataField: 'name',
            alignment: 'left'
          },
          {
            caption: LC('ADMIN.ADVERTISER-LIST.AD-TYPE'),
            width: 204,
            columnIndex: 16,
            allowEditing: false,
            dataField: 'ad_type',
            alignment: 'left',
            cellTemplate: function (container, options) {
              var usualAds = $window.$('<div />').dxButton({
                text: 'Usual',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  var w = $window.$('div.state-white' + options.data.id);
                  var b = $window.$('div.state-black' + options.data.id);
                  w.dxButton('instance').option('disabled', true);
                  b.dxButton('instance').option('disabled', true);
                  w.removeClass('active-white');
                  b.removeClass('active-white');
                  AdminService.editAdvertiserList(options.data.id, 'usualAds')
                    .then(function (res) {
                      w.dxButton('instance').option('disabled', false);
                      b.dxButton('instance').option('disabled', false);
                      if (res == 404) {
                        $window.DevExpress.ui.notify('Not found', 'warning', 4000);
                        $('#gridContainerWhite').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res == 503) {
                        $window.DevExpress.ui.notify('Not connect to appnexus server, please try again later', 'warning', 4000);
                        $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res !== 'Unactive') {
                        w.addClass('active-white');
                      }

                      return res;
                    })
                    .catch(function (err) {
                      return err;
                    });
                }
              });

              if (options.data.ad_type == 'usualAds') {
                usualAds.addClass('state-white' + options.data.id).addClass('active-white').appendTo(container);
              } else {
                usualAds.addClass('state-white' + options.data.id).appendTo(container);
              }

              var videoAds = $window.$('<div />').dxButton({
                text: 'Video',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  var w = $window.$('div.state-white' + options.data.id);
                  var b = $window.$('div.state-black' + options.data.id);
                  w.dxButton('instance').option('disabled', true);
                  b.dxButton('instance').option('disabled', true);
                  w.removeClass('active-white');
                  b.removeClass('active-white');
                  AdminService.editAdvertiserList(options.data.id, 'videoAds')
                    .then(function (res) {
                      w.dxButton('instance').option('disabled', false);
                      b.dxButton('instance').option('disabled', false);
                      if (res == 404) {
                        $window.DevExpress.ui.notify('Not found', 'warning', 4000);
                        $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res == 503) {
                        $window.DevExpress.ui.notify('Not connect to appnexus server, please try again later', 'warning', 4000);
                        $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res !== 'Unactive') {
                        b.addClass('active-white');
                      }

                      return res;
                    })
                    .catch(function (err) {
                      return err;
                    });
                }
              });

              if (options.data.ad_type == 'videoAds') {
                videoAds.addClass('state-black' + options.data.id).addClass('active-white').appendTo(container);
              } else {
                videoAds.addClass('state-black' + options.data.id).appendTo(container);
              }
            }
          },
          {
            caption: LC('ADMIN.ADVERTISER-LIST.DATA_SOURCE'),
            width: 204,
            columnIndex: 16,
            allowEditing: false,
            dataField: 'grid_data_source',
            alignment: 'left',
            cellTemplate: function (container, options) {
              var report = $window.$('<div />').dxButton({
                text: 'Report',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  var w = $window.$('div.state-whiteDS' + options.data.id);
                  var b = $window.$('div.state-blackDS' + options.data.id);
                  w.dxButton('instance').option('disabled', true);
                  b.dxButton('instance').option('disabled', true);
                  w.removeClass('active-white');
                  b.removeClass('active-white');
                  AdminService.editAdvertiserDataSource(options.data.id, 'report')
                    .then(function (res) {
                      w.dxButton('instance').option('disabled', false);
                      b.dxButton('instance').option('disabled', false);
                      if (res == 404) {
                        $window.DevExpress.ui.notify('Not found', 'warning', 4000);
                        $('#gridContainerWhite').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res == 503) {
                        $window.DevExpress.ui.notify('Not connect to appnexus server, please try again later', 'warning', 4000);
                        $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res !== 'Unactive') {
                        w.addClass('active-white');
                      }

                      return res;
                    })
                    .catch(function (err) {
                      return err;
                    });
                }
              });

              if (options.data.grid_data_source == 'report') {
                report.addClass('state-whiteDS' + options.data.id).addClass('active-white').appendTo(container);
              } else {
                report.addClass('state-whiteDS' + options.data.id).appendTo(container);
              }

              var tracker = $window.$('<div />').dxButton({
                text: 'Tracker',
                height: 30,
                width: 89,
                disabled: false,
                onClick: function (e) {
                  var w = $window.$('div.state-whiteDS' + options.data.id);
                  var b = $window.$('div.state-blackDS' + options.data.id);
                  w.dxButton('instance').option('disabled', true);
                  b.dxButton('instance').option('disabled', true);
                  w.removeClass('active-white');
                  b.removeClass('active-white');
                  AdminService.editAdvertiserDataSource(options.data.id, 'tracker')
                    .then(function (res) {
                      w.dxButton('instance').option('disabled', false);
                      b.dxButton('instance').option('disabled', false);
                      if (res == 404) {
                        $window.DevExpress.ui.notify('Not found', 'warning', 4000);
                        $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res == 503) {
                        $window.DevExpress.ui.notify('Not connect to appnexus server, please try again later', 'warning', 4000);
                        $window.$('#gridContainer2').dxDataGrid('instance').refresh();
                        return res;
                      }

                      if (res !== 'Unactive') {
                        b.addClass('active-white');
                      }

                      return res;
                    })
                    .catch(function (err) {
                      return err;
                    });
                }
              });

              if (options.data.grid_data_source == 'tracker') {
                tracker.addClass('state-blackDS' + options.data.id).addClass('active-white').appendTo(container);
              } else {
                tracker.addClass('state-blackDS' + options.data.id).appendTo(container);
              }
            }
          }
        ]
      }
    };
  }
})();
