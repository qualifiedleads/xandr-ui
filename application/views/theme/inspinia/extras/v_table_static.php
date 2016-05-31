<div class="ibox float-e-margins">
                        <div class="ibox-title">
                            <h5>Registered Users</h5>
                        </div>
                        <div class="ibox-content">
                            <div class="table-responsive">
                                <table class="table table-striped table-custom-static">
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
<?php if (isset($users) && count(@$users) > 0):?>
    <?php foreach ($users as $user):?>
                                        <tr>
                                            <td><input type="checkbox" class="i-checks" name="id[]" /></td>
                                            <td><?php echo $user['name'];?></td>
                                            <td><?php echo $user['type'];?></td>
                                            <td><?php echo $user['username'];?></td>
                                            <td><?php echo $user['email'];?></td>
        <?php if ($user['status'] == "active"):?>
                                            <td><span class="label label-info"><?php echo $user['status'];?></span></td>
        <?php elseif ($user['status'] == "inactive"):?>
                                            <td><span class="label label-warning"><?php echo $user['status'];?></span></td>
        <?php endif;?>
                                            <td>
                                                <a href="#" class="btn btn-default btn-xs" title="Details"><i class="fa fa-eye"></i></a>
                                                <a href="#" class="btn btn-default btn-xs" title="Edit"><i class="fa fa-pencil"></i></a>
                                                <a href="#" class="btn btn-default btn-xs" title="Delete"><i class="fa fa-trash"></i></a>
                                            </td>
                                        </tr>
    <?php endforeach;?>
<?php endif;?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
