angular
    .module('myApp')
    .controller('EditControllerDefault', EditControllerDefault);


function EditControllerDefault($state, $stateParams, $scope, $rootScope, djangoService) {
    var resource = $stateParams.resource;
    var tid = $stateParams.id;

    $scope.fields = [];
    $scope.item = {};

    $scope.loadItem = function () {
        djangoService.get({id: tid}, function (response) {
            $scope.item = response.result;
            $scope.fields = response.fields;
        })
    };

    $scope.loadItem();

    $scope.update = function () {
        $scope.updatedItem = new djangoService($scope.item);
        $scope.updatedItem.$update(function (data) {
            $state.go('resource.edit', {resource: resource, id: tid});
        });

    };

    $scope.updateAndClose = function () {
        $scope.updatedItem = new djangoService($scope.item);
        $scope.updatedItem.$update(function (data) {
            $scope.close();
        });

    };

    $scope.updateAndDelete = function () {
        $scope.item.active_end_date = new Date();
        $scope.updatedItem = new djangoService($scope.item);
        $scope.updatedItem.$update(function (data) {
            $scope.close();
        });

    };

    $scope.close = function () {
        $state.go('resource.list', {resource: resource});
    };

    $scope.setNow = function (field) {
        $scope.item[field] = new Date();
    };

    $scope.resetNow = function (field) {
        $scope.item[field] = null;
    };

}