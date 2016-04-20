<div class="row">
    <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
            <div class="x_title">
                <h2>Bar Graph.</h2>
                <div class="clearfix"></div>
            </div>
            <div class="clearfix"></div>
            <div class="x_content">
                <div id="bar_graph" style="width:100%; height:300px;"></div>
            </div>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="x_panel">
            <div class="x_title">
                <h2>Line Graph.</h2>
                <div class="clearfix"></div>
            </div>
            <div class="clearfix"></div>
            <div class="x_content">
                <canvas id="line_graph"></canvas>
            </div>
        </div>
    </div>
</div>
<script src="js/chartjs/chart.min.js"></script>
<script>
    // Line chart
    Chart.defaults.global.elements.line.tension = 0;
    var data = 
        {
            type : "line",
            data : {
                labels: ["January", "February", "March", "April", "May", "June", "July"],
                datasets:
                [{
                    label: "Impressions",
                    backgroundColor: "rgba(38, 185, 154, 0.31)",
                    borderColor: "rgba(38, 185, 154, 0.7)",
                    pointBorderColor: "rgba(38, 185, 154, 0.7)",
                    pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointBorderWidth: 1,
                    data: [31, 74, 6, 39, 20, 85, 7]
                },
                {
                    label: "Cost",
                    backgroundColor: "rgba(3, 88, 106, 0.3)",
                    borderColor: "rgba(3, 88, 106, 0.70)",
                    pointBorderColor: "rgba(3, 88, 106, 0.70)",
                    pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(151,187,205,1)",
                    pointBorderWidth: 1,
                    data: [82, 23, 66, 9, 99, 4, 2]
                }]
            }
        }
    var data2 = 
        {
            type : "line",
            data : {
                labels: ["Enero", "Pebrero", "Marso", "Abril", "Mayo", "Hunyo", "Hulyo"],
                datasets:
                [{
                    label: "Impressions",
                    backgroundColor: "rgba(38, 185, 154, 0.31)",
                    borderColor: "rgba(38, 185, 154, 0.7)",
                    pointBorderColor: "rgba(38, 185, 154, 0.7)",
                    pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointBorderWidth: 1,
                    data: [31, 74, 6, 39, 20, 85, 7]
                },
                {
                    label: "Cost",
                    backgroundColor: "rgba(3, 88, 106, 0.3)",
                    borderColor: "rgba(3, 88, 106, 0.70)",
                    pointBorderColor: "rgba(3, 88, 106, 0.70)",
                    pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(151,187,205,1)",
                    pointBorderWidth: 1,
                    data: [82, 23, 66, 9, 99, 4, 2]
                }]
            }
        }
            
    var lineChart = new Chart($("#line_graph"),data);

</script>