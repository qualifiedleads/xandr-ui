<div id="billing_content"></div>
<?php if(!empty(@$_SESSION['userdata']['company'])):?>
<script>
    $(document).ready(function(){

        // Initialize loading content.
        var loader = 
                    '<div class="sk-spinner sk-spinner-wave">'+
                        '<div class="sk-rect1"></div> '+
                        '<div class="sk-rect2"></div> '+
                        '<div class="sk-rect3"></div> '+
                        '<div class="sk-rect4"></div> '+
                        '<div class="sk-rect5"></div>'+
                    '</div>';
        $("#billing_content").html('<div class="ibox float-e-margins"><div class="ibox-content">'+loader+'</div></div>');

        // Table Builder
        var buildTable = function(rows)
        {
            var output  = '<div style="text-align:right;font-size:16px"><b style="display:inline-block;margin:auto 10px 10px auto">'+rows[0][4]+'</b></div>';
                output += '<table class="table table-bordered">';

            for (var n in rows)
            {
                if (n == 1)
                {
                    output +=   '<thead>'+
                                    '<tr>'+
                                        '<th>'+rows[n][0]+'</th>'+
                                        '<th>'+rows[n][1]+'</th>'+
                                        '<th>'+rows[n][2]+'</th>'+
                                        '<th>'+rows[n][3]+'</th>'+
                                        '<th>'+rows[n][4]+'</th>'+
                                    '</tr>'+
                                '</thead>';
                }
                if (n > 1)
                {
                    // NOTE: Refactor; improve number formatting regex in the next update.

                    var amounts = ($.trim(rows[n][2]) != "")? (rows[n][2]).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,') + " USD" : "";
                    var imps = (typeof rows[n][4] == "number")? (String(rows[n][4])).replace(/(\d)(?=(?:\d{3})+\b)/g, '$1,') : rows[n][4];
                    output +=   '<tbody>'+
                                    '<tr>'+
                                        '<td>'+rows[n][0]+'</td>'+
                                        '<td>'+rows[n][1]+'</td>'+
                                        '<td style="text-align:right">'+amounts+'</td>'+
                                        '<td>'+rows[n][3]+'</td>'+
                                        '<td>'+imps+'</td>'+
                                    '</tr>'+
                                '</tbody>';
                }
            }

            output += '</table>';
            return output;
        }
        // Request for billing content.
        $.ajax({
            url : "https://script.google.com/macros/s/AKfycbwPJWzTlqbhcu18qkr6sw3YZTRVXL_qb5xratbCQ_dgHLOThGPT/exec?advertiser_name=<?php echo $_SESSION['userdata']['company'];?>",
            method : "get",
            asynch : true,
            success : function(response)
            {
                if (response.status == "ok")
                {
                    var iboxes = "";
                    for (var n in response.data)
                    {
                        iboxes += '<div class="ibox float-e-margins"><div class="ibox-content">'+buildTable(response.data[n])+'</div></div>';
                    }
                    
                    $("#billing_content").html(iboxes);
                }
                else
                {
                    var notice = '<div class="ibox float-e-margins"><div class="ibox-content"><p style="margin:0">You do not have registered billing account.</p></div></div>';
                    $("#billing_content").html(notice);
                }
            }
        });
    });
</script>
<?php else:?>
<script>
    $(document).ready(function(){
        $notice = '<div class="ibox float-e-margins"><div class="ibox-content"><p style="margin:0">You do not have registered billing account.</p></div></div>'
        $("#billing_content").html($notice);
    });
</script>
<?php endif;?>

