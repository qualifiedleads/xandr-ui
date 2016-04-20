<div class="row">
    <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
            <div class="x_title">
                <h2>Add New</h2>
                <div class="clearfix"></div>
            </div>
            <div class="clearfix"></div>
            <div class="x_content">

                <br />
                <form id="new_user_form" method="post" class="form-horizontal form-label-left">
                    <input type="hidden" name="task" value="add_user" />
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Full Name <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="name" class="form-control col-md-7 col-xs-12" data-paminta="text">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            User Type
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <select class="form-control" name="role_id">
                                <?php foreach($roles as $key=>$value): ?>
                                <option value="<?php echo $key;?>"><?php echo ucfirst($value);?></option>

                                <?php endforeach;?>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Username <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="username" class="form-control col-md-7 col-xs-12" data-paminta="text">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Password <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="password" name="password" class="form-control col-md-7 col-xs-12" data-paminta="password">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Email <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="email" class="form-control col-md-7 col-xs-12" data-paminta="email">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Company
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="company" class="form-control col-md-7 col-xs-12">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            APNX ID
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="apnx_id" class="form-control col-md-7 col-xs-12">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Status
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <label><input type="radio" name="status" value="active" checked="true" /> Active</label><br />
                            <label><input type="radio" name="status" value="inactive" /> Inactive</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-md-3 col-sm-3 col-xs-12"></div>
                        <div class="col-md-6 col-sm-6 col-xs-12 message_box">
                            
                        </div>
                    </div>
                    <div class="message_template" style="display: none">
                        <div class="alert alert-success alert-dismissible fade in animated fadeIn" role="alert">
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">×</span>
                            </button>
                            <span class="message">Message</span>
                        </div>
                        <div class="alert alert-danger alert-dismissible fade in shaking-lr" role="alert">
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">×</span>
                            </button>
                            <span class="message">Message</span>
                        </div>
                    </div>
                    <div class="clearfix"></div>
                    <!--<div class="ln_solid"></div>-->
                    <div class="form-group">
                        <div class="col-md-6 col-sm-6 col-xs-12 col-md-offset-3">
                            <button type="submit" class="btn btn-success"><span class="fa fa-spinner fa-spin"></span>Save</button>
                            <button type="reset" class="btn btn-primary">Clear</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
<script>
var add_user = function(){
    var msg_tmp = $('#new_user_form .message_template');
    var msg_box = $('#new_user_form .message_box');

    msg_box.html("");
    var formdata = $("#new_user_form").serialize();
    $('#new_user_form input').attr('disabled','true');
    $('#new_user_form button').attr('disabled','true');
    $.ajax({
        "type" : "POST",
        "url" : "users/new",
        "data" : formdata,
        "success" : function(response){
            setTimeout(function(){
                $('#new_user_form input').removeAttr('disabled');
                $('#new_user_form button').removeAttr('disabled');
                
                if(response.status == "ok"){
                    var msg_htm = msg_tmp.find(".alert-success").clone(true);
                    msg_box.html(msg_htm).find('.message').html('<b>Success:</b> '+response.message);
                    $('#new_user_form').trigger("reset");
                }
                else{
                    var msg_htm = msg_tmp.find(".alert-danger").clone(true);
                    msg_box.html(msg_htm).find('.message').html('<b>Error:</b> '+response.message);
                }
            },1000);
        }
    });
    return false;
}
$("#new_user_form").paminta(add_user);
</script>