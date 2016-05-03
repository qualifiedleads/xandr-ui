<div class="ibox float-e-margins" ng-app="tableUsers">
                        <div class="ibox-title">
                            <h5>Registered Users</h5>
                        </div>
                        <div class="ibox-content">
                            <div class="table-responsive">
                                <table class="table table-striped table-custom-static" ng-controller="makeTable">
                                    <thead>
                                        <tr>
                                            <th><input type="checkbox" class="i-checks" /></th>
                                            <th>Full Name </th>
                                            <th>Role</th>
                                            <th>Username </th>
                                            <th>Email</th>
                                            <th>Status</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr ng-repeat="user in users">
                                            <td><input type="checkbox" class="i-checks" name="id[]" /></td>
                                            <td>{{ user.name }}</td>
                                            <td>{{ user.role }}</td>
                                            <td>{{ user.username }}</td>
                                            <td>{{ user.email }}</td>
                                            <td><span class="label label-info">{{ user.status }}</span></td>
                                            <td>
                                                <a href="#" class="btn btn-default btn-xs" title="Details"><i class="fa fa-eye"></i></a>
                                                <a href="#" class="btn btn-default btn-xs" title="Edit"><i class="fa fa-pencil"></i></a>
                                                <a href="#" class="btn btn-default btn-xs" title="Delete"><i class="fa fa-trash"></i></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
<script>
    var users_model = {
        list : [{name: "Carl Lycos", role: "detective", username: "carll", email: "carl@lycosmail.net"}]
    }
    var app =  angular.module("tableUsers", []);
    app.controller("makeTable", function($scope, $http){
        /*$http.get("<?php echo base_url('users/json/getall');?>")
        .then(function(response) {
            $scope.users = response.data;
        });*/
        $scope.users = users_model.list;
    });
</script>
