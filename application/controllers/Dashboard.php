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

        // CSS in header preload.
        $v_dashboard_layout['header_css'] = $this->load->view("theme/inspinia/custom/css/v_dashboard_head_css", "", true);

        // Navbar Side Contents
        $v_dashboard_layout['nav_header'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_header", ["user_privileges"=>$user_privileges], true);
        $v_dashboard_layout['nav_menus'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_menus", ["user_privileges"=>$user_privileges], true);

        // Navbar Top Contents
        $v_dashboard_layout['nav_logout_button'] = $this->load->view("theme/inspinia/navbar_static_top/v_logout_button", "", true);

        // Page Heading
        $v_page_info['title'] = "Stats for Advertiser";
        $v_page_info['breadcrumbs'] = array('Home'=>'');
        $v_page_info['user_privileges'] = $user_privileges;
        $v_dashboard_layout['page_info'] = $this->load->view("theme/inspinia/page_heading/v_page_info", $v_page_info, true);
        $v_dashboard_layout['action_area'] = $this->load->view("theme/inspinia/page_heading/v_action_date_range", "", true);

        // Extras
        $v_dashboard_layout['extras'] = $this->load->view("theme/inspinia/custom/js/v_dashboard_body_js_1", "", true);
        $v_dashboard_layout['extras'] .= $this->load->view("theme/inspinia/plugins/js/v_date_range_picker", "", true);
        $v_dashboard_layout['extras'] .= $this->load->view("theme/inspinia/plugins/js/v_flot_chart", "", true);
        $v_dashboard_layout['extras'] .= $this->load->view("theme/inspinia/plugins/js/v_jvectormap", "", true);
        $v_dashboard_layout['extras'] .= $this->load->view("theme/inspinia/custom/js/v_dashboard_body_js_2", "", true);

        // Contents
        //$v_home_layout['contents'] = $this->load->view("theme/inspinia/content/v_dashboard_index", "", true);

        $this->load->view("theme/inspinia/v_dashboard_layout", $v_dashboard_layout);
    }

    public function login()
    {
        $this->load->view("theme/inspinia/v_portal_layout");
    }
}