<link href="theme/inspinia/css/plugins/footable/footable.core.css" rel="stylesheet">
                        <div class="ibox-content">
                            <input type="text" class="form-control input-sm m-b-xs" id="filter"
                                   placeholder="Search in table">

                            <table id="users_table" class="table table-stripped" data-page-size="10" data-filter=#filter>
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Role</th>
                                        <th>Username</th>
                                        <th>Email</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                        <!--<th data-hide="phone,tablet"></th>-->
                                    </tr>
                                </thead>
                                <tbody>
                                    
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <td colspan="6">
                                            <ul class="pagination pull-right"></ul>
                                        </td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                        <!-- FooTable -->
                        <script src="<?php echo base_url('theme/inspinia/js/plugins/footable/footable.all.min.js');?>"></script>
                        <!-- Page-Level Scripts -->
                        <script>
                            $(document).ready(function() {
                                users.updateTable();
                            });
                        </script>
