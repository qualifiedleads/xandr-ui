(function () {
    'use strict';

    angular
        .module('myApp',
            [
                //
                'ngResource',
                'ui.router',

                'ui.bootstrap',
                'ui.bootstrap.tpls',
                'ui.bootstrap.pagination',
                'ui.bootstrap.alert',

                // Bootstrap module
                'mgcrea.ngStrap',

                // Date picker module
                'mgcrea.ngStrap.timepicker',
                'mgcrea.ngStrap.datepicker'
            ]);
})();
