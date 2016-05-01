<h2><?php echo @$title;?></h2><?php
                if(@$breadcrumbs):?>
                    <ol class="breadcrumb">
                    <?php foreach ($breadcrumbs as $name=>$link):?>
                        <li>
                            <a href="<?php echo $link;?>"><?php echo ucfirst($name);?></a>
                        </li>
                    <?php endforeach;?>
                    </ol><?php endif;?>
                    