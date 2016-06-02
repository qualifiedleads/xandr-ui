<script>
        function abbreviate(number, maxPlaces, forcePlaces, forceLetter) {
            function annotate(number, maxPlaces, forcePlaces, abbr) {
                // set places to false to not round
                var rounded = 0
                switch(abbr) {
                    case 'T':
                    rounded = number / 1e12
                    break
                    case 'B':
                    rounded = number / 1e9
                    break
                    case 'M':
                    rounded = number / 1e6
                    break
                    case 'K':
                    rounded = number / 1e3
                    break
                    case '':
                    rounded = number
                    break
                }
                if(maxPlaces !== false) {
                    var test = new RegExp('\\.\\d{' + (maxPlaces + 1) + ',}$')
                    if(test.test(('' + rounded))) {
                        rounded = rounded.toFixed(maxPlaces)
                    }
                }
                if(forcePlaces !== false) {
                    rounded = Number(rounded).toFixed(forcePlaces)
                }
                return rounded + abbr
            }
            number = Number(number)
            forceLetter = forceLetter || false
            if(forceLetter !== false) {
            return annotate(number, maxPlaces, forcePlaces, forceLetter)
            }
            var abbr
            if(number >= 1e12) {
                abbr = 'T'
            }
            else if(number >= 1e9) {
                abbr = 'B'
            }
            else if(number >= 1e6) {
                abbr = 'M'
            }
            else if(number >= 1e3) {
                abbr = 'K'
            }
            else {
                abbr = ''
            }
            return annotate(number, maxPlaces, forcePlaces, abbr)
        }

        var dash = {};
        dash.data = [];
        dash.total = {cost:0,conv:0,imps:0,clks:0,cpc:0,cpm:0,cvr:0,ctr:0}
        dash.plots =
        {
            cost : {data: null, hoverable: true, color: '#18A689'},
            conv : {data: null, hoverable: true, color: '#21B9BB'},
            imps : {data: null, hoverable: true, color: '#1C84C6'},
            clks : {data: null, hoverable: true, color: '#533A71'},
            cpc : {data: null, hoverable: true, color: '#F8AC59'},
            cpm : {data: null, hoverable: true, color: '#ED5565'},
            cvr : {data: null, hoverable: true, color: '#50514F'},
            ctr : {data: null, hoverable: true, color: '#843B62'}
        }
        dash.setPlots = function (data)
        {
            var cost=[], conv=[], imps=[], clks=[], cpc=[], cpm=[], cvr=[], ctr=[];
            for (var n in data)
            {
                var t_cost = parseFloat((data[n]).cost);
                var t_conv = parseFloat((data[n]).total_convs);
                var t_imps = parseFloat((data[n]).imps);
                var t_clks = parseFloat((data[n]).clicks);
                var js_time = (data[n]).date * 1000;

                cost.push([js_time,t_cost]);
                conv.push([js_time,t_conv]);
                imps.push([js_time,t_imps]);
                clks.push([js_time,t_clks]);

                var ccpc = parseFloat(t_cost / t_clks);
                var ccpm = parseFloat(t_cost / (t_imps / 1000));
                var ccvr = (t_conv / t_imps) * 100;
                var cctr = (t_clks / t_imps) * 100;

                cpc.push([js_time,ccpc]);
                cpm.push([js_time,ccpm]);
                cvr.push([js_time,ccvr]);
                ctr.push([js_time,cctr]);
                dash.total.cost += t_cost;
                dash.total.conv += t_conv;
                dash.total.imps += t_imps;
                dash.total.clks += t_clks;
            }
            dash.plots.cost.data = cost;
            dash.plots.conv.data = conv;
            dash.plots.imps.data = imps;
            dash.plots.clks.data = clks;
            dash.plots.cpc.data = cpc;
            dash.plots.cpm.data = cpm;
            dash.plots.cvr.data = cvr;
            dash.plots.ctr.data = ctr;
            dash.total.cpc = dash.total.cost / dash.total.clks;
            dash.total.cpm = dash.total.cost / (dash.total.imps / 1000);
            dash.total.cvr = (dash.total.conv / dash.total.imps) * 100;
            dash.total.ctr = (dash.total.clks / dash.total.imps) * 100;
            return true;
        }
        dash.applyDate = function (start_date, end_date)
        {
            var url = "<?php echo base_url('test/get_analytics?columns=imps,clicks,total_convs,cost,date&advertiser_id='.$_SESSION['userdata']['apnx_id']);?>";
                url+= "&start_date="+start_date+"&end_date="+end_date;
            for (var j in dash.total) dash.total[j] = 0;
            for (var k in dash.plots) dash.plots[k].data = null;
            $.ajax({
                method : "GET",
                url : url,
                success : function (response)
                {
                    if (response.status == "ok")
                    {
                        dash.data = response.data;
                        if (dash.setPlots(response.data))
                        {
                            dash.update();
                        }
                        else
                        {
                            console.log("Stalled.");
                        }
                    }
                    else if (response.status == "error")
                    {
                        modals.message(response.message);
                    }    
                }
            });
        }
        dash.update = function ()
        {
            var metrics_1 = $("#graph_metrics_1");
            var metrics_2 = $("#graph_metrics_2");
            var dataset_1, dataset_2;
            
            // Process the two datasets.
            $('#graph_vs_pallet_1').css('background-color',dash.plots[metrics_1.val()].color);
            $('#graph_vs_pallet_2').css('background-color',dash.plots[metrics_2.val()].color);
            dataset_1 = dash.plots[metrics_1.val()];
            dataset_2 = dash.plots[metrics_2.val()];
            dataset_1.yaxis = 1;
            dataset_2.yaxis = 2;
            dataset_2.position = "right";

            var options = {
                xaxes: [{mode: 'time'}],
                yaxes : [
                    {},
                    {alignTicksWithAxis: 1,position: "right"}
                ],
                grid: {
                    color: "#999999",
                    hoverable: true,
                    tickColor: "#D4D4D4",
                    borderWidth:0,
                    hoverable: true //IMPORTANT! this is needed for tooltip to work,
                },
                
                /*
                tooltip: true,
                tooltipOpts: {
                    content: "%s for %x was %y",
                    xDateFormat: "%y-%0m-%0d",
                    onHover: function(flotItem, $tooltipEl) {
                        console.log(flotItem, $tooltipEl);
                    }
                }
                */
            }
            $.plot($('#cumulative_line_chart'),[dataset_1,dataset_2],options);
            dash.init();
        }
        dash.init = function()
        {
            $('#main_graph span.stat-label').each(function()
            {
                var data_for = $(this).attr('data-for');

                $(this).css('background-color', dash.plots[data_for].color)
                .attr('title', dash.total[data_for]);

                if (data_for == "cpc" || data_for == "cpm")
                {
                    $(this).text(dash.total[data_for].toFixed(2)+' USD');
                }
                else if (data_for == "cvr" || data_for == "ctr")
                {
                    $(this).text(dash.total[data_for].toFixed(3)+' %');
                }
                else if (data_for == "cost")
                {
                    $(this).text(abbreviate(dash.total[data_for],2,false,false)+' USD');
                }
                else{
                    $(this).text(abbreviate(dash.total[data_for],2,false,false));
                }
            });
        }
    </script>
