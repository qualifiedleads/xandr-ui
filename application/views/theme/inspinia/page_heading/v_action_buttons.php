<?php if(in_array('users_view', $user_privileges) || in_array('all', $user_privileges)):?>
<button class="btn btn-default" onclick="users.new()"><b>+</b> New</button>
<?php endif;?>