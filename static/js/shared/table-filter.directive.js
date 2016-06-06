angular
    .module('myApp')
    .directive('tableFilter', tableFilter)

function tableFilter() {

    return {
        restrict: 'AE',
        templateUrl: "js/shared/table-filter.directive.html"
    };
}

