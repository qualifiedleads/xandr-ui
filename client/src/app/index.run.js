(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {

    $log.debug('runBlock end');
  }

})();
