<?php
/**
* Test
*/
class Test extends CI_Controller
{
    
    public function __construct()
    {
        parent::__construct();
        $this->load->helper('url');
        $this->load->model("m_users");
    }
    public function index()
    {

    }
    public function get_analytics()
    {
        $advertiser_id = $this->input->get('advertiser_id');
        $columns = $this->input->get('columns');
        $start_date = $this->input->get('start_date');
        $end_date = $this->input->get('end_date');
        $response = ["status"=>"error","code"=>null,"message"=>"Syntax error.","debug_info"=>null];
        $date_date = '/^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$/';
        $date_full = '/^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]) (0[1-9]|1[0-9]|2[0-3]):(\d{2}):(\d{2})$/';
        $date_matches = [];
        $errors = 0;

        // Validate request.
        if (isset($_COOKIE['Authorization']))
        {
            $api_token = $_COOKIE['Authorization'];
            $result = $this->m_users->getBy(['api_token'=>$api_token]);
            if (count($result) == 1)
            {
                $userdata = $result[0];
                if ($userdata['api_time'] < time())
                {
                    $response['message'] = "Token has expired.";
                    $errors++;
                }
            }
            else
            {
                $response['message'] = "Invalid token.";
                $errors++;
            }
        }
        else
        {
            $response['message'] = "Access denied.";
            $errors++;
        }

        // Require a start_date query string & validate its value.
        if ($errors == 0)
        {
            if ($start_date)
            {
                if (preg_match($date_full, $start_date, $date_matches))
                {
                    $start_date = mktime($date_matches[4],$date_matches[5],$date_matches[6],$date_matches[2],$date_matches[3],$date_matches[1]);
                }
                elseif (preg_match($date_date, $start_date, $date_matches))
                {
                    $start_date = mktime(00,00,00,$date_matches[2],$date_matches[3],$date_matches[1]);
                }
                else
                {
                    $response['message'] = "Start date is invalid.";
                    $errors++;
                }
            }
            else
            {
                $response['message'] = "Start date is missing.";
                $errors++;
            }
        }

        // Check for end_date & process output.
        if ($errors == 0)
        {
            if ($end_date)
            {
                if (preg_match($date_full, $end_date, $date_matches))
                {
                    $end_date = mktime($date_matches[4],$date_matches[5],$date_matches[6],$date_matches[2],$date_matches[3],$date_matches[1]);
                }
                elseif (preg_match($date_date, $end_date, $date_matches))
                {
                    $end_date = mktime(23,59,59,$date_matches[2],$date_matches[3],$date_matches[1]);
                }
                else
                {
                    $response['message'] = "End date is invalid.";
                    $errors++;
                }
            }
        }

        // Check for columns.
        if ($errors == 0)
        {
            if ($columns)
            {
                $columns = explode(',', trim($columns));
                $sql_columns = [];

                foreach ($columns as $column)
                {
                    $sql_columns[] = '`network_analytics`.`'.$column.'`';
                }

                $columns = implode(',', $sql_columns);
            }
            else
            {
                $columns = '*';
            }
        }

        // Check for advertiser_id.
        if ($errors == 0)
        {
            if ($advertiser_id)
            {
                if (!is_numeric($advertiser_id))
                {
                    $response['message'] = "Advertiser_id is invalid.";
                    $errors++;
                }
            }
            else
            {
                $response['message'] = "Advertiser_id is required.";
                $errors++;
            }
        }

        // Fetch data if every parameter is clean.
        if ($errors == 0)
        {
            $SQL = "SELECT {$columns} FROM `network_analytics` WHERE `network_analytics`.`date` >= {$start_date}";
            if ($end_date) $SQL .= " AND `network_analytics`.`date` <= {$end_date}";
            $SQL .= " AND `network_analytics`.`advertiser_id` = {$advertiser_id}";
            $SQL .= " ORDER BY `network_analytics`.`date`";

            $query = $this->db->query($SQL);
            $result = $query->result_array();

            $response['status'] = "ok";
            $response['message'] = "Success.";
            $response['data'] = $result;
            $response['debug_info']['rows'] = count($result);
            $response['debug_info']['sql'] = $SQL;
        }

        header("Content-Type: application/json");
        echo json_encode($response);
    }
    public function serverName()
    {
        $server = $_SERVER['SERVER_NAME'];
        echo domain_base($server);
    }
}