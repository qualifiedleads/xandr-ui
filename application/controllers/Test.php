<?php
/**
* Test
*/
class Test extends CI_Controller
{
    
    public function __construct()
    {
        parent::__construct();
        $this->load->model("m_users");
    }
    public function index()
    {
        $single = ['email'=>'max@localhost.loc'];
        $multiple = ['email'=>'john@doe.tld','username'=>'john','password'=>'johnpass123'];
        echo "<pre>";
        print_r($this->m_users->getBy($single));
    }
}