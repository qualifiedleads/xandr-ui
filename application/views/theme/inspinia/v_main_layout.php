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

    <!-- Plugins CSS -->
    <link href="<?php echo base_url('theme/inspinia/css/plugins/awesome-bootstrap-checkbox/awesome-bootstrap-checkbox.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/plugins/iCheck/custom.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('theme/inspinia/css/plugins/toastr/toastr.min.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('css/plugins/paminta/paminta.css');?>" rel="stylesheet" />
    <link href="<?php echo base_url('css/inspinia-custom.css');?>" rel="stylesheet" />

    <!-- Extras CSS - Page limted CSS -->
    <?php echo @$header_css;?>

    <!-- Essential -->
    <script src="<?php echo base_url('theme/inspinia/js/jquery-2.1.1.js');?>"></script>
 
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
                <?php echo @$contents;?>
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

    <!-- Essentials - Side wide element or functions. -->
    <!-- Essentials[Modal] -->
    <div class="modal fade inmodal" id="change_pass_modal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="static">
        <div class="modal-dialog modal-sm">
            <form id="change_pass_form" class="form-custom" method="post">
                <input type="hidden" name="task" value="change_my_pw" />
                <input type="hidden" name="user_id" value="<?php echo @$_SESSION['userdata']['user_id'];?>" />
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">Change Password</h4>
                    </div>
                    <div class="modal-body">
                        <table class="modal-table" align="center">
                            <tbody>
                                <tr>
                                    <td><input type="password" name="opassword" class="form-control" data-paminta="password" placeholder="Old Password" /></td>
                                </tr>
                                <tr>
                                    <td><input type="password" name="npassword" class="form-control" data-paminta="password" placeholder="New Password" /></td>
                                </tr>
                                <tr>
                                    <td><input type="password" name="rpassword" class="form-control" data-paminta="password" placeholder="Retype Password" /></td>
                                </tr>
                            </tbody>
                        </table>
                        
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary submit"><span class="fa fa-spinner rotating"></span> Change</button>
                        <button type="button" class="btn btn-white" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    <script>
        $(document).ready(function(){
            $("#change_pass_form").paminta(users.updateMyPass);
        })
    </script>
    <!-- End Essentials -->

    <!-- Extras - Page limited element or functions. Pass it on $extras variable from the calling controller. -->
    <?php echo @$extras;?>
    <!-- End Extras -->

    <!-- SESSION DATA - Temporary reference only for checking what's in the current session.
    <?php
        print_r($_SESSION);
    ?>
    -->

    <!-- Mainly scripts -->
    <script src="<?php echo base_url('theme/inspinia/js/bootstrap.min.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/metisMenu/jquery.metisMenu.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/slimscroll/jquery.slimscroll.min.js');?>"></script>

    <!-- Custom and plugin javascript -->
    <script src="<?php echo base_url('theme/inspinia/js/plugins/toastr/toastr.min.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/inspinia.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/pace/pace.min.js');?>"></script>
    <script src="<?php echo base_url('js/plugins/paminta/paminta.js');?>"></script>

    <!-- Custom -->
    <script src="<?php echo base_url('js/inspinia-custom.js');?>"></script>
    
</body>
</html>
