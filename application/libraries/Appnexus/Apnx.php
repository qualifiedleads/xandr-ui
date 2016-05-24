<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Apnx
{
    private $config;
    private $download_attempts = 0;
    private $login_attempts = 0;
    private $token_dir;
    private $token_text;
    private $token_time;
    private $user;
    private $user_index = 0;
    
    public function __construct()
    {
        include "config.php";

        // Set defaults.
        $this->user = @$config['api_creds'][0];
        $this->token_dir = __DIR__.'/logs/sessions/a0';
        $this->token_text = $this->token_dir.'/token';
        $this->token_time = $this->token_dir.'/time';
    }

    public function setUserIndex($num = 0)
    {
        if ($num)
        {
            if (array_key_exists($num, $this->config['api_creds']))
            {
                $this->user_index = $num;
                $this->user = $this->config['api_creds'][$num];
                $this->token_dir = __DIR__.'/logs/sessions/a'.$num;
                $this->token_text = $this->token_dir.'/token';
                $this->token_time = $this->token_dir.'/time';
                
                if (!is_dir($this->token_dir))
                {
                    if (mkdir($this->token_dir, 0777, true))
                    {
                        file_put_contents($this->token_text, "0");
                        file_put_contents($this->token_time, "0");
                    }
                }
            }
            else
            {
                die("API user index not found.");
            }
        }
    }

    public function getReport($report_id)
    {
        if($result = $this->requestGet('report?id='.$report_id))
        {
            $result = json_decode($result, true);

            if (!isset($result['response']['error']))
            {
                if (isset($result["response"]["execution_status"]))
                {
                    if ($result["response"]["execution_status"] != "ready")
                    {
                        if ($this->download_attempts < 5)
                        {
                            $this->download_attempts++;
                            sleep(1);
                            $this->getReport($report_id);
                        }
                        else
                        {
                            $this->logError("Failed downloading report with id {$report_id}.");
                            return $this->download_attempts;
                        }
                    }
                    else
                    {
                        return $this->requestGet('report-download?id='.$report_id);
                    }
                }
                else
                {
                    return "Something else.";
                }
            }
            else
            {
                $this->logError($result['response']['error']);
                return $result['response'];
            }
        }     
    }

    public function getTokenText()
    {
        if ($token_text = file_get_contents($this->token_text))
        {
            return $token_text;
        }
        else
        {
            die("Cannot retrieve token.");
        }
    }

    public function getTokenTime()
    {
        $token_time = @file_get_contents($this->token_time);

        if (!$token_time)
        {
            if (!is_dir($this->token_dir))
            {
                if (mkdir($this->token_dir, 0777, true))
                {
                    file_put_contents($this->token_time, "1");
                    return "1";
                }
            }
            else
            {
                return false;
            }
        }
        else
        {
            return $token_time;
        }
    }

    public function getTokenTimeRemaining($scale = null)
    {
        $time_remaining = (int) $this->getTokenTime();

        if ($scale)
        {
            if ($scale == "minute")
            {
                return ($time_remaining - time()) / 60;
            }
            if ($scale == "hour")
            {
                return (($time_remaining - time()) / 60) / 60;
            }
        }
        else
        {
            return ($time_remaining - time());
        }
    }

    public function logError($message = null)
    {
        if ($this->config['enable_error_logs'])
        {
            $data = date($this->config['date_format'], time()).' - '.$message."\n";
            @file_put_contents(__DIR__."/logs/errors.log", $data, FILE_APPEND);
        }
    }

    public function login()
    {
        $endpoint = $this->config['api_base'].'auth';
        $array_request = array(
            "auth" => array(
                "username" => $this->user['name'],
                "password" => $this->user['pass']
            )
        );
        $json_request = json_encode($array_request);

        // Send request.
        $curl = curl_init($endpoint);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $json_request);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($curl);

        // Process response.
        $response_data = json_decode($response, true);

        if (isset($response_data['response']['token']))
        {
            
            $token = $response_data['response']['token'];
            $expiry = time() + $this->config['token_expiry'];

            # Save token to file.
            file_put_contents($this->token_text, $token);

            # Save token expiration time to file.
            file_put_contents($this->token_time, $expiry);

            return true;
        }
        else
        {
            return false;
        }
    }

    public function keepAlive()
    {
        //$token_text = $this->getTokenText();
        $token_time = $this->getTokenTime();

        if (time() < $token_time)
        {
            return true;
        }
        else
        {
            $max_retry = $this->config['max_login_retry'];

            if (!$this->login())
            {
                if ($this->login_attempts < $max_retry)
                {
                    $this->login_attempts++;
                    $this->logError("Login failed. Attempting retry ".$this->login_attempts.'...');
                    usleep(600000);
                    $this->keepAlive();
                }
                else
                {
                    $this->logError("Login failed permanently.");
                    return false;
                }
            }
            else
            {
                return true;
            }
        }
    }

    public function requestGet($endpoint)
    {
        if ($this->keepAlive())
        {
            $curl = curl_init($this->config['api_base'].$endpoint);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$this->getTokenText()));
            curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "GET");
            return curl_exec($curl);
        }
        else
        {
            return false;
        }
    }

    public function requestPost($endpoint, $json_data)
    {
        if ($this->keepAlive())
        {
            $curl = curl_init($this->config['api_base'].$endpoint);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$this->getTokenText()));
            curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "POST");
            curl_setopt($curl, CURLOPT_POSTFIELDS, $json_data);
            return curl_exec($curl);
        }
        else
        {
            return false;
        }
    }

    public function requestPut($endpoint, $json_data)
    {
        if ($this->keepAlive())
        {
            $curl = curl_init($this->config['api_base'].$endpoint);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_HTTPHEADER, array("Authorization: ".$this->getTokenText()));
            curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PUT");
            curl_setopt($curl, CURLOPT_POSTFIELDS, $json_data);
            return curl_exec($curl);
        }
        else
        {
            return false;
        }
    }
}