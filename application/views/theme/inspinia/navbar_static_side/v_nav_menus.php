<li>
                        <a href="<?php echo base_url();?>"><i class="fa fa-home"></i>
                        <span class="nav-label">Home</span></a>
                    </li><?php if(in_array('users_view', $user_privileges) || in_array('all', $user_privileges)):?><li>
                        <a href="users">
                            <i class="fa fa-users"></i>
                            <span class="nav-label">Users</span>
                        </a>
                    </li>
<?php endif;?>
                    <li>
                        <a href="#"><i class="fa fa-area-chart"></i>
                        <span class="nav-label">Campaigns</span><span class="fa arrow"></span></a>
                        <ul class="nav nav-second-level collapse">
                            <li><a href="campaign_tree">Campaign Tree</a></li>
                            <li><a href="campaign_single">Single</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-line-chart"></i>
                        <span class="nav-label">Optimiser</span></a>
                    </li>
                    <li>
                        <a href="billing"><i class="fa fa-money"></i>
                        <span class="nav-label">Billing</span></a>
                    </li>

