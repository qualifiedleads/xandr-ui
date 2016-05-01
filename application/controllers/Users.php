<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Users extends CI_Controller {
    public function __construct() {
        parent::__construct();
        $this->load->library("auth");
        //$this->auth->limit();
    }
    public function index() {
        $task = $this->input->post("task");
        if ($task) {
            if ($task == "signin") {
                $username = $this->input->post("username");
                $password = $this->input->post("password");
                $remember = $this->input->post("remember");
                if ($username && $password) {
                    if ($remember) {
                        $signin_result = $this->auth->signin($username, $password, $remember);
                    }
                    else {
                        $signin_result = $this->auth->signin($username, $password);
                    }
                    header("Content-Type: application/json");
                    echo json_encode($signin_result);
                }
                else {
                    echo "No user or pass.";
                }
            }
            if ($task == "reset_pw") {
                $email = $this->input->post("email");
                if ($email) {
                    $sql = "SELECT `users`.`id`,`users`.`email`,`users`.`status` FROM `users` WHERE `email`='{$email}'";
                    $query = $this->db->query($sql);
                    if ($query->num_rows() == 1) {
                        $userdata = $query->result_array()[0];
                        if ($userdata['status'] == "active") {
                            $response = array("status"=>"ok","code"=>"active","message"=>"Please check your email.");
                        }
                        elseif ($userdata['status'] == "inactive") {
                            $response = array("status"=>"error","code"=>"inactive","message"=>"Account is inactive.");
                        }
                        if ($response) {
                            header("Content-Type: application/json");
                            echo json_encode($response);
                        }
                    }
                    else {
                        $response = array("status"=>"error","code"=>"not_found","message"=>"Unauthorized access.");
                        header("Content-Type: application/json");
                        echo json_encode($response);
                    }
                }
            }
        }
        else {
            $this->auth->limit();
            // Navbar Side Contents
            $v_main_layout['nav_header'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_header", "", true);
            $v_main_layout['nav_menus'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_menus", "", true);

            // Navbar Top Contents
            $v_main_layout['nav_logout_button'] = $this->load->view("theme/inspinia/navbar_static_top/v_logout_button", "", true);

            // Page Heading
            $v_page_info['title'] = "Users";
            $v_page_info['breadcrumbs'] = array('Home' => base_url());
            $v_main_layout['page_info'] = $this->load->view("theme/inspinia/page_heading/v_page_info", $v_page_info, true);
            $v_main_layout['action_area'] = $this->load->view("theme/inspinia/page_heading/v_action_buttons", "", true);

            $this->load->view("theme/inspinia/v_main_layout", $v_main_layout);
        }
    }
    public function sign_in() {

    }
    public function sign_out() {
        unset($_COOKIE['sid']);
        setcookie('sid', null, -1, '/');
        session_destroy();
        header("Location: ".base_url("portal"));
    }
    private function list_users() {
        // Privileges
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        if (in_array("view_users",$user_privileges) || in_array("all",$user_privileges)){
            
            // Page title
            $data["page_title"] = 'RTB.cat - Users';
            
            // Content Title
            $data["content_title"] = 'Users';

            // Topbar right
            $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);

            // Side menu
            $data["side_menu"] = "";
            $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_users", "", true);
            
            // Content
            $data["content"] = "";
            $get_users_sql = "SELECT `users`.`id`,`users`.`name`,`users`.`username`,`users`.`email`,`users`.`company`,`users`.`status`,`users`.`role_id`,`roles`.`type` FROM `users` INNER JOIN `roles` ON `users`.`role_id`=`roles`.`id`";
            $get_users_query = $this->db->query($get_users_sql);
            $users_data = array('users'=>$get_users_query->result_array());
            $data["content"] .= $this->load->view("main/v_panel_user_list", $users_data, true);

            $data['sess_expiration'] = $this->config->item('sess_expiration');
            $this->load->view("v_dashboard", $data);
        }
        else {
            show_404();
        }
    }
    private function new_user() {
        // Privileges
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        if (in_array("view_users",$user_privileges) || in_array("all",$user_privileges)) {
            
            // Page title
            $data["page_title"] = 'RTB.cat - Users add new';
            
            // Content Title
            $data["content_title"] = 'Users';

            // Topbar right
            $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);

            // Side menu
            $data["side_menu"] = "";
            $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_users", "", true);
            
            // Content
            $data["content"] = "";
            if (in_array("add_users",$user_privileges) || in_array("all",$user_privileges)) {
                $get_roles_sql = "SELECT * FROM `roles`";
                $get_roles_query = $this->db->query($get_roles_sql);
                $get_roles_result = $get_roles_query->result_array();
                $roles_data = array();
                foreach($get_roles_result as $role_data){
                    if($_SESSION['userdata']['role_id'] > 1){
                        if($role_data['id'] != 1){
                            $roles_data[$role_data['id']] = $role_data['type'];
                        }
                    }
                    else{
                        $roles_data[$role_data['id']] = $role_data['type'];
                    }
                }
                $form_data = array('roles'=>$roles_data);
                $data["content"] .= $this->load->view("main/v_panel_user_new", $form_data, true);
            }

            $data['sess_expiration'] = $this->config->item('sess_expiration');
            $this->load->view("v_dashboard", $data);
        }
        else {
            show_404();
        }
    }
    private function save_new_user() {

        // Privileges.
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        // Post data.
        $name = $this->input->post("name");
        $email = $this->input->post("email");
        $company = $this->input->post("company");
        $username = $this->input->post("username");
        $password = $this->auth->hash($this->input->post("password"),$username);
        $role_id = $this->input->post("role_id");
        $status = $this->input->post("status");
        $apnx_id = $this->input->post("apnx_id");

        // Process request.
        if (in_array("add_users",$user_privileges) || in_array("all",$user_privileges)) {
            $insert_sql = "INSERT INTO `users`(`name`,`email`,`company`,`username`,`password`,`role_id`,`status`,`apnx_id`) VALUES('{$name}','{$email}','{$company}','{$username}','{$password}','{$role_id}','{$status}','{$apnx_id}')";
            if($this->db->query($insert_sql)){
                $response = array(
                    "status" => "ok",
                    "message" => "New user added."
                );
            }
            else{
                $response = array(
                    "status" => "error",
                    "message" => "Database insert failed."
                );
            }
        }
        else {
            $response = array(
                "status" => "error",
                "message" => "Unauthorized request."
            );
        }
        header("Content-Type: application/json");
        echo json_encode($response);
    }
    private function edit_user() {
        $user_id = isset($this->uri->segments[3])? (int)$this->uri->segments[3] : 0;
        if(!empty($user_id)){

            $get_sql = "
            SELECT `users`.`id` AS `user_id`,`users`.`name`,`users`.`email`,`users`.`company`,`users`.`username`,`users`.`role_id`,`users`.`status`,`users`.`apnx_id`,`roles`.`type`
            FROM `users` INNER JOIN `roles` ON `users`.`role_id`=`roles`.`id` WHERE `users`.`id`='{$user_id}'";

            $get_query = $this->db->query($get_sql);

            if($get_query->num_rows() == 1){

                // Privileges
                $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

                if(in_array("edit_users",$user_privileges) || in_array("all",$user_privileges)){
                    
                    // Page title
                    $data["page_title"] = 'RTB.cat - Users';
                    
                    // Content Title
                    $data["content_title"] = 'Users';

                    // Topbar right
                    $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);

                    // Side menu
                    $data["side_menu"] = "";
                    $data["side_menu"] .= $this->load->view("side_bar/v_side_menu_users", "", true);
                    
                    // Content
                    $data["content"] = "";
                    $get_roles_sql = "SELECT * FROM `roles`";
                    $get_roles_query = $this->db->query($get_roles_sql);
                    $get_roles_result = $get_roles_query->result_array();
                    $roles_data = array();
                    foreach($get_roles_result as $role_data){
                        if($_SESSION['userdata']['role_id'] > 1){
                            if($role_data['id'] != 1){
                                $roles_data[$role_data['id']] = $role_data['type'];
                            }
                        }
                        else{
                            $roles_data[$role_data['id']] = $role_data['type'];
                        }
                    }
                    $userdata = $get_query->result_array();
                    $user_data = array('userdata'=>$userdata[0],'roles'=>$roles_data);
                    $data["content"] .= $this->load->view("main/v_panel_user_edit", $user_data, true);

                    $data['sess_expiration'] = $this->config->item('sess_expiration');
                    $this->load->view("v_dashboard", $data);
                }
                else{
                    show_404();
                }

            }
            else{
                echo "user not found";
            }
        }
    }
    private function update_user() {
        // Privileges.
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        // Post Data.
        $id = (int) $this->input->post("id");
        $name = $this->input->post("name");
        $role = (int) $this->input->post("role_id");
        $username = $this->input->post("username");
        $email = $this->input->post("email");
        $company = $this->input->post("company");
        $apnx_id = $this->input->post("apnx_id");
        $status = $this->input->post("status");

        if(in_array("edit_users",$user_privileges) || in_array("all",$user_privileges)){
            // Update action.
            $update_sql = "UPDATE `users` SET `name`='{$name}',`role_id`='{$role}',`username`='{$username}',`email`='{$email}',`company`='{$company}',`apnx_id`='{$apnx_id}',`status`='{$status}' WHERE `id`='{$id}'";
            $this->db->query($update_sql);
            if($this->db->affected_rows() > 0){
                $response = array(
                    "status" => "ok",
                    "message" => "Changes saved."
                );
            }
            else{
                $response = array(
                    "status" => "error",
                    "message" => "No entry to update."
                );
            } 
        }
        else{
            $response = array(
                "status" => "error",
                "message" => "Unauthorized action."
            );
        }
        header("Content-Type: application/json");
        echo json_encode($response);
    }
    private function delete_user() {
        // Privileges.
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        if(in_array("delete_users",$user_privileges) || in_array("all",$user_privileges)){
            $user_id = isset($this->uri->segments[3])? (int)$this->uri->segments[3] : 0;
            // Delete action.
            if(!empty($user_id)){
                $delete_sql = "DELETE FROM `users` WHERE `users`.id='{$user_id}'";
                $this->db->query($delete_sql);
                header("Location: ".base_url('users/list'));
            }
            else{
                die("Invalid action.");
            }
        }
        else{
            die("Unauthorized access.");
        }
    }
}