<div class="modal fade inmodal" id="edit_user_modal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="static">
                                <div class="modal-dialog modal-md">
                                    <form id="edit_user_form" class="form-custom" method="post">
                                    <input type="hidden" name="task" value="update" />
                                    <input type="hidden" name="user_id" />
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                                            <h4 class="modal-title">Edit User</h4>
                                        </div>
                                        <div class="modal-body">
                                            <table class="modal-table" align="center">
                                                <tbody>
                                                    <tr>
                                                        <td><label>Name</label></td><td><input type="text" name="name" class="form-control" data-paminta="text" /></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Username</label></td><td><input type="text" name="username" class="form-control" data-paminta="text" /></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Role</label></td>
                                                        <td>
                                                            <select name="role_id" class="form-control">
<?php if(count(@$roles) > 0):?>
    <?php foreach($roles as $role):?>
                                                                <option value="<?php echo $role['role_id'];?>"><?php echo ucfirst($role['role_name']);?></option>
    <?php endforeach;?>
<?php endif;?>
                                                            </select>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Email</label></td><td><input type="text" name="email" class="form-control" data-paminta="email" /></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Company</label></td><td><input type="text" name="company" class="form-control" /></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>APNX ID</label></td><td><input type="text" name="apnx_id" class="form-control" /></td>
                                                    </tr>
                                                    <tr>
                                                        <td><label>Status</label></td>
                                                        <td>
                                                            <div class="radio radio">
                                                                <input type="radio" id="edit_status_active" name="status" value="active" checked="true" /><label for="edit_status_active"> Active</label>
                                                            </div>
                                                            &nbsp;&nbsp;
                                                            <div class="radio">
                                                                <input type="radio" id="edit_status_inactive" name="status" value="inactive" /><label for="edit_status_inactive"> Inactive</label>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            
                                        </div>
                                        <div class="modal-footer">
                                            <button type="submit" class="btn btn-primary submit"><span class="fa fa-spinner rotating"></span> Save</button>
                                            <button type="button" class="btn btn-white" data-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                    </form>
                                </div>
                            </div>
                            <script>
                                $(document).ready(function(){
                                    $("#edit_user_form").paminta(users.update);
                                })
                            </script>