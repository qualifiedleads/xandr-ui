<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Auth {
    public function __construct(){
        session_start();
        session_regenerate_id(true);
    }
    public function destroy(){

    }
    public function limit(){
        $CI =& get_instance();
        if(!isset($_SESSION['userdata'])){
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
                    header("Location: ".base_url('sessions'));
                }
            }
            else{
                header("Location: ".base_url('sessions'));
            }
        }
    }
    public function hash($password,$salt){
        $password = md5($password.$salt);
        $salt = md5($salt);
        return substr($password, 0, 13).substr($salt, 5, 6).substr($password, 13, 19);
    }
}