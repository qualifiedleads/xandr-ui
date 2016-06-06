angular
    .module('myApp')
    .controller('ListControllerDefault', ListControllerDefault);

function ListControllerDefault($state, $stateParams, $scope, $rootScope, $http, $filter, djangoService) {

    // Scope variables
    $scope.tableData = [];
    $scope.listLoaded = false;
    $scope.resource = $stateParams.resource;
    $scope.fields = [];
    $scope.statusList = [];
    $scope.maxRanges = [10, 20, 50, 100];

    $scope.listOptions = {
        searchField: $state.params.searchField || '',
        q: $state.params.q || '',
        sort: $state.params.sort || "",
        order: $state.params.order || "asc",
        total: 0,
        limit: parseInt($state.params.limit) || 10,
        offset: parseInt($state.params.offset) || 0,
        currentPage: 0,
        label: $state.params.label,
        filter: $state.params.filter
    };

    $scope.loadList = function () {
        djangoService.query($state.params, function (data) {
            $scope.list = data.result;
            $scope.fields = data.fields;
            $scope.filters = data.filters;
            $scope.listOptions.total = data.total;
            $scope.listOptions.currentPage = Math.ceil($scope.listOptions.offset / $scope.listOptions.limit) + 1;
            $scope.listLoaded = true;
        });
    };

    $scope.loadList();

    $scope.changeOptionAndRefresh = function (field, value) {
        $scope.listOptions[field] = value;
        $scope.refreshList(); // Update When changed.
    };


    $scope.refreshList = function () {
        var options = angular.copy($scope.listOptions);

        console.log(options);

        delete options.total;
        delete options.currentPage;

        $state.go("resource.list", options, {reload: true});
    };

    $scope.changeLimit = function (limit) {
        // Return to page 1
        $scope.listOptions.offset = 0;
        $scope.changeOptionAndRefresh("limit", limit);
    };

    $scope.selectPage = function (page) {
        $scope.changeOptionAndRefresh("offset", $scope.listOptions.limit * (page - 1));
    };

    $scope.pageChanged = function () {
        $scope.selectPage($scope.listOptions.currentPage);
    };

    $scope.itemClass = function (item) {
        var result = [];
        if (angular.isDefined(item.activeStartDate) && angular.isDefined(item.activeEndDate)) {
            var now = new Date();

            var startDate = new Date(item.activeStartDate);
            var endDate = null;
            if (item.activeEndDate !== null)
                endDate = new Date(item.activeEndDate);
            if (startDate <= now) {
                if (endDate === null) {
                    result.push("rowActive");
                }
                else {
                    if (endDate >= now) {
                        result.push("rowActive");
                    }
                    else {
                        result.push("rowInactive");
                    }
                }
            }
            else {
                result.push("rowInactive");
            }
        }

        return result;
    };

}