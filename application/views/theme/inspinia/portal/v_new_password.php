<div class="signin-box animated fadeIn">
                <h3>New Password</h3>
                <p>Create a new password for your account.</p>
                <form id="newpassword_form" class="m-t form-custom" role="form" novalidate="true">
                    <input type="hidden" name="task" value="update_pw" />
                    <input type="hidden" name="user_id" value="<?php echo @$user_id;?>" />
                    <div class="form-group">
                        <input type="password" name="npassword" class="form-control" placeholder="New password"  data-paminta="password" />
                    </div>
                    <div class="form-group">
                        <input type="password" name="rpassword" class="form-control" placeholder="Retype password"  data-paminta="password" />
                    </div>
                    <button type="submit" class="btn btn-primary block full-width m-b submit">
                        <span class="fa fa-spinner rotating"></span> Save
                    </button>
                </form>
            </div>
<!-- Submit Script with Paminta Validator -->
<script src="<?php echo base_url('js/plugins/paminta/paminta.js');?>"></script>
<script>
    $('#newpassword_form').paminta(function(e, o){
        e.preventDefault();
        var data = $(o).serialize();

        // Disable form fields.
        $(o).find("input").prop("disabled", true);
        $(o).find("select").prop("disabled", true);
        $(o).find("button").prop("disabled", true);

        // Send AJAX login request.
        $.ajax({
            url: "<?php echo base_url('users/reset/');?>",
            type: "post",
            data: data,
            error: function(jqXHR) {
                setTimeout(function() {
                    // Show toastr notice.
                    toastr.options.positionClass = "toast-top-center";
                    toastr.error(jqXHR.statusText, "Error "+jqXHR.status);
                    // Disable form fields.
                    $(o).find("input").prop("disabled", false);
                    $(o).find("select").prop("disabled", false);
                    $(o).find("button").prop("disabled", false);
                }, 1000);
            },
            success: function(response) {
                setTimeout(function() {
                    // Show toastr notice.
                    if(response.status == "error") {
                        toastr.options.positionClass = "toast-top-center";
                        toastr.error(response.message, "Error");
                        $(o).find("input").prop("disabled", false);
                        $(o).find("select").prop("disabled", false);
                        $(o).find("button").prop("disabled", false);
                    }
                    else if(response.status == "ok") {
                        toastr.options.positionClass = "toast-top-center";
                        toastr.success("Redirecting...", "Success");
                        setTimeout(function(){top.location = "<?php echo base_url();?>";}, 2000);
                    }
                }, 1000);
            }
        });
        console.log(data);
    });
</script>
