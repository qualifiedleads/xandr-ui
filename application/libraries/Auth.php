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

        // Load necessary dependencies.
        if(!isset($CI->m_users))
        {
            $CI->load->model("m_users");
        }

        # If session userdata does not exist (unauthenticated visitor).
        if(!isset($_SESSION['userdata']))
        {

            # Check for session cookie and revalidate login status.
            if(isset($_COOKIE['sid']))
            {

                $params = ["sid"=>trim($_COOKIE['sid'])];
                $result = $CI->m_users->getSesInfoBy($params);

                if(count($result) == 1)
                {
                    $user_data = $result[0];

                    if(time() > $user_data['sid_time'])
                    {
                        header("Location: ".base_url($redirect_page));
                    }
                    else
                    {
                        $_SESSION['userdata'] = $user_data;
                    }
                }
                else
                {
                    if($redirect_page)
                    {
                        header("Location: {$redirect_page}");
                    }
                    else
                    {
                        exit;
                    }
                }

            }
            else
            {
                if($redirect_page)
                {
                    header("Location: {$redirect_page}");
                }
                else
                {
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
        $params = ["username"=>$username,"password"=>$password];
        $result = $CI->m_users->getSesInfoBy($params);

        if(count($result) == 1){ // User found.

            $user_data = $result[0];

            if($user_data['status'] == "active"){ // Account is active.

                // Update session data to db.
                $sid_time = time() + (int) $CI->config->item('user_sid_time');
                $sid_hash = md5($sid_time);
                $update_params = ["sid"=>$sid_hash,"sid_time"=>$sid_time];
                $CI->m_users->update($update_params, $user_data['user_id']);

                $_SESSION['userdata'] = $user_data;

                if($remember){ // If remember is checked, set cookie.
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