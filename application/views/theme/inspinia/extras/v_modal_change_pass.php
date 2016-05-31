<div class="modal fade inmodal" id="change_pass_modal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="static">
                                <div class="modal-dialog modal-sm">
                                    <form id="change_pass_form" class="form-custom" method="post">
                                        <input type="hidden" name="task" value="change_my_pw" />
                                        <input type="hidden" name="user_id" value="<?php echo @$_SESSION['userdata']['user_id'];?>" />
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                                                <h4 class="modal-title">Change Password</h4>
                                            </div>
                                            <div class="modal-body">
                                                <table class="modal-table" align="center">
                                                    <tbody>
                                                        <tr>
                                                            <td><input type="password" name="opassword" class="form-control" data-paminta="password" placeholder="Old Password" /></td>
                                                        </tr>
                                                        <tr>
                                                            <td><input type="password" name="npassword" class="form-control" data-paminta="password" placeholder="New Password" /></td>
                                                        </tr>
                                                        <tr>
                                                            <td><input type="password" name="rpassword" class="form-control" data-paminta="password" placeholder="Retype Password" /></td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                
                                            </div>
                                            <div class="modal-footer">
                                                <button type="submit" class="btn btn-primary submit"><span class="fa fa-spinner rotating"></span> Change</button>
                                                <button type="button" class="btn btn-white" data-dismiss="modal">Close</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                            <script>
                                $(document).ready(function(){
                                    $("#change_pass_form").paminta(users.updateMyPass);
                                })
                            </script>