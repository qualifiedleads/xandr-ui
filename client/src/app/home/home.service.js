(function () {
  'use strict';

  angular
  .module('pjtLayout')
  .service('Home', Home);

  /** @ngInject */
  function Home($http) {
    var _this = this;

    _this.AdverInfo = {};

    function add(advObject) {
      _this.AdverInfo = {
        'advertiser_id': advObject.advertiser_id || '',
        'advertiser_name': advObject.advertiser_name || '',
        'advertiser_ad_type': advObject.advertiser_ad_type || '',
        'campaign': advObject.campaign || '',
        'id': advObject.id || '',
        'line_item': advObject.line_item || '',
        'line_item_id': advObject.line_item_id || '',
      };
    }

    function get() {
      return _this.AdverInfo;
    }

    _this.add = add;
    _this.get = get;
  }
})();
