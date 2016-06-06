angular
    .module('myApp')
    .controller('MainController', MainController);

function MainController($state, $scope) {

    $scope.truckOptions = {
        resource: "truck",
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

}