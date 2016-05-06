<?php
defined('BASEPATH') OR exit('No direct script access allowed');

/**
* This controller displays the frontend for users to:
* -sign-in
* -sign-out
* -reset pasword
*/

class Portal extends CI_Controller
{
    
    function __construct()
    {
        parent::__construct();
        $this->load->config("custom");
        $this->load->model("m_users");
    }

    public function index()
    {
        $data['short_title'] = "rtb";
        $data['content'] = $this->load->view("theme/inspinia/portal/v_login", "", true);
        $data['short_footnote'] = 'rtb.cat &copy; 2016';
        $this->load->view("theme/inspinia/v_portal_layout", $data);
    }

    public function v2() {
        $data['center_boxes'] = $this->load->view("theme/inspinia/custom/v_portal_boxes", "", true);
        $modal_msg_data = array("modal_id"=>"modal_message","modal_message"=>"Default text.");
        $data['base_element'] = $this->load->view("theme/inspinia/custom/v_bs_modal_message", $modal_msg_data, true);
        $this->load->view("theme/inspinia/v_portal_layout_v2", $data);
    }
}