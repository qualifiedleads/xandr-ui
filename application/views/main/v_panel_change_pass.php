<div class="row">
    <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
            <div class="x_title">
                <h2>Change Password.</h2>
                <div class="clearfix"></div>
            </div>
            <div class="clearfix"></div>
            <div class="x_content">

                <br />
                <form id="account_settings_form" method="post" class="form-horizontal form-label-left">
                    <input type="hidden" name="task" value="update_password" />
                    <input type="hidden" name="username" value="<?php echo $_SESSION['userdata']['username'];?>" />
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Old Password <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="password" name="opassword" class="form-control col-md-7 col-xs-12" data-paminta="password">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            New Password <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="password" name="npassword" class="form-control col-md-7 col-xs-12" placeholder="Type 6 characters or more." data-paminta="password">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-sm-3 col-xs-12">
                            Confirm <span class="required">*</span>
                        </label>
                        <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="password" name="rpassword" class="form-control col-md-7 col-xs-12" placeholder="Retype new password." data-paminta="password">
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
                        </div>
                    </div>
                </form>
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
</script>