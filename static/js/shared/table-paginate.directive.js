angular
    .module('myApp')
    .directive('tablePaginate', tablePaginate)

function tablePaginate() {

    return {
        restrict: 'AE',
        templateUrl: "js/shared/table-paginate.directive.html"
    };
}

