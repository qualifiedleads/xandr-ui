/**
 * This module defines the resource mappings required by Angular JS to map to a
 * standard Grails CRUD URL scheme that uses `"/$controller/$action?/$id?"`.
 */
angular
    .module('myApp')
    .factory('djangoService', djangoService);

function djangoService($resource) {
    var domainBaseUrl = "http://localhost:8000";

    return $resource(domainBaseUrl + '/trucks/:id/', {id: '@id'}, {
        'query': {method: 'GET'},
        'update': {method:'PUT'},
    });
}