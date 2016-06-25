<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Users extends CI_Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->load->config("custom");
        $this->load->model("m_users");
        $this->load->library("auth");
    }
    public function index()
    {
        $task = $this->input->post("task");

        if ($task)
        {
            if ($task == "add")
            {
                $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

                if (in_array("users_add",$user_privileges) || in_array("all",$user_privileges))
                {
                    $name     = $this->input->post("name");
                    $email    = $this->input->post("email");
                    $company  = $this->input->post("company");
                    $username = $this->input->post("username");
                    $role_id  = $this->input->post("role_id");
                    $status   = $this->input->post("status");
                    $apnx_id  = $this->input->post("apnx_id");

                    $result   = "";

                    // Check username.
                    if($this->m_users->checkBy(["username"=>$username]))
                    {
                        $result = ["status"=>"error","code"=>"invalid","message"=>"Username is not available.","data"=>""];
                    }
                    elseif($this->m_users->checkBy(["email"=>$email]))
                    {
                        $result = ["status"=>"error","code"=>"invalid","message"=>"Email is not available.","data"=>""];
                    }
                    else
                    {
                        $insert_data = [
                            "name" => $name,
                            "email" => $email,
                            "company" => $company,
                            "username" => $username,
                            "role_id" => $role_id,
                            "status" => $status,
                            "apnx_id" => $apnx_id,
                            "token" => md5(time().microtime()),
                            "token_time" => time()+$this->config->item("user_token_time")
                        ];

                        if ($this->m_users->add($insert_data))
                        {
                            $new_list = $this->m_users->getAll();
                            $result = ["status"=>"ok","code"=>"valid","message"=>"New user added.","data"=>$new_list];
                        }
                        else
                        {
                            $result = ["status"=>"error","code"=>"valid","message"=>"Insert failed.","data"=>""];
                        }
                    }

                    header("Content-Type: application/json");
                    echo json_encode($result);
                }
            }

            if ($task == "update")
            {
                $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

                if (in_array("users_edit",$user_privileges) || in_array("all",$user_privileges))
                {
                    $user_id  = $this->input->post("user_id");
                    $name     = $this->input->post("name");
                    $email    = $this->input->post("email");
                    $company  = $this->input->post("company");
                    $username = $this->input->post("username");
                    $role_id  = $this->input->post("role_id");
                    $status   = $this->input->post("status");
                    $apnx_id  = $this->input->post("apnx_id");

                    $update_params = [
                        "name"=>$name,
                        "email"=>$email,
                        "company"=>$company,
                        "username"=>$username,
                        "role_id"=>$role_id,
                        "status"=>$status,
                        "apnx_id"=>$apnx_id
                    ];

                    $result = "";
                    $errors = [];
                    $target_user = $this->m_users->getBy(["id"=>$user_id]);
                    $me_is_root = false;
                    $target_is_root = false;

                    // Check if user id exists.
                    if (count($target_user) > 0)
                    {
                        
                        // Determine if currently logged user is root.
                        if(in_array("all", $user_privileges)) $me_is_root = true;

                        // Determine if target user is root.
                        if($target_user[0]['privileges']=="all") $target_is_root = true;

                        // Check if target account is not root level.
                        if (!$target_is_root)
                        {
                            // Check if username belongs to another user.
                            $username_result = $this->m_users->getBy(["username"=>$username]);
                            if (count($username_result) == 1)
                            {
                                if ($user_id != $username_result[0]['user_id'])
                                {
                                    $errors[] = ["status"=>"error","code"=>"invalid","message"=>"Username is already in use.","data"=>""];
                                }
                            }

                            // Check if email belongs to another user.
                            $email_result = $this->m_users->getBy(["email"=>$email]);
                            if (count($email_result) == 1)
                            {
                                if ($user_id != $email_result[0]['user_id'])
                                {
                                    $errors[] = ["status"=>"error","code"=>"invalid","message"=>"Email is already in use.","data"=>""];
                                }
                            }

                            // Prevent logged account to promote user to root if root privilege is not present.
                            $role_id_result = $this->m_users->getRolesBy(["id"=>$role_id]);
                            $role_id_result = $role_id_result[0];
                            if ($role_id_result['privileges'] == "all")
                            {
                                if (!$me_is_root)
                                {
                                    $errors[] = ["status"=>"error","code"=>"restricted","message"=>"Permision denied.","data"=>""];
                                }
                            }
                        }
                        else
                        {
                            // Grant permission to edit root target if logged user is also root.
                            if($me_is_root)
                            {
                                // Check if username belongs to another user.
                                $username_result = $this->m_users->getBy(["username"=>$username]);
                                if (count($username_result) == 1)
                                {
                                    if ($user_id != $username_result[0]['user_id'])
                                    {
                                        $errors[] = ["status"=>"error","code"=>"invalid","message"=>"Username is already in use.","data"=>""];
                                    }
                                }

                                // Check if email belongs to another user.
                                $email_result = $this->m_users->getBy(["email"=>$email]);
                                if (count($email_result) == 1)
                                {
                                    if ($user_id != $email_result[0]['user_id'])
                                    {
                                        $errors[] = ["status"=>"error","code"=>"invalid","message"=>"Email is already in use.","data"=>""];
                                    }
                                }
                            }
                            else
                            {
                                $errors[] = ["status"=>"error","code"=>"restricted","message"=>"Permision denied.","data"=>""];
                            }
                        }
                    }
                    else
                    {
                        $errors[] = ["status"=>"error","code"=>"invalid","message"=>"User does not exist.","data"=>""];
                    }

                    // Process result output.
                    if(count($errors) == 0)
                    {
                        if ($this->m_users->update($update_params, $user_id))
                        {
                            $result = ["status"=>"ok","code"=>"valid","message"=>"User updated.","data"=>$this->m_users->getAll()];
                        }
                        else
                        {
                            $result = ["status"=>"error","code"=>"invalid","message"=>"Update process failed.","data"=>""];
                        }
                    }
                    else
                    {
                        $result = $errors[0];
                    }

                    header("Content-Type: application/json");
                    echo json_encode($result);
                }
            }

            if ($task == "delete")
            {
                $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

                if (in_array("users_delete",$user_privileges) || in_array("all",$user_privileges))
                {
                    $id = $this->input->post("id");
                    $errors = [];

                    if ($id)
                    {
                        if (gettype($id) == "array")
                        {
                            // Batch delete here.
                        }
                        else
                        {
                            // Verify the user existed.
                            $get_user_result = $this->m_users->getBy(["id"=>$id]);

                            if (count($get_user_result) == 1)
                            {
                                $target_user = $get_user_result[0];
                                $target_is_root = false;
                                $me_is_root = false;
                                $affected_rows = 0;

                                // Prevent deleting own account.
                                if ($_SESSION['userdata']['user_id'] == $target_user['user_id'])
                                {
                                    $errors[] = [
                                        "status" => "error",
                                        "code" => "invalid",
                                        "message" => "Deleting own account is not allowed.",
                                        "data" => ""
                                    ];
                                }
                                else
                                {
                                    if ($target_user['privileges']=="all") $target_is_root = true;
                                    if (in_array("all", $user_privileges)) $me_is_root = true;

                                    // Check if target is root.
                                    if ($target_is_root)
                                    {
                                        // If logged user is root, proceed to delete.
                                        if ($me_is_root)
                                        {
                                            $affected = $this->m_users->delete($id);

                                            if (!$affected)
                                            {
                                                $errors[] = [
                                                    "status" => "error",
                                                    "code" => "db",
                                                    "message" => "Delete from db failed.",
                                                    "data" => ""
                                                ];
                                            }
                                        }
                                        else
                                        {
                                            $errors[] = [
                                                "status" => "error",
                                                "code" => "restricted",
                                                "message" => "Permision denied.",
                                                "data" => ""
                                            ];
                                        }
                                    }
                                    else
                                    {
                                        $affected_rows = $this->m_users->delete($id);
                                        if (!$affected_rows)
                                        {
                                            $errors[] = [
                                                "status" => "error",
                                                "code" => "db",
                                                "message" => "Delete from db failed.",
                                                "data" => ""
                                            ];
                                        }
                                    }
                                }
                            }
                            else
                            {
                                $errors[] = [
                                    "status" => "error",
                                    "code" => "not_found",
                                    "message" => "User does not exist.",
                                    "data" => ""
                                ];
                            }
                        }
                    }
                    else
                    {
                        $errors[] = [
                            "status" => "error",
                            "code" => "error",
                            "message" => "The id is not present.",
                            "data" => ""
                        ];
                    }
                    
                    // Finalize output.
                    if(count($errors) == 0)
                    {
                        $response = [
                            "status" => "ok",
                            "code" => "success",
                            "message" => "Deleted ".$affected_rows." user(s).",
                            "data" => $this->m_users->getAll()
                        ];
                    }
                    else
                    {
                        $response = $errors[0];
                    }

                    // Return an output.
                    header("Content-Type: application/json");
                    echo json_encode($response);
                }
            }

            if ($task == "signin")
            {
                $username = $this->input->post("username");
                $password = $this->input->post("password");
                $remember = $this->input->post("remember");
                if ($username && $password)
                {
                    if ($remember)
                    {
                        $signin_result = $this->auth->signin($username, $password, $remember);
                    }
                    else
                    {
                        $signin_result = $this->auth->signin($username, $password);
                    }
                    header("Content-Type: application/json");
                    echo json_encode($signin_result);
                }
                else
                {
                    echo "No user or pass.";
                }
            }

            if ($task == "change_my_pw")
            {
                $user_id = $this->input->post("user_id");
                $opassword = $this->input->post("opassword");
                $npassword = $this->input->post("npassword");
                $rpassword = $this->input->post("rpassword");

                if ($user_id && $opassword && $npassword && $rpassword)
                {
                    $errors = [];
                    $get_user = $this->m_users->getSesInfoBy(["id"=>$user_id]);

                    // Make sure user exist.
                    if (!$get_user)
                    {
                        $errors[] = ["status"=>"error","code"=>"not_found","message"=>"User does not exist."];
                    }
                    else
                    {
                        $userdata = $get_user[0];
                        $opassword = $this->auth->hash($opassword, $userdata['username']);

                        if ($opassword != $userdata['password'])
                        {
                            $errors[] = ["status"=>"error","code"=>"not_found","message"=>"Old password is wrong."];
                        }
                        elseif (strlen($npassword) < 6)
                        {
                            $errors[] = ["status"=>"error","code"=>"invalid","message"=>"New password is too short."];
                        }
                        elseif ($npassword != $rpassword)
                        {
                            $errors[] = ["status"=>"error","code"=>"invalid","message"=>"Password did not match."];
                        }
                        else
                        {
                            $npassword = $this->auth->hash($npassword, $userdata['username']);

                            if ($this->m_users->update(["password"=>$npassword], $user_id))
                            {
                                $response = ["status"=>"ok","code"=>"success","message"=>"New password saved."];
                            }
                            else
                            {
                                $errors[] = ["status"=>"error","code"=>"db","message"=>"Database update failed."];
                            }
                        }

                    }

                    if (count($errors) > 0)
                    {
                        $response = $errors[0];
                    }

                    header("Content-Type: application/json");
                    echo json_encode($response);
                }
                else
                {
                    header("Content-Type: application/json");
                    echo json_encode([]);
                }
            }

            if ($task == "reset_pw")
            {
                $email = $this->input->post("email");

                if ($email)
                {
                    $result = $this->m_users->getBy(["email"=>$email]);

                    if (count($result) == 1)
                    {
                        $userdata = $result[0];

                        if ($userdata['status'] == "active")
                        {
                            $token = md5(time().microtime());
                            $token_time = time()+$this->config->item("user_token_time");
                            $update_params = [
                                "token"=>$token,
                                "token_time"=>$token_time
                            ];

                            if ($this->m_users->update($update_params, $userdata['user_id']))
                            {
                                $reset_link = base_url("users/reset/{$token}");
                                $first_name = explode(' ', $userdata['name'])[0];
                                $message = $this->load->view("etc/v_password_reset_email", ["name"=>$first_name,"reset_link"=>$reset_link], true);
                                $subject = "Reset your password";
                                $from = "From: ".$this->config->item("system_email");
                                
                                mail($userdata['email'], $subject, $message, $from);
                                $response = array("status"=>"ok","code"=>"active","message"=>"Please check your email.", "data"=>$userdata['email']);
                            }
                            else
                            {
                                $response = array("status"=>"error","code"=>"db","message"=>"Token update failed.");
                            }
                        }
                        elseif ($userdata['status'] == "inactive")
                        {
                            $response = array("status"=>"error","code"=>"inactive","message"=>"Account is inactive.");
                        }
                        if ($response)
                        {
                            header("Content-Type: application/json");
                            echo json_encode($response);
                        }
                    }
                    else
                    {
                        $response = array("status"=>"error","code"=>"not_found","message"=>"Unauthorized access.");
                        header("Content-Type: application/json");
                        echo json_encode($response);
                    }
                }
            }
        }
        elseif($_SERVER['REQUEST_METHOD'] == "POST")
        {
            $input = file_get_contents('php://input');
            $request = json_decode($input, true);
            $response = [
                "status" => "error",
                "code" => null,
                "message" => "Invalid syntax.",
                "data" => null,
                "debug_info" => [
                    "date" => date($this->config->item('log_date_format'),time())
                ]
            ];

            if (isset($request['auth']))
            {
                if (isset($request['auth']['token']))
                {
                    $result = $this->m_users->getBy(['api_token'=>$request['auth']['token']]);
                    if (count($result) > 0)
                    {
                        $data = $result[0];
                        if (time() > $data['api_time'])
                        {
                            $response['message'] = "Token has expired.";
                        }
                        else
                        {
                            $response['status'] = "ok";
                            $response['message'] = "Token is active.";
                            $response['data'][]['accounts'] = trim($data['apnx_id']);
                            $response['debug_info']['seconds_to_expire'] = $data['api_time'] - time();
                        }
                        $response['debug_info']['items_found'] = count($result);
                    }
                    else
                    {
                        $response['message'] = "Invalid token.";
                    }
                }
                elseif (isset($request['auth']['username'],$request['auth']['password']))
                {
                    $result = $this->auth->signin($request['auth']['username'],$request['auth']['password']);
                    
                    if ($result['status'] == "ok")
                    {
                        $response['status'] = "ok";
                        $response['message'] = $result['message'];
                        $response['data'][]['token'] = $result['data'];
                    }
                    elseif ($result['status'] == "error")
                    {
                        $response['status'] == "error";
                        $response['message'] = $result['message'];
                    }
                }
            }

            header("Content-Type: json/application");
            echo json_encode($response);
        }
        else
        {
            $this->auth->limit();
            $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

            // Initialize placeholders.
            $v_main_layout['contents'] = "";
            $v_main_layout['extras']  = "";

            // Navbar Side Contents
            $v_main_layout['nav_header'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_header", "", true);
            $v_main_layout['nav_menus'] = $this->load->view("theme/inspinia/navbar_static_side/v_nav_menus", ["user_privileges"=>$user_privileges], true);

            // Navbar Top Contents
            $v_main_layout['nav_logout_button'] = $this->load->view("theme/inspinia/navbar_static_top/v_logout_button", "", true);

            // Page Heading
            $v_page_info['title'] = "Registered Users";
            $v_page_info['breadcrumbs'] = array('Home' => base_url(),'Users'=>'');
            $v_main_layout['page_info'] = $this->load->view("theme/inspinia/page_heading/v_page_info", $v_page_info, true);
            $v_main_layout['action_area'] = $this->load->view("theme/inspinia/page_heading/v_action_buttons", ["user_privileges"=>$user_privileges], true);

            if (in_array("users_view",$user_privileges) || in_array("all",$user_privileges))
            {
                // Content Priviledged
                $users_table['users'] = $this->m_users->getAll();
                $v_main_layout['contents'] .= $this->load->view("theme/inspinia/content/v_table_users", $users_table, true);
                
                // Extras Priviledged
                $users_modal['roles'] = $this->m_users->getRoles();
                $users_modal['user_privileges'] = $user_privileges;
                $v_main_layout['extras'] .= $this->load->view("theme/inspinia/extras/v_modal_user_new", $users_modal, true);
                $v_main_layout['extras'] .= $this->load->view("theme/inspinia/extras/v_modal_user_edit", $users_modal, true);
                $v_main_layout['extras'] .= $this->load->view("theme/inspinia/extras/v_modal_user_view", $users_modal, true);
            }

            // Extras Common
            $v_main_layout['extras'] .= $this->load->view("theme/inspinia/extras/v_modal_confirm", "", true);

            $this->load->view("theme/inspinia/v_main_layout", $v_main_layout);
        }
    }
    public function sign_out()
    {
        unset($_COOKIE['sid'],$_COOKIE['authorization']);
        setcookie('sid', null, -1, '/');
        setcookie('Authorization', null, -1, '/');
        session_destroy();
        header("Location: ".base_url("portal"));
    }
    public function reset($token=null)
    {
        if($token)
        {
            $token_result = $this->m_users->getBy(["token"=>$token]);

            if (count($token_result) == 1)
            {
                $userdata = $token_result[0];

                if ($userdata['token_time'] < time())
                {
                    $data['short_title'] = '<i class="fa fa-exclamation-circle"></i>';
                    $data['content'] = '<h3>Token has expired.</h3>';
                    $data['short_footnote'] = '';
                    $this->load->view("theme/inspinia/v_portal_layout", $data);
                }
                else
                {
                    $data['short_title'] = "rtb";
                    $data['content'] = $this->load->view("theme/inspinia/portal/v_new_password", ["user_id"=>$userdata['user_id']], true);
                    $data['short_footnote'] = 'rtb.cat &copy; 2016';
                    $this->load->view("theme/inspinia/v_portal_layout", $data);
                }
            }
            else
            {
                show_404();
            }
        }
        else
        {
            $task = $this->input->post("task");

            if($task && $task == "update_pw")
            {
                $user_id = $this->input->post("user_id");
                $npassword = $this->input->post("npassword");
                $rpassword = $this->input->post("rpassword");

                if ($npassword && $rpassword && $user_id)
                {
                    $get_user = $this->m_users->getBy(["id"=>$user_id]);

                    if(count($get_user) == 1)
                    {
                        $userdata = $get_user[0];

                        if (strlen(trim($npassword)) < 4)
                        {
                            $response = ["status"=>"error","code"=>"invalid","message"=>"Password is too short.","data"=>""];
                        }
                        elseif ($npassword != $rpassword)
                        {
                            $response = ["status"=>"error","code"=>"invalid","message"=>"Password did not match.","data"=>""];
                        }
                        else
                        {
                            $update_params = [
                                "password"=>$this->auth->hash($npassword, $userdata['username']),
                                "token"=>"",
                                "token_time"=>""
                            ];

                            if ($this->m_users->update($update_params, $user_id))
                            {
                                $response = ["status"=>"ok","code"=>"success","message"=>"New password saved.","data"=>""];
                            }
                            else
                            {
                                $response = ["status"=>"error","code"=>"db","message"=>"Password update failed.","data"=>""];
                            }
                        }
                    }
                    else
                    {
                        $response = ["status"=>"error","code"=>"not_found","message"=>"Use does not exist.","data"=>""];
                    }

                    header("Content-Type: application/json");
                    echo json_encode($response);
                }
            }
            else
            {
                show_404();
            }
        }
    }
    public function json($method = null) {
        // Privileges
        $user_privileges = explode(',', @$_SESSION['userdata']['privileges']);

        if (in_array("users_view",$user_privileges) || in_array("all",$user_privileges))
        {
            if($method == "get_all")
            {
                header("Content-Type: application/json");
                echo $this->m_users->getAll(true);
            }
            elseif($method == "get_by_id")
            {
                $id = $this->input->get('id');
                if(is_numeric($id))
                {
                    $param = ['id'=>$id];
                    $user_data = $this->m_users->getBy($param);
                    if ($user_data)
                    {
                        $user_data[0]['reset_link'] = "";
                        if ($user_data[0]['token'] != "") $user_data[0]['reset_link'] = base_url("users/reset/".$user_data[0]['token']);
                        
                        header("Content-Type: application/json");
                        echo json_encode($user_data);
                    }
                    else
                    {
                        header("Content-Type: application/json");
                        echo json_encode([]);
                    }
                }
            }
        }
    }
    
}