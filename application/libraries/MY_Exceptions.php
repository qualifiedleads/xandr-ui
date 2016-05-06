<?php
class MY_Exceptions extends CI_Exceptions {

public function __construct(){
    parent::__construct();
}

function show_404($page = ''){ // error page logic

    header("HTTP/1.1 404 Not Found");
    $CI =& get_instance();
    $data['short_title'] = "404";
    $data['content'] = '<h3>Page Not Found</h3><p>Sorry, but the page you are looking for was not found.</p>';
    $data['short_footnote'] = '';
    $CI->load->view("theme/inspinia/v_portal_layout", $data);
}