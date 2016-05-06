
<!DOCTYPE html>
<html>

<head>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>INSPINIA | Login</title>

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

    <!-- Essential -->
    <script src="<?php echo base_url('theme/inspinia/js/jquery-2.1.1.js');?>"></script>

</head>

<body class="gray-bg">

    <div class="middle-box text-center loginscreen animated fadeInDown">
        <div>
            <h1><?php echo @$short_title;?></h1>
        </div>
        
        <div id="wrapper">
            <?php echo @$content;?>
            <p class="m-t"> <small><?php echo @$short_footnote;?></small> </p>
        </div>
    </div>

    <!-- Mainly scripts -->
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

</body>

</html>