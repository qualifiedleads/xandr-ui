<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Apnx {
    private $c;
    public function __construct(){
        $this->c =& get_instance();
        $this->c->config->load("appnexus");
    }
    public function remaining() {
        $token_exp_file = $this->c->config->item("apnx_token_expire_file");
        $token_exp_allowance = $this->c->config->item("apnx_token_expire_allowance");
        $token_expiry = file_get_contents($token_exp_file);
        $remaining = $token_expiry - (time()+$token_exp_allowance);
        return "Remaining time: ".round($remaining/60)." minutes";
    }
}