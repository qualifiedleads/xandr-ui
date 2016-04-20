<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Front extends CI_Controller {
    public function __construct() {
        parent::__construct();
        $this->load->library("auth");
        $this->auth->limit();
    }
    public function index() {
        // Side menu
        $user_privileges = explode(',', $_SESSION['userdata']['privileges']);
        if(in_array("view_campaign_stats",$user_privileges)){
            $data["side_menu"] = $this->load->view("side_bar/v_side_menu_campaign_stats", "", true);
        }
        
        $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_right_menu", "", true);
        $data["content_title"] = 'Dashboard <small>Dashboard</small>';
        $data["content"] = $this->load->view("test/sample_panel1", "", true);
        $data['sess_expiration'] = $this->config->item('sess_expiration');
        $this->load->view("v_front", $data);
    }
}