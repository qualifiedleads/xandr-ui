<div class="campaigns_tree">

  <div class="ibox-content">
    <div id="jstree1">
      <ul>
        <li class="jstree-open">
            Campaign 1with a really long odd name and many short cuts and abbreviations
            <ul>
                <li data-jstree='"type":"css"}'>Optimiser</li>
                <li data-jstree='"type":"css"}'>Re-Test list</li>
            </ul>
        </li>
        <li>Campaign 2</li>
        <li>Campaign 3</li>
        <li>Campaign 4</li>
        <li>Campaign 5</li>
        <li>Campaign 6</li>
        <li>Campaign 7</li>
        <li>Campaign 8</li>
      </ul>
  
    </div>
  </div>
</div>

<style>
    .jstree-open > .jstree-anchor > .fa-folder:before {
        content: "\f07c";
    }

    .jstree-default .jstree-icon.none {
        width: 0;
    }
</style>

<script>
    $(document).ready(function(){

        $('#jstree1').jstree({
            'core' : {
                'check_callback' : true
            },
            'plugins' : [ 'types', 'dnd' ],
            'types' : {
                'default' : {
                    'icon' : 'fa fa-folder'
                },
                'html' : {
                    'icon' : 'fa fa-file-code-o'
                },
                'svg' : {
                    'icon' : 'fa fa-file-picture-o'
                },
                'css' : {
                    'icon' : 'fa fa-file-code-o'
                },
                'img' : {
                    'icon' : 'fa fa-file-image-o'
                },
                'js' : {
                    'icon' : 'fa fa-file-text-o'
                }

            }
        });

    });
</script>
