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
    getBy($pointers, $json) - Gets user detail by the supplied
        key=>value pair.
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
                `roles`.`type`
                FROM `users`
                INNER JOIN `roles`
                ON `users`.`role_id`=`roles`.`id`
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
    getAll($json) - Gets all of users.
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
                `roles`.`type`
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
}