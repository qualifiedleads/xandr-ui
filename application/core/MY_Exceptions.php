<?php
defined('BASEPATH') OR exit('No direct script access allowed');

/**
* 
*/
class MY_Exceptions extends CI_Exceptions
{
    public function __construct()
    {
        parent::__construct();
    }

    public function show_404($page = '', $log_error = TRUE)
    {
        $CI =& get_instance();

        $data['short_title'] = "404";
        $data['content'] = '<h3>Page Not Found</h3><p>Sorry, but the page you are looking for was not found.</p>';
        $data['short_footnote'] = '';
        echo $CI->load->view("theme/inspinia/v_portal_layout", $data, true);
    }
}