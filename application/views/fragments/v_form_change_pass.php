<form id="change_pass_form" method="post" action="<?php echo "sessions/change_pass/".$token; ?>">
                        <input type="hidden" name="task" value="change_pass" />
                        <h1>Change Password</h1>
                        <div class="form-group has-feedback">
                            <input type="password" name="npassword" class="form-control has-feedback-left" placeholder="New password">
                            <span class="fa fa-key form-control-feedback left" aria-hidden="true"></span>
                        </div>
                        <div class="form-group has-feedback">
                            <input type="password" name="rpassword" class="form-control has-feedback-left" placeholder="Retype password">
                            <span class="fa fa-unlock form-control-feedback left" aria-hidden="true"></span>
                        </div>
                        <div class="message_box"></div>
                        <div class="message_template" style="display: none">
                            <div class="alert alert-danger alert-dismissible fade in">
                                <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">x</span></button>
                                <span class="message"></span>
                            </div>
                            <div class="alert alert-success alert-dismissible fade in">
                                <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">x</span></button>
                                <span class="message"></span>
                            </div>
                        </div>
                        <div class="button-block">
                            <a class="btn btn-default" id="change_pass_button"><span class="fa fa-spinner fa-spin"></span>Change Now</a>
                        </div>
                        <div class="clearfix"></div>
                        <div class="separator">

                            <p class="change_link">Already a member ?
                                <a id="tologin" href="#tologin"> Log in </a>
                            </p>
                            <div class="clearfix"></div>
                            <br />
                            <div>
                                <p>©2016 RTB.cat</p>
                            </div>
                        </div>
                    </form>
