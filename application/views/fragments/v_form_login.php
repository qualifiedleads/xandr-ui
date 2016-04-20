<form id="signin_form" method="post">
                        <input type="hidden" name="task" value="signin" />
                        <h1>Login</h1>
                        <div class="form-group has-feedback">
                            <input type="text" name="username" class="form-control has-feedback-left" placeholder="Username" />
                            <span class="fa fa-user form-control-feedback left" aria-hidden="true"></span>
                        </div>
                        <div class="form-group has-feedback">
                            <input type="password" name="password" class="form-control has-feedback-left" placeholder="Password" />
                            <span class="fa fa-key form-control-feedback left" aria-hidden="true"></span>
                        </div>
                        <div class="message_box"></div>
                        <div class="message_template" style="display: none">
                            <div class="alert alert-success alert-dismissible fade in">
                                <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">x</span></button>
                                <span class="message"></span>
                            </div>
                            <div class="alert alert-danger alert-dismissible fade in">
                                <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">x</span></button>
                                <span class="message"></span>
                            </div>
                        </div>
                        <div class="button-block">
                            <a class="btn btn-default" role="submit" id="signin_button"><span class="fa fa-spinner fa-spin"></span>Log  in</a>
                            <label>
                                <a><input type="checkbox" name="remember" value="1"> Remember</a>
                            </label>
                        </div>
                        <div  class="clearfix"></div>
                        <div  class="separator">
                            <p  class="change_link">
                                <a class="submit" href="#toreset">  Lost your password?  </a>
                            </p>
                            <div  class="clearfix"></div>
                            <br  />
                            <div>
                                <p>©2016  RTB.cat</p>
                            </div>
                        </div>
                    </form>
