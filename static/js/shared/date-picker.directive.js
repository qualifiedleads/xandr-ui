angular
    .module('cockpit2')
    .directive('clearDate', clearDate)
    .directive('setToday', setToday);


function clearDate($parse) {
    return {
        restrict: 'EA',
        replace: true,
        require: 'ngModel',
        template: "<a class=\"btn btn-sm\"><span class=\"glyphicon glyphicon-remove\"></span></a>",
        link: function (scope, elem, attrs, ctrl) {
            elem.bind('click', function () {
                ctrl.$setViewValue("");
                ctrl.$render();

                scope.$apply();

                return false;
            });
        }
    };
}

function setToday($parse) {
    return {
        restrict: 'EA',
        replace: true,
        require: 'ngModel',
        template: "<a class=\"btn btn-sm\"><span class=\"glyphicon glyphicon-calendar\"></span></a>",
        link: function (scope, elem, attrs, ctrl) {
            elem.bind('click', function () {
                ctrl.$setViewValue(new Date());
                ctrl.$render();

                scope.$apply();

                return false;
            });
        }
    };
}
