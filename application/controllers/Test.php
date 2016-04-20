<?php
class Test extends CI_Controller {
    public function index() {
        $password = md5("thequickbrownfox");
        $salt = md5("romeo1");
        $left = substr($password, 0, 13);
        $center = substr($password, 5, 6);
        $right = substr($password, 13, 19);
        $result = $left.$center.$right;
        $html = <<<HTML
        <div style="font-family: courier">
            <div>{$password}</div>
            <div>{$salt}</div>
            <div>{$result}</div>
        </div>
HTML;
        echo $html;
    }
}