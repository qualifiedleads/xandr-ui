<div class="modal fade inmodal" id="view_user_modal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="static">
                                <div class="modal-dialog modal-md">
                                    <form id="new_user_form" class="form-custom" method="post">
                                    <input type="hidden" name="task" value="" />
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                                            <h4 class="modal-title">User Details</h4>
                                        </div>
                                        <div class="modal-body">
                                            <table class="table modal-table" align="center">
                                                <tbody>
                                                    <tr>
                                                        <td><label>ID</label></td>
                                                        <td class="value-cell" data-rel="id"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Name</label></td>
                                                        <td class="value-cell" data-rel="name"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Username</label></td>
                                                        <td class="value-cell" data-rel="username"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Role</label></td>
                                                        <td class="value-cell" data-rel="role"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Email</label></td>
                                                        <td class="value-cell" data-rel="email"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Company</label></td>
                                                        <td class="value-cell" data-rel="company"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>APNX ID</label></td>
                                                        <td class="value-cell" data-rel="apnx_id"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Status</label></td>
                                                        <td class="value-cell" data-rel="status"></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Reset Link</label></td>
                                                        <td>
                                                            <input type="text" data-rel="reset" />
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-whitesubmit" data-dismiss="modal"><span class="fa fa-spinner rotating"></span> Close</button>
                                        </div>
                                    </div>
                                    </form>
                                </div>
                            </div>
                            <script>
                                $(document).ready(function(){
                                    $("#new_user_form").paminta(users.add);
                                })
                            </script>