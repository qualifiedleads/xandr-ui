<!DOCTYPE html>
<html>
<head>
 
    <!-- Metadata -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>rtb Stats | Page</title>
 
    <!-- Core CSS Files -->
    <link href="<?php echo base_url('theme/inspinia/css/bootstrap.min.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/font-awesome/css/font-awesome.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/animate.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/style.css');?>" rel="stylesheet" />

    <!-- Plugins -->
    <link href="<?php echo base_url('theme/inspinia/css/plugins/iCheck/custom.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/plugins/toastr/toastr.min.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('css/plugins/paminta/paminta.css');?>" rel="stylesheet" />

    <!-- Custom -->
    <link href="<?php echo base_url('css/inspinia-custom.css');?>" rel="stylesheet" />
 
</head>
<body class="portal-layout">
    <div>
        <?php echo @$center_boxes;?>
    </div>
    <?php echo @$base_element;?>

    <!-- Mainly scripts -->
    <script src="<?php echo base_url('theme/inspinia/js/jquery-2.1.1.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/bootstrap.min.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/metisMenu/jquery.metisMenu.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/slimscroll/jquery.slimscroll.min.js');?>"></script>

    <!-- Custom and plugin javascript -->
    <script src="<?php echo base_url('theme/inspinia/js/inspinia.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/pace/pace.min.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/toastr/toastr.min.js');?>"></script>

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
                url: "users",
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
                        else {
                            // Redirect to base url.
                            var url_last = "";
                            var url_path = top.location.pathname.split('/');
                            url_path.shift();
                            url_last = url_path.pop();
                            if(url_last == "") url_last = url_path.pop();
                            top.location = '//'+top.location.host+'/'+url_path;
                        }
                        // Disable form fields.
                        $(o).find("input").prop("disabled", false);
                        $(o).find("select").prop("disabled", false);
                        $(o).find("button").prop("disabled", false);
                    }, 1000);
                }
            });
        });

        function test() {
            console.log("test");
        }
    </script>

</body>
</html>