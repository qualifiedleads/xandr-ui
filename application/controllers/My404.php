<?php
defined('BASEPATH') OR exit('No direct script access allowed');
/**
* 
*/
class My404 extends CI_Controller
{
    
    public function __construct()
    {
        parent::__construct();
    }

    public function index()
    {
        $data['short_title'] = "404";
        $data['content'] = '<h3>Page Not Found</h3><p>Sorry, but the page you are looking for was not found.</p>';
        $data['short_footnote'] = '';
        $this->load->view("theme/inspinia/v_portal_layout", $data);
    }
}