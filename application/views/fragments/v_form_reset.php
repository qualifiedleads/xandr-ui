<form id="reset_form" method="post">
                        <input type="hidden" name="task" value="reset" value="1" />
                        <h1>Reset Password</h1>
                        <div class="form-group has-feedback">
                            <input type="text" name="email" class="form-control has-feedback-left" placeholder="Email">
                            <span class="fa fa-send-o form-control-feedback left" aria-hidden="true"></span>
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
                            <a class="btn btn-default" id="reset_button"><span class="fa fa-spinner fa-spin"></span>Reset Now</a>
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
