<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Dashboard extends CI_Controller {
    public function __construct(){
        parent::__construct();
        $this->load->library("auth");
        $this->auth->limit();
    }
    public function _remap($uri) {
        if($uri == "settings") {
            $this->settings();
        }
        else {
            $this->index();
        }
    }
    private function index() {

        // Global
        $data["page_title"] = "RTB.cat - Dashboard";

        // Side menu
        $data["side_menu"] = "";
        $user_privileges = explode(',', $_SESSION['userdata']['privileges']);
        if(in_array("view_campaign_stats",$user_privileges)){
            $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_campaign_stats", "", true);
        }
        if(in_array("view_users",$user_privileges) || in_array("all",$user_privileges)){
            $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_users", "", true);
        }
        
        $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);
        $data["content_title"] = 'Dashboard';
        $data["content"] = $this->load->view("test/sample_panel1", "", true);
        $data['sess_expiration'] = $this->config->item('sess_expiration');
        $this->load->view("v_dashboard", $data);
    }
    private function settings() {
        if($this->input->post("task") == "update_password"){
            $username = $this->input->post("username");
            $opassword = $this->auth->hash($this->input->post("opassword"), $username);
            $npassword = $this->input->post("npassword");
            $rpassword = $this->input->post("rpassword");
            if($npassword != $rpassword){
                $response = array(
                    "status" => "error",
                    "message" => "Password did not match."
                );
                header("Content-Type: application/json");
                echo json_encode($response);
            }
            else{
                $get_sql = "SELECT * FROM `users` WHERE `username`='{$username}' AND `password`='{$opassword}'";
                $get_query = $this->db->query($get_sql);
                if($get_query->num_rows() == 1){
                    $userdata = $get_query->result_array();
                    $user_id = $userdata[0]['id'];
                    $new_password = $this->auth->hash($npassword, $username);
                    $set_sql = "UPDATE `users` SET `password`='{$new_password}' WHERE `id`='{$user_id}'";
                    $this->db->query($set_sql);
                    $response = array(
                        "status" => "ok",
                        "message" => "New password saved."
                    );
                    header("Content-Type: application/json");
                    echo json_encode($response);
                }
                else{
                    $response = array(
                        "status" => "error",
                        "message" => "Old password is wrong."
                    );
                    header("Content-Type: application/json");
                    echo json_encode($response);
                }
            }
        }
        else{
            // Privileges
            $user_privileges = explode(',', $_SESSION['userdata']['privileges']);

            // Global
            $data["page_title"] = "RTB.cat - Dashboard";

            // Side menu
            $data["side_menu"] = "";
            if(in_array("view_campaign_stats",$user_privileges)){
                $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_campaign_stats", "", true);
            }
            if(in_array("view_users",$user_privileges) || in_array("all",$user_privileges)){
                $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_users", "", true);
            }

            // Topbar right.
            $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);

            // Content
            $data["content_title"] = 'Account <small>Settings</small>';
            $data["content"] = $this->load->view("main/v_panel_change_pass", "", true);

            // Template
            $data['sess_expiration'] = $this->config->item('sess_expiration');
            $this->load->view("v_dashboard", $data);
        }
    }
}