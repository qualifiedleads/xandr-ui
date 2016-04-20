<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Charts extends CI_Controller {
    public function __construct() {
        parent::__construct();
        $this->load->library("auth");
        $this->auth->limit();
    }
    public function _remap($uri) {
        if($uri == "impressions-vs-cost") {
            $this->impressions_vs_cost();
        }
        elseif($uri == "ctr-vs-cpa") {
            $this->ctr_vs_cpa();
        }
        else{
            show_404();
        }
    }
    private function impressions_vs_cost() {
        // Page title
        $data["page_title"] = 'RTB.cat - Charts';
        // Content Title
        $data["content_title"] = 'Charts <small>Impressions vs. Cost</small>';

        // Side menu
        $user_privileges = explode(',', $_SESSION['userdata']['privileges']);
        if(in_array("view_campaign_stats",$user_privileges)){
            $data["side_menu"] = $this->load->view("side_bar/v_side_menu_campaign_stats", "", true);
        }
        // Topbar right
        $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);
        $data["content"] = $this->load->view("fragments/v_htm_impressions_vs_cost", "", true);
        $data['sess_expiration'] = $this->config->item('sess_expiration');
        $this->load->view("v_dashboard", $data);
    }
    private function ctr_vs_cpa() {
        // Page title
        $data["page_title"] = 'RTB.cat - Charts';
        // Content Title
        $data["content_title"] = 'Charts <small>CTR vs. CPA(Conversion)</small>';

        // Side menu
        $user_privileges = explode(',', $_SESSION['userdata']['privileges']);
        if(in_array("view_campaign_stats",$user_privileges)){
            $data["side_menu"] = $this->load->view("side_bar/v_side_menu_campaign_stats", "", true);
        }
        // Topbar right
        $data["topbar_right_menu"] = $this->load->view("fragments/v_topbar_menu_right", "", true);
        $data["content"] = $this->load->view("test/sample_panel1", "", true);
        $data['sess_expiration'] = $this->config->item('sess_expiration');
        $this->load->view("v_dashboard", $data);
    }
}