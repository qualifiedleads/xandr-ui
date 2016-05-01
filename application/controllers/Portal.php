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
    }

    public function index() {
        $this->load->view("theme/inspinia/v_portal_layout");
    }

    public function v2() {
        $data['center_boxes'] = $this->load->view("theme/inspinia/custom/v_portal_boxes", "", true);
        $modal_msg_data = array("modal_id"=>"modal_message","modal_message"=>"Default text.");
        $data['base_element'] = $this->load->view("theme/inspinia/custom/v_bs_modal_message", $modal_msg_data, true);
        $this->load->view("theme/inspinia/v_portal_layout_v2", $data);
    }
}