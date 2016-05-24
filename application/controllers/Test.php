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
    }
    public function index()
    {

    }
    public function getAnalytics()
    {
        
    }
    public function serverName()
    {
        echo $_SERVER['SERVER_NAME'];
    }
}