<?php
defined('BASEPATH') OR exit('No direct script access allowed');
/**
* Users model.
*/
class M_users extends CI_Model
{
    public function __construct()
    {
        parent::__construct();
    }

    /*
    checkBy($pointers) - Gets user detail by the supplied
        key=>value pair. Returns true when found.
    +-----------+---------------------------------------------+
    | $pointers | Array of column=>value pair for query.      |
    +-----------+---------------------------------------------+
    */
    public function checkBy($pointers)
    {
        $index = 0;
        $sql = "SELECT `users`.`id`
                FROM `users`
                ";
        
        foreach($pointers as $key=>$val)
        {
            if($index == 0)
            {
                $sql .= " WHERE `{$key}`='{$val}'";
                $index++;
            }
            else
            {
                $sql .= " AND `{$key}`='{$val}'";
            }
        }

        $query = $this->db->query($sql);
        $result = $query->num_rows();

        if($result > 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    /*
    getBy($pointers, $json) - Gets user detail by the supplied
        key=>value pair. Returns data array or json.
    +-----------+---------------------------------------------+
    | $pointers | Array of column=>value pair for query.      |
    +-----------+---------------------------------------------+
    | $json     | If true will return json formatted result.  |
    +-----------+---------------------------------------------+
    */
    public function getBy($pointers, $json = false)
    {
        $index = 0;
        $sql = "SELECT
                `users`.`id` AS `user_id`,
                `users`.`name`,
                `users`.`email`,
                `users`.`company`,
                `users`.`username`,
                `users`.`role_id`,
                `users`.`status`,
                `roles`.`type` as `role_name`
                FROM `users`
                INNER JOIN `roles`
                ON `users`.`role_id`=`roles`.`id`
                ";
        
        foreach($pointers as $key=>$val)
        {
            if($index == 0)
            {
                $sql .= " WHERE `users`.`{$key}`='{$val}'";
                $index++;
            }
            else
            {
                $sql .= " AND `users`.`{$key}`='{$val}'";
            }
        }

        $query = $this->db->query($sql);
        $result = $query->result_array();

        if ($json)
        {
            return json_encode($result);
        }
        else
        {
            return $result;
        }
    }

    /*
    getAll($json) - Gets all users. Returns array or json.
    +-----------+---------------------------------------------+
    | $json     | If true will return json formatted result.  |
    +-----------+---------------------------------------------+
    */
    public function getAll($json = false)
    {
        $sql = "SELECT
                `users`.`id` AS `user_id`,
                `users`.`name`,
                `users`.`email`,
                `users`.`company`,
                `users`.`username`,
                `users`.`role_id`,
                `users`.`status`,
                `roles`.`type` as `role_name`
                FROM `users`
                INNER JOIN `roles`
                ON `users`.`role_id`=`roles`.`id`
                ";
        $query = $this->db->query($sql);
        $result = $query->result_array();

        if ($json)
        {
            return json_encode($result);
        }
        else
        {
            return $result;
        }
    }

    /*
    getRoles($json) - Get roles & privileges. Returns array or
        json.
    +-----------+---------------------------------------------+
    | $json     | If true will return json formatted result.  |
    +-----------+---------------------------------------------+
    */
    public function getRoles($json = false)
    {
        $sql = "SELECT
                `roles`.`id` AS `role_id`,
                `roles`.`type` AS `role_type`,
                `roles`.`privileges`
                FROM `roles`
                ";

        $query = $this->db->query($sql);
        $result = $query->result_array();

        if ($json)
        {
            return json_encode($result);
        }
        else
        {
            return $result;
        }
    }

    /*
    add($pointers, $json) - Insert user detail by the supplied
        key=>value pair. Returns true or false.
    +-----------+---------------------------------------------+
    | $pointers | Array of column=>value pair for query.      |
    +-----------+---------------------------------------------+
    | $json     | If true will return json formatted result.  |
    +-----------+---------------------------------------------+
    */
    public function add($pointers)
    {
        $index = 0;
        $sql = "INSERT INTO `users`";
        
        foreach($pointers as $key=>$val)
        {
            if($index == 0)
            {
                $sql .= " SET `{$key}`='{$val}'";
                $index++;
            }
            else
            {
                $sql .= ", `{$key}`='{$val}'";
            }
        }

        $query = $this->db->query($sql);

        return $this->db->affected_rows() > 0;
    }
}