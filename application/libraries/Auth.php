<?php
defined('BASEPATH') OR exit('No direct script access allowed');

/*
* Author: Mike
* Description: This class is used for login related functions.
*/

class Auth {
    public function __construct () {
        session_start();
        session_regenerate_id(true);
    }
    public function limit ($redirect_page = null) {

        /*
        * This function will limit access of protected contents.
        * If the "$redirect_page" parameter is supplied, the current
        * page will be redirected to it else contents will be blank.
        */

        $CI =& get_instance();

        # If session userdata does not exist (unauthenticated visitor).
        if(!isset($_SESSION['userdata'])){

            # Check for session cookie and revalidate login status.
            if(isset($_COOKIE['sid'])){

                $sql_get_1 = "SELECT * FROM `users` INNER JOIN `roles` ON `users`.`role_id`=`roles`.`id` WHERE `sid`='".trim($_COOKIE['sid'])."'";
                $query_get_1 = $CI->db->query($sql_get_1);

                if($query_get_1->num_rows() == 1){
                    $userdata_temp_0 = $query_get_1->result_array();
                    $userdata_temp_0 = $userdata_temp_0[0];
                    if(time() > $userdata_temp_0['sid_time']){
                        header("Location: ".base_url('sessions'));
                    }
                    else{
                        $_SESSION['userdata'] = $userdata_temp_0;
                    }
                }
                else{
                    if($redirect_page) {
                        header("Location: {$redirect_page}");
                    }
                    else {
                        exit;
                    }
                }

            }
            else{
                if($redirect_page) {
                    header("Location: {$redirect_page}");
                }
                else {
                    exit;
                }
            }
        }
    }
    public function hash ($password, $salt) {

        /*
        * This function is used for the hashing of password.
        * This adds salt and changes the normal length of MD5 hash.
        */

        $password = md5($password.$salt);
        $salt = md5($salt);
        return substr($password, 0, 13).substr($salt, 5, 6).substr($password, 13, 19);
    }
    public function signin ($username, $password, $remember = false) {

        /*
        * This function is used for authenticating username & password.
        */

        $CI =& get_instance();

        $password = $this->hash($password, $username);
        $sql_get = "SELECT *,`users`.`id` AS `user_id` FROM `users` INNER JOIN `roles` ON `users`.`role_id`=`roles`.`id` WHERE `users`.`username`='{$username}' AND `users`.`password`='{$password}'";
        $query = $CI->db->query($sql_get);

        if($query->num_rows() == 1){ // User found.

            $user_data = $query->result_array();
            $user_data = $user_data[0];

            if($user_data['status'] == "active"){ // Account is active.

                $sid_time = time() + (int) $CI->config->item('sess_expiration');
                $sid_hash = md5($sid_time);
                $sql_update = "UPDATE `users` SET `sid`='{$sid_hash}',`sid_time`='{$sid_time}' WHERE `id`='".$user_data['user_id']."'";
                $CI->db->query($sql_update);
                $_SESSION['userdata'] = $user_data;
                $_SESSION['userdata']['user_id'] = $user_data['user_id'];
                $_SESSION['userdata']['sid'] = $sid_hash;
                $_SESSION['userdata']['sid_time'] = $sid_time;

                if($remember){ // If remember is checked.
                    setcookie("sid", $sid_hash, $sid_time,'/');
                }

                return array("status"=>"ok","code"=>"active","message"=>"Account is active.");

            }
            else{ // Account is inactive.
                return array("status"=>"error","code"=>"inactive","message"=>"Account is not active.");
            }

        }
        else{
            return array("status"=>"error","code"=>"not_found","message"=>"Authentication failed.");
        }
    }
}