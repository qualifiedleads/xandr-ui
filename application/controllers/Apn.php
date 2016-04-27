<?php

class Apn extends CI_Controller {
    
    private $req_count = 0;
    private $req_count_limit = 4;
    private $report_id = "";

    public function __construct() {
        parent::__construct();
        $this->config->load("appnexus");
        date_default_timezone_set('UTC');
        $this->date_format = $this->config->item("apnx_datetime");
    }
    public function index() {}
    public function list_domains($advertiser_id="") {
        if($this->keep_alive()){
            $endpoint = $this->config->item("apnx_url")."domain-list";
            $token = trim(file_get_contents($this->config->item("apnx_token_file")));
            $curl = curl_init($endpoint);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$token));
            $response = curl_exec($curl);
            print_r(json_decode($response, true));
        }
        else{
            echo "Connection failed.";
        }
    }
    public function update_domain_list($list_id="", $domains="") {
        if($this->keep_alive()){
            if(is_numeric($list_id)){
                // Required values.
                $endpoint = $this->config->item("apnx_url")."domain-list?id=".$list_id;
                $token = trim(file_get_contents($this->config->item("apnx_token_file")));
                $data = array("domains"=>$domains);
                $json_request = $this->load->view("json/json_domain_list", $data, true);

                // Curl request.
                $curl = curl_init($endpoint);
                curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$token));
                curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PUT");
                curl_setopt($curl, CURLOPT_POSTFIELDS, $json_request);
                $response = curl_exec($curl);

                // Process response.
                $response = json_decode($response, true);

                if(isset($response['response']['status'])){
                    if($response['response']['status'] == "OK"){
                        return true;
                    }
                    else{
                        return false;
                    }
                }
                elseif(isset($response['response']['error_id'])){
                    if($response['response']['error_id'] == "NOAUTH"){
                        if($this->login()){
                            $this->update_domain_list();
                        }
                        else{
                            return false;
                        }
                    }
                    else{
                        return false;
                    }
                }
                else{
                    return false;
                }
            }
            else{
                return false;
            }
        }
        else{
            return false;
        }
    }
    public function filter_domains($client_file=null) {

        /*
        * Filter the domains on a particular campaign and update the list.
        */

        $this->log($client_file." triggered.");

        if($client_file){

            // Verify that the file exists first.
            $file_path = $this->config->item("apnx_log_folder").$client_file.'.json';
            if(file_exists($file_path)){
                $client_settings = json_decode(file_get_contents($file_path));
            }
            else{
                $error = date(DATE_RFC1036, time()).' - Client file not found.';
                $error_log = $this->config->item("apnx_error_file");
                @file_put_contents($error_log, $error."\n", FILE_APPEND);
                echo $error;
                exit;
            }

            if($this->keep_alive()){

                /*
                * Campaign settings
                */

                $advertiser_id = $client_settings->advertiser_id;
                $campaign_id = $client_settings->campaign_id;
                $whitelist_id = $client_settings->whitelist_id;
                $blacklist_id = $client_settings->blacklist_id;
                $media_cost['value'] = @$client_settings->rules->media_cost->value;
                $media_cost['operator'] = @$client_settings->rules->media_cost->operator;
                $condition_file = $this->config->item("apnx_log_folder").$client_settings->rules->condition_file;

                //--------------------------------------------------------------------------------
                // Required values.
                $endpoint = $this->config->item("apnx_url")."report?advertiser_id=".$advertiser_id;
                $token = trim(file_get_contents($this->config->item("apnx_token_file")));
                $last_45_days = date($this->date_format, time()-3888000);
                $today = date($this->date_format, time());
                $data = array(
                    'campaign_id' => $campaign_id,
                    'start_date' => $last_45_days,
                    'end_date' => $today,
                    'media_cost' => $media_cost
                );
                $json_request = $this->load->view("json/json_domain_report", $data, true);

                // Curl request for report.
                $curl = curl_init($endpoint);
                curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$token));
                curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "POST");
                curl_setopt($curl, CURLOPT_POSTFIELDS, $json_request);
                $response = curl_exec($curl);
                $response = json_decode($response, true);

                // Process response.
                if(isset($response["response"]["report_id"])){ # Report ID is present.
                    $this->report_id = $response["response"]["report_id"];
                    $check_result = $this->check_report($this->report_id); # Check api until report is ready.
                    if($check_result != "failed"){
                        $result = $this->get_report($check_result); # Get report CSV report.
                        if(json_decode($result)) { # If response is not a CSV. Meaning json with error code.
                            $this->req_count = 0;
                            sleep(1);
                            $this->filter_domains();
                        }
                        else{ # If response is a CSV.
                            
                            $list = array("whitelist"=>array(),"blacklist"=>array());
                            $lines = explode(PHP_EOL, $result);
                            array_shift($lines);
                            array_pop($lines);

                            if(count($lines) > 0){
                                /*
                                +-----------------------------------------------------
                                | WHITELIST & BLACKLIST CONDITIONAL STATEMENT HERE
                                +-----------------------------------------------------
                                */
                                // Whitelist and blacklist domains.
                                foreach($lines as $csv_line){
                                    $csv_cols = str_getcsv($csv_line);
                                    $domain = $csv_cols[0];
                                    $cpa = $csv_cols[1];
                                    $conv = $csv_cols[2]+$csv_cols[3];
                                    $cost = $csv_cols[4];

                                    if(file_exists($condition_file)){
                                        include($condition_file);
                                    }

                                }
                                /*
                                +--------------------------------------------------------
                                */
                            }

                            // Process the list.
                            $log_folder = $this->config->item("apnx_log_folder");

                            // For whitelist.
                            if(count($list["whitelist"]) > 0){

                                $whitelist_file = $log_folder.'whitelist_'.$whitelist_id.'.log';
                                $whitelist_array = array();

                                if(file_exists($whitelist_file)){
                                    $whitelist_entries = explode(PHP_EOL, trim(file_get_contents($whitelist_file)));
                                    $whitelist_raw = array_merge($list["whitelist"], $whitelist_entries);
                                    $whitelist_array = array_unique($whitelist_raw);
                                    $whitelist_text = implode(PHP_EOL, $whitelist_array);

                                    // Save list to local file.
                                    file_put_contents($whitelist_file, $whitelist_text);
                                }
                                else{
                                    $whitelist_array = $list["whitelist"];

                                    // Save list to local file.
                                    $whitelist_text = implode(PHP_EOL, $list["whitelist"]);
                                    file_put_contents($whitelist_file, $whitelist_text);
                                }

                                // Update live domain targeting list.
                                $whitelist_domain_array = array_map(function($o){return '"'.$o.'"';}, $whitelist_array);
                                $whitelist_domain_text = implode(",", $whitelist_domain_array);
                                $this->update_domain_list($whitelist_id, $whitelist_domain_text);
                            }
                            else{
                                $whitelist_domain_text = "Whitelist counted 0";
                            }

                            // For blackslist.
                            if(count($list["blacklist"]) > 0){

                                $blacklist_file = $log_folder.'blacklist_'.$blacklist_id.'.log';
                                $blacklist_array = array();
                                
                                if(file_exists($blacklist_file)){
                                    $blacklist_entries = explode(PHP_EOL, trim(file_get_contents($blacklist_file)));
                                    $blacklist_raw = array_merge($list["blacklist"], $blacklist_entries);
                                    $blacklist_array = array_unique($blacklist_raw);
                                    $blacklist_text = implode(PHP_EOL, $blacklist_array);

                                    // Save list to local file.
                                    file_put_contents($blacklist_file, $blacklist_text);
                                }
                                else{
                                    $blacklist_array = $list["blacklist"];

                                    // Save list to local file.
                                    $blacklist_entries = implode(PHP_EOL, $list["blacklist"]);
                                    file_put_contents($blacklist_file, $blacklist_entries);
                                }

                                // Update live domain targeting list.
                                $blacklist_domain_array = array_map(function($o){return '"'.$o.'"';}, $blacklist_array);
                                $blacklist_domain_text = implode(",", $blacklist_domain_array);
                                $this->update_domain_list($blacklist_id, $blacklist_domain_text);
                            }
                            else{
                                $blacklist_domain_text = "Blacklist counted 0";
                            }

                            /*
                            +-----------------------------------------------------------------------
                            | POST SUCCESS PROCESS
                            +-----------------------------------------------------------------------
                            */
                            // For visual output.
                            // echo $whitelist_domain_text;
                            // echo "<br />";
                            // echo $blacklist_domain_text;
                            // Log execution.
                            $this->log($client_file." success.");
                            echo "Whitelist: <br />";
                            echo $whitelist_domain_text;
                            echo "<br /><br />";
                            echo "Blacklist: <br />";
                            echo $blacklist_domain_text;
                            /*
                            +-----------------------------------------------------------------------
                            */

                        }
                    }
                    else{
                        echo "failed";
                    }
                }
                elseif(isset($response["response"]["error_id"])){
                    if($response["response"]["error_id"] == "NOAUTH"){
                        if($this->login()){
                            $this->filter_domains();
                        }
                        else{
                            $error = date(DATE_RFC1036, time()).' - Authentication failed.';
                            $error_log = $this->config->item("apnx_error_file");
                            @file_put_contents($error_log, $error."\n", FILE_APPEND);
                            echo $error;
                        }
                    }
                }
                else{
                    $error = date(DATE_RFC1036, time()).' - ';
                    $error_log = $this->config->item("apnx_error_file");
                    if(isset($response['response']['error'])){
                        $error .= $response['response']['error'];
                    }
                    else{
                        $error .= "Unknown error has occured.";
                    }
                    @file_put_contents($error_log, $error."\n", FILE_APPEND);
                    echo "$error";
                }
            }
            else{
                $error_log = $this->config->item("apnx_error_file");
                $error = date(DATE_RFC1036, time())." - Token refresh failed.";
                @file_put_contents($error_log, $error."\n", FILE_APPEND);
                echo $error;
            }
        }
    }
    private function login() {
        // Basic values.
        $api_base = $this->config->item("apnx_url");
        $endpoint = $api_base."auth";
        $username = $this->config->item("apnx_user");
        $password = $this->config->item("apnx_pass");
        $token_time = $this->config->item("apnx_token_time");
        $token_file = $this->config->item("apnx_token_file");
        $token_exp_file = $this->config->item("apnx_token_expire_file");

        // Login values.
        $data["username"] = trim($username);
        $data['password'] = trim($password);
        $json_request = $this->load->view("json/json_apn_login", $data, true);

        //Send request.
        $curl = curl_init($endpoint);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $json_request);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($curl);

        // Process response.
        $response_data = json_decode($response, true);
        if(isset($response_data['response']['token'])){
            $token = $response_data['response']['token'];
            $expiry = time() + $token_time;

            # Save token to file.
            file_put_contents($token_file, $token);
            # Save token expiration time to file.
            file_put_contents($token_exp_file, $expiry);

            return true;
        }
        else{
            return false;
        }
    }
    private function keep_alive() {
        /*
        * Keeps the token updated. Returns true when successful.
        */
        $token_exp_file = $this->config->item("apnx_token_expire_file");
        $token_exp_allowance = $this->config->item("apnx_token_expire_allowance");
        $token_expiry = file_get_contents($token_exp_file);
        $time_now = time()+$token_exp_allowance;
        if($time_now > $token_expiry) {
            if($this->login()){
                return true;
            }
            else{
                return false;
            }
        }
        else{
            return true;
        }
    }
    private function check_report($report_id) {
        /*
        * Check if the report is ready. Returns url text for download or the text "failed"
        * on failure.
        */

        // Make sure request did not exceed the threshold limit.
        if($this->req_count < $this->req_count_limit){
            $this->req_count++;

            // Required values.
            $endpoint = $this->config->item("apnx_url")."report?id=".$report_id;
            $token = trim(file_get_contents($this->config->item("apnx_token_file")));

            // Curl request.
            $curl = curl_init($endpoint);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$token));
            $response = curl_exec($curl);
            $response = json_decode($response, true);

            // Process response.
            if(isset($response["response"]["execution_status"])){
                if($response["response"]["execution_status"] != "ready"){
                    sleep(1);
                    $this->check_report($this->report_id);
                }
                else{
                    if(isset($response["response"]["report"]["url"])){ # Report is ready for download.
                        return $response["response"]["report"]["url"];
                    }
                    else{
                        return "failed";
                    }
                }
            }
            else{
                return "failed";
            }
        }
        else{
            return "failed";
        }
    }
    private function get_report($report_url) {
        /*
        * Returns the actual report data as text.
        */

        // Required values.
        $endpoint = $this->config->item("apnx_url").$report_url;
        $token = trim(file_get_contents($this->config->item("apnx_token_file")));

        // Curl request.
        $curl = curl_init($endpoint);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$token));
        return curl_exec($curl);
    }
    public function remaining() {
        $token_exp_file = $this->config->item("apnx_token_expire_file");
        $token_exp_allowance = $this->config->item("apnx_token_expire_allowance");
        $token_expiry = file_get_contents($token_exp_file);
        $remaining = $token_expiry - (time()+$token_exp_allowance);
        echo "Remaining time:".round($remaining/60)." minutes";
    }
    public function files($filename=null){
        $file_path = $this->config->item("apnx_log_folder").$filename;
        if(file_exists($file_path)){
            $file_contents = file_get_contents($file_path);
            echo nl2br($file_contents);
        }
        else{
            echo "File not found.";
            exit;
        }
    }
    public function whitelist($id=null){
        if($id){
            $file_path = $this->config->item("apnx_log_folder")."whitelist_{$id}.log";
            if(file_exists($file_path)){
                $file_contents = trim(file_get_contents($file_path));
                echo nl2br($file_contents);
            }
            else{
                echo "File not found.";
                exit;
            }
        }
    }
    public function blacklist($id=null){
        if($id){
            $file_path = $this->config->item("apnx_log_folder")."blacklist_{$id}.log";
            if(file_exists($file_path)){
                $file_contents = trim(file_get_contents($file_path));
                echo nl2br($file_contents);
            }
            else{
                echo "File not found.";
                exit;
            }
        }
    }
    private function log($message=null){
        if($message){
            $log_file = $this->config->item("apnx_log_folder")."runs.log";
            $timestamp = date(DATE_RFC850, time());
            $log_entry = "{$timestamp} - {$message}".PHP_EOL;
            file_put_contents($log_file, $log_entry, FILE_APPEND);
        }
    }
    public function log_clear($file_name=null){
        if($file_name){
            $log_file = $this->config->item("apnx_log_folder")."{$file_name}.log";
            if(file_exists($log_file)){
                file_put_contents($log_file, "");
                echo "Log cleared.";
            }
            else{
                echo "File not found.";
            }
        }
    }
    public function test() {
        $last_45_days = date($this->date_format, time()-3888000);
        $today = date($this->date_format, time());
        $data = array(
            'start_date' => $last_45_days,
            'end_date' => $today
        );
        print_r($data);
    }
}