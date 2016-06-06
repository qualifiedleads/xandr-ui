angular
    .module('myApp')
    .controller('CreateControllerDefault', CreateControllerDefault);


function CreateControllerDefault($state, $stateParams, $scope, $rootScope, djangoService) {
    var resource = $stateParams.resource;
    $scope.formData = new djangoService();
    $scope.fields = [];

    $scope.loadFields = function(){
        djangoService.query(function (result) {
            $scope.fields = result.fields;
        });
    };

    $scope.loadFields();

    $scope.create = function () {
        $scope.doSave();
        $state.go('resource.create', {resource: resource});
    };

    $scope.createAndClose = function () {
        $scope.doSave();
        $scope.close();
    };

    $scope.createAndNew = function () {
        $scope.doSave();
        $state.go('resource.create', {resource: resource});
    };

    $scope.close = function () {
        $state.go('resource.list', {resource: resource});
    };

    $scope.doSave = function () {
        $scope.formData.$save(function (data) {
            console.log(data);
        });
    };

    $scope.setNow = function (field) {
        $scope.formData[field] = new Date();
    };

    $scope.resetNow = function (field) {
        $scope.formData[field] = null;
    };

}