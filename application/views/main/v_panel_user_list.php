<div class="row">
    <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
            <div class="x_title">
                <h2>List</h2>
                <div class="clearfix"></div>
            </div>
            <div class="clearfix"></div>
            <div class="x_content">
                <table id="users_list" class="table table-striped projects">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Username</th>
                            <th>Type</th>
                            <th>Email</th>
                            <th>Company</th>
                            <th>Status</th>
                            <th style="width: 110px">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php if(count($users) > 1): ?>
                            <?php foreach($users as $user): ?>
                        <tr>
                            <td><?php echo $user['name'];?></td>
                            <td><?php echo $user['username'];?></td>
                            <td><?php echo ucfirst($user['type']);?></td>
                            <td><?php echo $user['email'];?></td>
                            <td><?php echo $user['company'];?></td>
                            <td>
                                <?php if($user['status']=="active"): ?>
                                <button type="button" class="btn btn-success btn-xs"><?php echo ucfirst($user['status']);?></button>
                                <?php else: ?>
                                <button type="button" class="btn btn-warning btn-xs"><?php echo ucfirst($user['status']);?></button>
                                <?php endif;?>
                            </td>
                            <td>
                                <?php if($_SESSION['userdata']['role_id'] > 1): ?>
                                    <?php if($user['role_id'] > 1): ?>
                                        <?php if($_SESSION['userdata']['user_id'] != $user['id']): ?>
                                <a href="javascript:void(0)" title="View" data-id="<?php echo $user['id'];?>" class="btn btn-primary btn-xs view"><i class="fa fa-folder"></i></a>
                                <a href="users/edit/<?php echo $user['id'];?>" title="Edit" data-id="<?php echo $user['id'];?>" class="btn btn-info btn-xs edit"><i class="fa fa-pencil"></i></a>
                                            <?php if($_SESSION['userdata']['user_id'] != $user['id']): ?>
                                <a href="javascript:void(0)" title="Delete" data-id="<?php echo $user['id'];?>" data-toggle="modal" data-target="#confirm_modal" class="btn btn-danger btn-xs delete"><i class="fa fa-trash-o"></i></a>
                                            <?php endif;?>
                                        <?php else: ?>
                                <a href="javascript:void(0)" title="View" data-id="<?php echo $user['id'];?>" class="btn btn-primary btn-xs view"><i class="fa fa-folder"></i></a>
                                <a href="users/edit/<?php echo $user['id'];?>" title="Edit" data-id="<?php echo $user['id'];?>" class="btn btn-info btn-xs edit"><i class="fa fa-pencil"></i></a>
                                        <?php endif;?>
                                    <?php else: ?>
                                <a href="javascript:void(0)" title="View" data-id="<?php echo $user['id'];?>" class="btn btn-primary btn-xs view"><i class="fa fa-folder"></i></a>
                                    <?php endif;?>
                                <?php else: ?>
                                <a href="javascript:void(0)" title="View" data-id="<?php echo $user['id'];?>" class="btn btn-primary btn-xs view"><i class="fa fa-folder"></i></a>
                                <a href="users/edit/<?php echo $user['id'];?>" title="Edit" data-id="<?php echo $user['id'];?>" class="btn btn-info btn-xs edit"><i class="fa fa-pencil"></i></a>
                                    <?php if($_SESSION['userdata']['user_id'] != $user['id']): ?>
                                <a href="javascript:void(0)" title="Delete" data-id="<?php echo $user['id'];?>" data-toggle="modal" data-target="#confirm_modal" class="btn btn-danger btn-xs delete"><i class="fa fa-trash-o"></i></a>
                                    <?php endif;?>
                                <?php endif;?>
                            </td>
                        </tr>
                            <?php endforeach;?>
                        <?php endif;?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
<!-- Confirm Modal -->
<div id="confirm_modal" class="modal fade" role="dialog">
    <div class="modal-dialog modal-sm">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">Confirm</h4>
            </div>
            <div class="modal-body">
                <p>Do you want to delete an entry?</p>
            </div>
            <div class="modal-footer">
                <a class="btn btn-success" id="modal_action_yes" data-id="">Yes</a>
                <a class="btn btn-warning" data-dismiss="modal">No</a>
            </div>
        </div>
    </div>
</div>
<script>
var pw_change = function(){
    var npassword = $('#account_settings_form input[name="npassword"]');
    var rpassword = $('#account_settings_form input[name="rpassword"]');
    var msg_tmp = $('#account_settings_form .message_template');
    var msg_box = $('#account_settings_form .message_box');

    if(npassword.val() != rpassword.val()) {
        var msg_htm = msg_tmp.find(".alert-danger").clone(true);
        msg_box.html(msg_htm).find('.message').html('<b>Error:</b> New password did not match.');
    }
    else{
        msg_box.html("");
        var formdata = $("#account_settings_form").serialize();
        $('#account_settings_form input').attr('disabled','true');
        $('#account_settings_form button').attr('disabled','true');
        $.ajax({
            "type" : "POST",
            "url" : "dashboard/settings",
            "data" : formdata,
            "success" : function(response){
                setTimeout(function(){
                    $('#account_settings_form input').removeAttr('disabled');
                    $('#account_settings_form button').removeAttr('disabled');
                    
                    if(response.status == "ok"){
                        var msg_htm = msg_tmp.find(".alert-success").clone(true);
                        msg_box.html(msg_htm).find('.message').html('<b>Success:</b> '+response.message);
                    }
                    else{
                        var msg_htm = msg_tmp.find(".alert-danger").clone(true);
                        msg_box.html(msg_htm).find('.message').html('<b>Error:</b> '+response.message);
                    }
                },1000);
            }
        });
    }
    return false;
}
$("#account_settings_form").paminta(pw_change);
var users = {
    "view" : function(){

    },
    "edit" : function(){
        console.log("Edit");
    },
    "delete" : function(){

    }
}
// Initialize event handlers.
$("#users_list a.delete").click(function(){
    var id = $(this).attr('data-id');
    $("#modal_action_yes").attr("href","users/delete/"+id);
})
</script>