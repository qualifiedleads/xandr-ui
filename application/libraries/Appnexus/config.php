<?php
/*
+-------------------------------------------------------------
| Appnexus API Configuration File
+-------------------------------------------------------------
*/
@include "creds.php";

// Base endpoint (trailing slash included).
$config['api_base'] = "http://api.appnexus.com/";

// Token expiration time in seconds.
$config['token_expiry'] = 7200; # 2 hrs default.

// Token refresh interval in seconds.
$config['token_refresh'] = 6600; # 1.83 hrs.

// Date format to use.
$config['date_format'] = "Y-m-d H-i-s T";

// Number of login attempts to failure.
$config['max_login_retry'] = 3;

// Error logging option.
$config['enable_error_logs'] = true;

/* Do not add or edit anything below this line.
+------------------------------------------------------------
*/
$this->config = $config;