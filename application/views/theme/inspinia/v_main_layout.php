<!DOCTYPE html>
<html>
<head>
 
    <!-- Metadata -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>INSPINIA | Page</title>
 
    <!-- Core CSS Files -->
    <link href="<?php echo base_url('theme/inspinia/css/bootstrap.min.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/font-awesome/css/font-awesome.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/animate.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/style.css');?>" rel="stylesheet" />

    <!-- Plugins -->
    <link href="<?php echo base_url('theme/inspinia/css/plugins/iCheck/custom.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('css/plugins/paminta/paminta.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('css/inspinia-custom.css');?>" rel="stylesheet" />

    <!-- Essential -->
    <script src="<?php echo base_url('theme/inspinia/js/jquery-2.1.1.js');?>"></script>
    <script src="<?php echo base_url('js/libs/angular/angular-1.4.8.min.js');?>"></script>
 
</head>
<body>

    <div id="wrapper">

        <nav class="navbar-default navbar-static-side" role="navigation">
            <div class="sidebar-collapse">
                <ul class="nav metismenu" id="side-menu">
                    <?php echo @$nav_header;?>
                    <?php echo @$nav_menus;?>
                </ul>
            </div>
        </nav>

        <div id="page-wrapper" class="gray-bg">
            <div class="row border-bottom">
                <nav class="navbar navbar-static-top" role="navigation" style="margin-bottom: 0">
                    <div class="navbar-header">
                        <a class="navbar-minimalize minimalize-styl-2 btn btn-primary " href="#"><i class="fa fa-bars"></i> </a>
                    </div>
                    <ul class="nav navbar-top-links navbar-right">
                        <?php echo @$nav_welcome_message;?>
                        <?php echo @$nav_dropdown_message;?>
                        <?php echo @$nav_dropdown_alert;?>
                        <?php echo @$nav_logout_button;?>
                    </ul>
                </nav>
            </div>
            <div class="row wrapper border-bottom white-bg page-heading">
                <div class="col-lg-10">
                    <?php echo @$page_info;?>
                </div>
                <div class="col-lg-2">
                    <div class="title-action">
                        <?php echo @$action_area;?>
                    </div>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight">
                <div class="row">
                    <div>
                        <?php echo @$contents;?>
                    </div>
                </div>
            </div>
            <div class="footer">
                <div class="pull-right">
                    Dashboard.
                </div>
                <div>
                    <strong>Copyright</strong> rtb.cat &copy; 2014-2016
                </div>
            </div>
        </div>
    </div>
    <div id="full_loader" class="screen-overlay">
        <div class="cell-wrapper">
            <div class="center-box">
                <div class="sk-spinner sk-spinner-wave">
                    <div class="sk-rect1"></div>
                    <div class="sk-rect2"></div>
                    <div class="sk-rect3"></div>
                    <div class="sk-rect4"></div>
                    <div class="sk-rect5"></div>
                </div>
            </div>
        </div>
    </div>
    <!-- SESSION DATA
    <?php
        print_r($_SESSION);
    ?>
    -->

    <!-- Mainly scripts -->
    <script src="<?php echo base_url('theme/inspinia/js/bootstrap.min.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/metisMenu/jquery.metisMenu.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/slimscroll/jquery.slimscroll.min.js');?>"></script>

    <!-- Custom and plugin javascript -->
    <script src="<?php echo base_url('theme/inspinia/js/inspinia.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/pace/pace.min.js');?>"></script>

    <!-- iCheck -->
    <script src="<?php echo base_url('theme/inspinia/js/plugins/iCheck/icheck.min.js');?>"></script>
    <script>
        $(document).ready(function () {
            $('.i-checks').iCheck({
                checkboxClass: 'icheckbox_square-green',
                radioClass: 'iradio_square-green',
            });
        });
    </script>

    <!-- Custom -->
    <script src="<?php echo base_url('js/inspinia-custom.js');?>"></script>
    <!-- Paminta Validator -->
    <script src="<?php echo base_url('js/plugins/paminta/paminta.js');?>"></script>
    <script>
        $(document).ready(function () {
            $('.i-checks').iCheck({
                checkboxClass: 'icheckbox_square-green',
                radioClass: 'iradio_square-green',
            });
        });
    </script>

</body>
</html>
