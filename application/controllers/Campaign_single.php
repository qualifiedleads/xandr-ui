<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Campaign_single extends CI_Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->load->config("custom");
        $this->load->model("m_users");
        $this->load->library("auth");
    }
    public function index()
    {
        $task = $this->input->post("task");

        if ($task)
        {

        }
        else
        {
            $this->auth->limit();
            $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

            // Navbar Side Contents
            $v_main_layout['nav_header'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_header", "", true);
            $v_main_layout['nav_menus'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_menus", ["user_privileges"=>$user_privileges], true);

            // Navbar Top Contents
            $v_main_layout['nav_logout_button'] = $this->load->view("theme/inspinia/navbar_static_top/v_logout_button", "", true);

            // Page Heading
            $v_page_info['title'] = "Campaign Tree";
            $v_page_info['breadcrumbs'] = array('Home' => base_url(),'Campaign Tree'=>'javascript:void(0)');
            $v_main_layout['page_info'] = $this->load->view("theme/inspinia/page_heading/v_page_info", $v_page_info, true);

            // Contents
            $v_main_layout['contents'] = "";

            if (in_array("users_view",$user_privileges) || in_array("all",$user_privileges))
            {
                $v_main_layout['contents'] .= $this->load->view("jaiho/campaigns_single", '', true);
  
            }
            $this->load->view("jaiho/campaigns_main", $v_main_layout);
        }
    }

}