<li class="nav-header">
                        <div class="dropdown profile-element"> <span>
                                <!--<img alt="image" class="img-circle" src="img/profile_small_1.png" />-->
                                 </span>
                            <a data-toggle="dropdown" class="dropdown-toggle" href="#">
                                <span class="clear">
                                    <span class="block m-t-xs">
                                        <strong class="font-bold"><?php echo ucfirst($_SESSION['userdata']['name']);?></strong>
                                    </span>
                                    <span class="text-muted text-xs block"><?php echo ucfirst($_SESSION['userdata']['role_name']);?> <b class="caret"></b></span>
                                </span>
                            </a>
                            <ul class="dropdown-menu animated fadeInRight m-t-xs">
                                <li><a>Change Password</a></li>
                                <li class="divider"></li>
                                <li><a href="<?php echo base_url('users/sign_out');?>">Logout</a></li>
                            </ul>
                        </div>
                        <div class="logo-element">
                            rtb
                        </div>
                    </li>