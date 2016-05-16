<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Users extends CI_Controller
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
            $v_main_layout['action_area'] = $this->load->view("theme/inspinia/page_heading/v_action_buttons", ["user_privileges"=>$user_privileges], true);
            
            // Contents
            $v_main_layout['contents'] = "";

            if (in_array("users_view",$user_privileges) || in_array("all",$user_privileges))
            {
                $users_table['users'] = $this->m_users->getAll();
                $v_main_layout['contents'] .= $this->load->view("theme/inspinia/content/v_table_users", $users_table, true);
                $users_modal['roles'] = $this->m_users->getRoles();
                $users_modal['user_privileges'] = $user_privileges;
                $v_main_layout['contents'] .= $this->load->view("theme/inspinia/content/v_modal_user_new", $users_modal, true);
                $v_main_layout['contents'] .= $this->load->view("theme/inspinia/content/v_modal_user_edit", $users_modal, true);
                $v_main_layout['contents'] .= $this->load->view("theme/inspinia/content/v_modal_user_view", $users_modal, true);
            }

            $v_main_layout['extras']  = "";
            $v_main_layout['extras'] .= $this->load->view("theme/inspinia/content/v_modal_confirm", "", true);

            $this->load->view("theme/inspinia/v_main_layout", $v_main_layout);
        }
    }

}