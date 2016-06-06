angular
    .module('myApp')
    .config(config);

function config($urlRouterProvider, $stateProvider, $resourceProvider) {
    $urlRouterProvider.otherwise("/");
    $resourceProvider.defaults.stripTrailingSlashes = false;

    $stateProvider
        .state('index', {
            abstract: true,
            url: "/",
            templateUrl: "js/layout/content.html"
        })

        .state('index.home', {
            url: "",
            templateUrl: "js/layout/home.html",
            controller: MainController
        })

        .state('resource', {
            abstract: true,
            url: "/:resource",
            templateUrl: "js/layout/content.html"
        })

        .state('resource.list', {
            url: "/list?offset&limit&sort&order&q&searchField&filter",
            templateUrl: "js/base/list.html",
            controller: ListControllerDefault
        })

        .state('resource.edit', {
            url: "/edit/:id",
            templateUrl: "js/base/edit.html",
            controller: EditControllerDefault
        })

        .state('resource.create', {
            url: "/create",
            templateUrl: "js/base/create.html",
            controller: CreateControllerDefault
        })
}
