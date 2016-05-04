<?php
defined('BASEPATH') OR exit('No direct script access allowed');

/**
* 
*/
class Dashboard extends CI_Controller
{
    
    public function __construct()
    {
        parent::__construct();
        $this->load->library("auth");
        $this->auth->limit(base_url("portal"));
    }

    public function index()
    {
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        // Navbar Side Contents
        $v_main_layout['nav_header'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_header", ["user_privileges"=>$user_privileges], true);
        $v_main_layout['nav_menus'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_menus", ["user_privileges"=>$user_privileges], true);

        // Navbar Top Contents
        $v_main_layout['nav_logout_button'] = $this->load->view("theme/inspinia/navbar_static_top/v_logout_button", "", true);

        // Page Heading
        $v_page_info['title'] = "Home";
        $v_page_info['breadcrumbs'] = array('Home' => base_url());
        $v_page_info['user_privileges'] = $user_privileges;
        $v_main_layout['page_info'] = $this->load->view("theme/inspinia/page_heading/v_page_info", $v_page_info, true);
        //$v_main_layout['action_area'] = $this->load->view("theme/inspinia/page_heading/v_action_buttons", "", true);

        $this->load->view("theme/inspinia/v_main_layout", $v_main_layout);
    }

    public function login()
    {
        $this->load->view("theme/inspinia/v_portal_layout");
    }
}