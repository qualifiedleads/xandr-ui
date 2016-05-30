<h2><?php echo @$title;?></h2>
<?php if(@$breadcrumbs):?>
                    <ol class="breadcrumb">
<?php foreach ($breadcrumbs as $name=>$link): if ($link != ""):?>
                        <li>
                            <a href="<?php echo $link;?>"><?php echo ucfirst($name);?></a>
                        </li>
                        <?php else:?>
                        <li class="active">
                            <strong><?php echo ucfirst($name);?></strong>
                        </li>
<?php endif;endforeach;?>
                    </ol>
<?php endif;?>
 