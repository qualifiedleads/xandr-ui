<?php
/**
* Test
*/
class Test extends CI_Controller
{
    
    public function __construct()
    {
        parent::__construct();
        $this->load->library("Appnexus/Apnx");
        $this->load->helper('url');
    }
    public function index()
    {

    }
    public function getAnalytics()
    {
        
    }
    public function serverName()
    {
        $server = $_SERVER['SERVER_NAME'];
        echo domain_base($server);
    }
}