<script>
    $(function()
    {
        // Range picker change function.

        function cb (start, end)
        {
            $('#date_range_picker span').html(start.format('MMM DD, YYYY') + ' - ' + end.format('MMM DD, YYYY'));
        }
        function applyDateEvent(start, end, label)
        {
            var s_date = start.format('YYYY-MM-DD');
            var e_date = end.format('YYYY-MM-DD');
            cb(start, end);
            dash.applyDate(s_date, e_date);
        }
        cb(moment(), moment());
        $('#date_range_picker').daterangepicker
        (
            {
                dateLimit: { days: 60 },
                ranges : {
                    'Today': [moment(), moment()],
                    'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                    'Last 7 Days': [moment().subtract(7, 'days'), moment().subtract(1, 'days')],
                    'Last 30 Days': [moment().subtract(30, 'days'), moment().subtract(1, 'days')],
                    'This Month': [moment().startOf('month'), moment().endOf('month')],
                    'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
               },
                "opens": "left"
            }, 
            applyDateEvent
        );
        applyDateEvent(moment(),moment());
    });
    $(function()
    {
        $('#main_graph select.vs-dropdown-metrics').unbind('change').change(
            function()
            {
                var metrics_1 = $('#graph_metrics_1');
                var metrics_2 = $('#graph_metrics_2');
                $('#main_graph option').prop('disabled',false);
                $('#graph_metrics_2 option[value="'+metrics_1.val()+'"]').prop('disabled',true);
                $('#graph_metrics_1 option[value="'+metrics_2.val()+'"]').prop('disabled',true);
                dash.update();
            }
        );
    });
</script>
