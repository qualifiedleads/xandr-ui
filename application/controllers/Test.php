<?php
/**
* Test
*/
class Test extends CI_Controller
{
    
    public function __construct()
    {
        parent::__construct();
        
    }
    public function index()
    {

    }
    public function send()
    {
        $to = $this->input->get("to");

        if ($to)
        {
            $subject = "Test Message";
            $message_plain = "Hello,\nThis is a sample plain message.\nstats.rtb.cat";
            
            if (mail($to, $subject, $message_plain))
            {
                echo "Message sent to email.";
            }
            else
            {
                echo "Email sending failed.";
            }
        }
    }
}