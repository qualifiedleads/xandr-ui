<!DOCTYPE html>
<html lang="en">

<head>
    <base href="<?php echo base_url();?>" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title><?php echo @$page_title;?></title>

    <!-- Bootstrap core CSS -->

    <link href="css/bootstrap.min.css" rel="stylesheet">

    <link href="fonts/css/font-awesome.min.css" rel="stylesheet">
    <link href="css/animate.min.css" rel="stylesheet">
    <link href="css/shake.min.css" rel="stylesheet">

    <!-- Custom styling plus plugins -->
    <link href="css/custom.css" rel="stylesheet">
    <link href="css/page-login.css" rel="stylesheet">

    <!-- Bootstrap core JS -->
    <script src="js/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>

    <!-- Plugins JS -->
    <script src="js/notify.min.js"></script>

    <!--[if lt IE 9]>
                <script src="../assets/js/ie8-responsive-file-warning.js"></script>
                <![endif]-->

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
                    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
                    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
                <![endif]-->
</head>

<body>
    <div>
        <div id="wrapper">
            <div id="change_pass" class="animate form">
                <section class="login_content">
                    <?php echo @$change_pass_form; ?>
                </section>
            </div>
        </div>
    </div>
    <!-- Login Custom JS -->
    <script src="js/account-login.js"></script>
    <!-- /Login Custom JS -->
<!--
<?php print_r(@$_SESSION);?>

-->
</body>
</html>