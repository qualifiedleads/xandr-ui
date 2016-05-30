
<div class="ibox">
    <div class="ibox-content">
        <div class="home-stats">
            <div class="row">
                <div class="col-lg-5">
                    <div class="row">
                        <div class="col-lg-12">
                            <canvas id="lineChart" height="150"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3">
                    <div class="row" style="margin-left: 10px;">
                        <div class="col-lg-6">
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    Impressions
                                </label>
                            </div>
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    CPA
                                </label>
                            </div>
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    CPC
                                </label>
                            </div>
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    CPM
                                </label>
                            </div>
                        </div>
                        <div class="col-lg-6">
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    Clicks
                                </label>
                            </div>
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    Conversions
                                </label>
                            </div>
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    CTR
                                </label>
                            </div>
                            <div class="checkbox">
                                <input id="checkbox1" type="checkbox">
                                <label for="checkbox1">
                                    Media Spend
                                </label>
                            </div>
                        </div>

                    </div>

                </div>
                <div class="col-lg-4">
                    <div id="world-map" style="height: 200px;"></div>
                </div>
            </div>
        </div>

    </div>
</div>
<div class="ibox">
    <div class="ibox-content">
        <div class="home-campaigns">
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    <div id="range_slider"></div>
                </div>
            </div>
            <br>
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    <table class="table table-striped table-condensed">
                        <thead>
                        <tr>
                            <th></th>
                            <th>Spend</th>
                            <th>Conv.</th>
                            <th>Imp</th>
                            <th>Clicks</th>
                            <th>CPC avg.</th>
                            <th>CPM avg.</th>
                            <th>CVR avg.</th>
                            <th>CTR avg.</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td><strong>Totals</strong></td>
                            <td>$1710</td>
                            <td>13</td>
                            <td>3.2M</td>
                            <td>2769</td>
                            <td>$1.15</td>
                            <td>$1.57</td>
                            <td>0.9%</td>
                            <td>0.4%</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <table id="data-home" class="table table-striped">
                    <thead>
                    <tr>
                        <th>Line Item</th>
                        <th>Campaigns</th>
                        <th>Spend</th>
                        <th>Conv.</th>
                        <th>Imp</th>
                        <th>Clicks</th>
                        <th>CPC</th>
                        <th>CPM</th>
                        <th>CVR</th>
                        <th>CTR</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td width="1%">1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td width="30%">
                            <div>
                                <canvas id="lineChart2" height="200"></canvas>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</div>


<script src="<?php echo base_url('theme/inspinia/js/plugins/nouslider/jquery.nouislider.min.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/dataTables/datatables.min.js'); ?>"></script>

<!-- Flot -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.tooltip.min.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.spline.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.resize.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.pie.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.symbol.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.time.js'); ?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/curvedLines.js'); ?>"></script>

<!-- Peity -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/peity/jquery.peity.min.js'); ?>"></script>

<!-- jQuery UI -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/jquery-ui/jquery-ui.min.js'); ?>"></script>

<!-- Jvectormap -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/jvectormap/jquery-jvectormap-2.0.2.min.js'); ?>"></script>
<script
    src="<?php echo base_url('theme/inspinia/js/plugins/jvectormap/jquery-jvectormap-us-aea.js'); ?>"></script>

<!-- EayPIE -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/easypiechart/jquery.easypiechart.js'); ?>"></script>

<!-- Sparkline -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/sparkline/jquery.sparkline.min.js'); ?>"></script>

<!-- ChartJS-->
<script src="<?php echo base_url('theme/inspinia/js/plugins/chartJs/Chart.min.js'); ?>"></script>

<script>

    $(document).ready(function () {
        // Table
        $('#data-home').DataTable({
            dom: '<"html5buttons"B>lTfgitp',
            buttons: [
                {
                    text: 'Active',
                    action: function (e, dt, node, config) {
                        alert("TODO");
                    }
                }, {
                    text: 'Inactive',
                    action: function (e, dt, node, config) {
                        alert("TODO");
                    }
                }, {
                    text: 'All',
                    action: function (e, dt, node, config) {
                        alert("TODO");
                    }
                }, {
                    text: 'Filter',
                    action: function (e, dt, node, config) {
                        alert("TODO");
                    }
                },
            ]

        });


        // Stats
        var lineData = {
            labels: ["", "", "", "", "", "", ""],
            datasets: [
                {
                    label: "Example dataset",
                    fillColor: "rgba(220,220,220,0.5)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: [65, 59, 80, 81, 56, 55, 40]
                },
                {
                    label: "Example dataset",
                    fillColor: "rgba(26,179,148,0.5)",
                    strokeColor: "rgba(26,179,148,0.7)",
                    pointColor: "rgba(26,179,148,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(26,179,148,1)",
                    data: [28, 48, 40, 19, 86, 27, 90]
                }
            ]
        };

        var lineOptions = {
            scaleShowGridLines: true,
            scaleGridLineColor: "rgba(0,0,0,.05)",
            scaleGridLineWidth: 1,
            bezierCurve: true,
            bezierCurveTension: 0.4,
            pointDot: true,
            pointDotRadius: 4,
            pointDotStrokeWidth: 1,
            pointHitDetectionRadius: 20,
            datasetStroke: true,
            datasetStrokeWidth: 2,
            datasetFill: true,
            responsive: true,
            scaleShowLabels: false
        };

        var lineOptions2 = {
            scaleShowGridLines: false,
            scaleGridLineColor: "rgba(0,0,0,.05)",
            scaleGridLineWidth: 1,
            bezierCurve: true,
            bezierCurveTension: 0.4,
            pointDot: true,
            pointDotRadius: 4,
            pointDotStrokeWidth: 1,
            pointHitDetectionRadius: 20,
            datasetStroke: true,
            datasetStrokeWidth: 2,
            datasetFill: true,
            responsive: true,
            scaleShowLabels: false
        };


        var ctx = document.getElementById("lineChart").getContext("2d");
        var myNewChart = new Chart(ctx).Line(lineData, lineOptions);

        var ctx2 = document.getElementById("lineChart2").getContext("2d");
        var myNewChart2 = new Chart(ctx2).Line(lineData, lineOptions2);

        // Map Area
        var mapData = {
            "US-VA": 298,
        };

        $('#world-map').vectorMap({
            map: 'us_aea',
            backgroundColor: "white",
            zoomButtons: false,
            regionStyle: {
                initial: {
                    fill: '#e4e4e4',
                    "fill-opacity": 0.9,
                    stroke: 'none',
                    "stroke-width": 0,
                    "stroke-opacity": 0
                }
            },
            series: {
                regions: [{
                    values: mapData,
                    scale: ["#1ab394", "#22d6b1"],
                    normalizeFunction: 'polynomial'
                }]
            }
        });

        // Range Slider
        $("#range_slider").noUiSlider({
            start: [7, 14],
            behaviour: 'drag',
            connect: true,
            range: {
                'min': 1,
                'max': 31
            }
        });
    });
</script>
