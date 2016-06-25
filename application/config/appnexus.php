<?php
defined('BASEPATH') OR exit('No direct script access allowed');
/*
+-------------------------------------------------------------
| Appnexus API user credentials.
+-------------------------------------------------------------
*/
$config['apnx_url'] = "http://api.appnexus.com/";
$config['apnx_user'] = "stats_api";
$config['apnx_pass'] = "Stats?3nt3r!";
$config['apnx_token_time'] = 7200; // 2 hrs to expire.
$config['apnx_token_file'] = FCPATH.'temp/api_key.log';
$config['apnx_token_expire_file'] = FCPATH.'temp/api_time.log';
$config['apnx_token_expire_allowance'] = 300; // Renew 5 min. before expiry.
$config['apnx_error_file'] = FCPATH.'temp/api_errors.log';
$config['apnx_log_folder'] = FCPATH.'temp/';
$config['apnx_datetime'] = "Y-m-d";