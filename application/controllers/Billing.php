<?php
defined('BASEPATH') OR exit('No direct script access allowed');

/**
* Billing.
*/

class Billing extends CI_Controller
{
    
    function __construct()
    {
        parent::__construct();
        date_default_timezone_set('UTC');
        // $this->load->config("custom");
        // $this->load->model("m_users");
        $this->load->library("auth");
        $this->load->library("Appnexus/Apnx");
    }

    public function index()
    {
        // Limit this particular page to registered users.
        $this->auth->limit(base_url("portal"));

        // Privilege reference.
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        // Navbar Side Contents
        $v_main_layout['nav_header'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_header", ["user_privileges"=>$user_privileges], true);
        $v_main_layout['nav_menus'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_menus", ["user_privileges"=>$user_privileges], true);

        // Navbar Top Contents
        $v_main_layout['nav_logout_button'] = $this->load->view("theme/inspinia/navbar_static_top/v_logout_button", "", true);

        // Page Heading
        $v_page_info['title'] = "Billing Statement";
        $v_page_info['breadcrumbs'] = array('Home' => base_url(),'Billing' => '');
        $v_page_info['user_privileges'] = $user_privileges;
        $v_main_layout['page_info'] = $this->load->view("theme/inspinia/page_heading/v_page_info", $v_page_info, true);
        //$v_main_layout['action_area'] = $this->load->view("theme/inspinia/page_heading/v_action_buttons", "", true);

        // Contents
        $v_main_layout['contents'] = $this->load->view("theme/inspinia/content/v_billing", "", true);

        $this->load->view("theme/inspinia/v_main_layout", $v_main_layout);
    }

    public function getCostImps($apnx_id = null)
    {
        $timestamp = time();
        $YYYY = date("Y", $timestamp);  // A four digit representation of a year.
        $MM = date("m", $timestamp);    // A numeric representation of a month, with leading zeros (01 to 12).
        $MT = date("F", $timestamp);    // A full textual representation of a month (January through December).
        $DD = date("d", $timestamp);    // The day of the month with leading zeros (01 to 31).
        $hh = date("H", $timestamp);    // 24-hour format of an hour (00 to 23).
        $mm = date("i", $timestamp);    // Minutes with leading zeros (00 to 59).
        $ss = date("s", $timestamp);    // Seconds, with leading zeros (00 to 59).

        if ($apnx_id)
        {
            $json_request = $this->load->view("json/json_billing_cost", "", true);
            $response = $this->apnx->requestPost("report?advertiser_id={$apnx_id}", $json_request);
            $response = json_decode($response, true);
            
            if (!$response)
            {
                $error = $response['response']['error'];
                $output = [
                    "status" => "error",
                    "message" => "Authentication failed.",
                    "data" => ""
                ];

                header("Content-Type: application/json");
                echo json_encode($output);
            }
            else if (isset($response['response']['error']))
            {
                $error = $response['response']['error'];
                $output = [
                    "status" => "error",
                    "message" => $error,
                    "data" => ""
                ];

                header("Content-Type: application/json");
                echo json_encode($output);
            }
            else
            {
                $report_id = $response['response']['report_id'];
                $report_csv = $this->apnx->getReport($report_id);
                $report_array = explode("\n", $report_csv);
                $header = array_shift($report_array);
                array_pop($report_array);
                $output = [
                    "status" => "ok",
                    "message" => "Report retrieved successfully.",
                    "data" => ""
                ];
                $data = [
                    "google" => [
                        "media_cost" => 0,
                        "imps" => 0
                    ],
                    "yahoo" => [
                        "media_cost" => 0,
                        "imps" => 0
                    ],
                    "others" => [
                        "media_cost" => 0,
                        "imps" => 0
                    ]
                ];
                $date = [
                    "YYYY" => $YYYY,
                    "MM" => $MM,
                    "MT" => $MT,
                    "DD" => $DD,
                    "hh" => $hh,
                    "mm" => $mm,
                    "ss" => $ss
                ];
                
                // Filter, group according to seller
                foreach ($report_array as $csv)
                {
                    $csv_string = str_getcsv($csv);
                    $member_name = $csv_string[0];
                    $member_id = $csv_string[1];
                    $media_cost = $csv_string[2];
                    $imps = $csv_string[3];

                    // Google
                    if ($member_id == 181)
                    {
                        $data['google']['media_cost'] += $media_cost;
                        $data['google']['imps'] += $imps;
                    }
                    // Yahoo
                    elseif ($member_id == 273)
                    {
                        $data['yahoo']['media_cost'] += $media_cost;
                        $data['yahoo']['imps'] += $imps;
                    }
                    // Others
                    else
                    {
                        $data['others']['media_cost'] += $media_cost;
                        $data['others']['imps'] += $imps;
                    }
                }

                $output['data'] = $data;
                $output['date'] = $date;
                $json_output = json_encode($output);
                
                // JSON output.
                header("Content-Type: application/json");
                echo $json_output;
            }
        }
        else
        {
            $response = [
                "status" => "error",
                "message" => "Advertiser id required."
            ];
            header("Content-Type: application/json");
            echo json_encode($response);
        }
    }
}