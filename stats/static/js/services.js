function User($resource) {
    return $resource('/carave/users/:id/', {id: '@id'}, {
        'list': {method: 'GET'},
        'update': {method: 'PUT'},
    });
}


angular
    .module('inspinia')
    .factory('User', User)
