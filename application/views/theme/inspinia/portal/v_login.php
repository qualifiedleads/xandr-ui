<div id="signin"></div>
            <div id="forgot"></div>
            <div class="signin-box animated fadeIn">
                <h3>Welcome to rtb.cat</h3>
                <p>Sign-in</p>
                <form id="signin_form" class="m-t form-custom" role="form" novalidate="true">
                    <input type="hidden" name="task" value="signin">
                    <div class="form-group">
                        <input type="text" name="username" class="form-control" placeholder="Username"  data-paminta="text" />
                    </div>
                    <div class="form-group">
                        <input type="password" name="password" class="form-control" placeholder="Password"  data-paminta="password" />
                    </div>
                    <div class="form-group">
                        <div class="checkbox i-checks">
                            <label>
                                <input type="checkbox" name="remember" value="1" /><i></i> Remember me 
                            </label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary block full-width m-b submit">
                        <span class="fa fa-spinner rotating"></span> Login
                    </button>
                    <a href="#forgot"><small>Forgot password?</small></a>
                </form>
            </div>
            <div class="forgot-box hidden animated fadeIn">
                <h3>Reset your password</h3>
                <p>A link will be sent to your email.</p>
                <form id="reset_form" class="m-t form-custom" role="form" action="users" novalidate="true">
                    <input type="hidden" name="task" value="reset_pw">
                    <div class="form-group">
                        <input type="email" name="email" class="form-control" placeholder="Email"  data-paminta="email" />
                    </div>
                    <button type="submit" class="btn btn-primary block full-width m-b submit">
                        <span class="fa fa-spinner rotating"></span> Send
                    </button>
                    <a href="#signin"><small>Back to login.</small></a>
                </form>
            </div>
<!-- iCheck -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/iCheck/icheck.min.js');?>"></script>
<script>
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
</script>
<!-- Submit Script with Paminta Validator -->
<script src="<?php echo base_url('js/plugins/paminta/paminta.js');?>"></script>
<script>
    $('#signin_form').paminta(function(e, o){
        e.preventDefault();
        var data = $(o).serialize();

        // Disable form fields.
        $(o).find("input").prop("disabled", true);
        $(o).find("select").prop("disabled", true);
        $(o).find("button").prop("disabled", true);

        // Send AJAX login request.
        $.ajax({
            url: "<?php echo base_url('users');?>",
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
                    }
                    else if(response.status == "ok") {
                        toastr.options.positionClass = "toast-top-center";
                        toastr.success("Redirecting...", "Success");
                        top.location = "<?php echo base_url();?>";
                    }
                    // Disable form fields.
                    $(o).find("input").prop("disabled", false);
                    $(o).find("select").prop("disabled", false);
                    $(o).find("button").prop("disabled", false);
                }, 1000);
            }
        });
    });

    $('#reset_form').paminta(function(e, o){
        e.preventDefault();
        var data = $(o).serialize();

        // Disable form fields.
        $(o).find("input").prop("disabled", true);
        $(o).find("select").prop("disabled", true);
        $(o).find("button").prop("disabled", true);

        // Send AJAX login request.
        $.ajax({
            url: "<?php echo base_url('users');?>",
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
                    }
                    else if(response.status == "ok") {
                        toastr.options.positionClass = "toast-top-center";
                        toastr.success(response.message, "Success");
                    }
                    // Disable form fields.
                    $(o).find("input").prop("disabled", false);
                    $(o).find("select").prop("disabled", false);
                    $(o).find("button").prop("disabled", false);
                }, 1000);
            }
        });
    });
</script>
