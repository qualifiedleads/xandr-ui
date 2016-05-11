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
        // $this->load->config("custom");
        // $this->load->model("m_users");
        $this->load->library("Appnexus/Apnx");
    }

    public function index()
    {
        
    }

    public function getCostImps($apnx_id = null)
    {
        $timestamp = time();
        $year = date("Y", $timestamp);
        $nmonth = date("n", $timestamp); // A numeric representation of a month, without leading zeros (1 to 12).
        $tmonth = date("F", $timestamp); // A full textual representation of a month (January through December).
        $day = date("j", $timestamp); // The day of the month without leading zeros (1 to 31).

        $this->apnx->setUserIndex(1);

        if ($apnx_id)
        {
            $json_request = $this->load->view("json/json_billing_cost", "", true);
            $response = $this->apnx->requestPost("report?advertiser_id={$apnx_id}", $json_request);
            $response = json_decode($response, true);
            
            if (isset($response['response']['error']))
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
                    "y" => $year,
                    "nm" => $nmonth,
                    "tm" => $tmonth,
                    "d" => $day
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
                    if ($member_id == 273)
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

    public function test()
    {
        $timestamp = time();
        $year = date("Y", $timestamp);
        $month = date("n", $timestamp);
        $day = date("j", $timestamp);

        
    }
}