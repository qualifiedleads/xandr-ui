<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Sessions extends CI_Controller {
    public function __construct(){
        parent::__construct();
        $this->load->library("auth");
    }
    public function index(){
        if($this->input->post("task")!=""){
            $task = $this->input->post("task");
            /* Sign In */
            if($task == "signin"){
                if($result = $this->signin($this->input->post("username"), $this->input->post("password"))){
                    if($result == "active"){
                        $response = array(
                            "status"=>"ok",
                            "message"=>base_url()
                        );
                        header('Content-Type: application/json');
                        echo json_encode($response);
                    }
                    if($result == "inactive"){
                        $response = array(
                            "status"=>"error",
                            "message"=>"Account is inactive."
                        );
                        header('Content-Type: application/json');
                        echo json_encode($response);
                    }   
                }
                else {
                    $response = array(
                        "status" => "error",
                        "message" => "Login failed."
                    );
                    header('Content-Type: application/json');
                    echo json_encode($response);
                }
            }
            /* Reset */
            elseif($task == "reset"){
                if($this->forgot_password()){
                    $response = array(
                        "status" => "ok",
                        "message" => "Instructions sent."
                    );
                    header('Content-Type: application/json');
                    echo json_encode($response);
                }
                else{
                    $response = array(
                        "status" => "error",
                        "message" => "Invalid email."
                    );
                    header('Content-Type: application/json');
                    echo json_encode($response);
                }
            }
            else{
                $data["login_form"] = $this->load->view("fragments/v_login_form", "", true);
                $data["reset_form"] = $this->load->view("fragments/v_reset_form", "", true);
                $this->load->view("v_login", $data);
            }
        }
        else{
            $data["login_form"] = $this->load->view("fragments/v_form_login", "", true);
            $data["reset_form"] = $this->load->view("fragments/v_form_reset", "", true);
            $this->load->view("v_login", $data);
        }
    }
    private function signin($username,$password){
        $password = $this->auth->hash($password,$username);
        $sql_get = "SELECT *,`users`.`id` AS `user_id` FROM `users` INNER JOIN `roles` ON `users`.`role_id`=`roles`.`id` WHERE `users`.`username`='{$username}' AND `users`.`password`='{$password}'";
        $query = $this->db->query($sql_get);
        if($query->num_rows() == 1){ // User found.
            $user_data = $query->result_array();
            $user_data = $user_data[0];
            if($user_data['status'] == "active"){ // Account is active.
                $sid_time = time()+(int)$this->config->item('sess_expiration');
                $sid_hash = md5($sid_time);
                $sql_update = "UPDATE `users` SET `sid`='{$sid_hash}',`sid_time`='{$sid_time}' WHERE `id`='".$user_data['user_id']."'";
                $this->db->query($sql_update);
                $_SESSION['userdata'] = $user_data;
                $_SESSION['userdata']['id'] = $user_data['user_id'];
                $_SESSION['userdata']['sid'] = $sid_hash;
                $_SESSION['userdata']['sid_time'] = $sid_time;
                if($this->input->post("remember") == 1){ // If remember is checked.
                    setcookie("sid",$sid_hash,$sid_time,'/');
                }
                return "active";
            }
            else{ // Account is inactive.
                return "inactive";
            }
        }
        else{
            return false;
        }
    }
    public function logout(){
        unset($_COOKIE['sid']);
        setcookie('sid', null, -1, '/');
        session_destroy();
        header("Location: ".base_url("sessions"));
    }
    private function forgot_password(){
        $rmail = '/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/';
        $email = $this->input->post("email");
        if(preg_match($rmail, $email)){
            $token = md5(time());
            $token_time = time()+86400;// 24hrs
            $reset_link = base_url("sessions/change_pass/$token");
            
            // Update database.
            $sql_update = "UPDATE `users` set `token`='{$token}',`token_time`='{$token_time}' WHERE `email`='{$email}'";
            $this->db->query($sql_update);

            // Send email.
            $message = $this->load->view("etc/v_changepw_message",array("reset_link"=>$reset_link),true);
            mail($email,"Password Reset",$message,"From: noreply@localhost.net");
            return "ok";
        }
        else{
            return false;
        }
    }
    public function change_pass($token){
        if($token){
            $sql_get = "SELECT *,`users`.`id` AS `user_id` FROM `users` INNER JOIN `roles` ON `users`.`role_id`=`roles`.`id` WHERE `token`='{$token}'";
            $sql_query = $this->db->query($sql_get);
            if($sql_query->num_rows() == 1){
                $user_data = $sql_query->result_array();
                $user_data = $user_data[0];
                $_SESSION['user_temp'] = $user_data;
                if($this->input->post("task") == "change_pass"){
                    $npassword = $this->input->post("npassword");
                    $rpassword = $this->input->post("rpassword");
                    if($npassword != $rpassword){
                        $response = array(
                            "status" => "error",
                            "message" => "Password mismatch."
                        );
                        header("Content-Type: application/json");
                        echo json_encode($response);
                    }
                    else{
                        $newpasswd = $this->auth->hash($npassword,$user_data['username']);
                        $sql_update = "UPDATE `users` SET `users`.`password`='{$newpasswd}',`users`.`token`='',`users`.`token_time`='' WHERE `users`.`id`=".$user_data['user_id'];
                        if($this->db->query($sql_update)){
                            $response = array(
                                "status" => "ok",
                                "message" => "Password changed."
                            );
                            header("Content-Type: application/json");
                            echo json_encode($response);
                        }
                        else{
                            $response = array(
                                "status" => "error",
                                "message" => "Database error."
                            );
                            header("Content-Type: application/json");
                            echo json_encode($response);
                        }
                    }
                }
                else{
                    if($user_data['token_time'] > time()){ // Token is still valid.
                        $data['page_title'] = "RTB.cat - Change Your Password";
                        $data['change_pass_form'] = $this->load->view("fragments/v_form_change_pass",array("token"=>$token),true);
                        $this->load->view("v_change_pass",$data);
                    }
                    else{
                        echo "Token has expired.";
                    }
                }
            }
            else {
                header('HTTP/1.0 403 Forbidden');
                echo "This action is not allowed.";
            }
        }
    }
}