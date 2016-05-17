<div class="row">
    <!-- Left Column -->
    <div class="col-lg-8">
        <!-- Cumulative Stats -->
        <div class="row">
            <div class="col-lg-12">
                <div class="ibox">
                    <div class="ibox-content">
                        <div class="row">
                            <div class="col-lg-12">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flot-dashboard-chart"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Table -->
        <div class="jqGrid_wrapper">
            <table id="table_list_1"></table>
            <div id="pager_list_1"></div>
       </div>
        <!-- <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>Campaign</th>
                    <th>Spend</th>
                    <th>conv.</th>
                    <th>imp</th>
                    <th>clicks</th>
                    <th>cpc</th>
                    <th>cpm</th>
                    <th>CVR</th>
                    <th>CTR</th>
                    <th>
                        Compare
                        <div class="checkbox">
                            <input id="checkbox1" type="checkbox">
                            <label for="checkbox1">
                                <small>Select All</small>
                            </label>
                        </div>
                    </th>
                </tr>
            </thead>
            <tr>
                <td>Campaign 1</td>
                <td>$410</td>
                <td>8</td>
                <td>5500</td>
                <td>21</td>
                <td>$0.31</td>
                <td>$1.38</td>
                <td></td>
                <td></td>
                <td>
                    <div class="checkbox">
                        <input id="checkbox1" type="checkbox">
                        <label for="checkbox1">
                            
                        </label>
                    </div>
                </td>

            </tr>
        </table> -->
    </div>
    <!-- Right Column -->
    <div class="col-lg-4">
        <!-- Active campaigns -->
        <div class="row">
            <div class="col-lg-12">
                <div class="ibox">
                    <div class="ibox-content">
                        <div id="world-map" style="height: 300px;"></div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Filter -->
        <div class="row">
            <div class="col-lg-12">
                <div class="ibox float-e-margins">
                    <div class="ibox-content">
                        <div class="row">
                            <div class="col-lg-6">
                                <div class="checkbox">
                                    <input id="checkbox1" type="checkbox">
                                    <label for="checkbox1">
                                        impressions
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
                                        clicks
                                    </label>
                                </div>
                            </div>
                            <div class="col-lg-6">
                                <div class="checkbox">
                                    <input id="checkbox1" type="checkbox">
                                    <label for="checkbox1">
                                        media spend
                                    </label>
                                </div>
                                <div class="checkbox">
                                    <input id="checkbox1" type="checkbox">
                                    <label for="checkbox1">
                                        conversions
                                    </label>
                                </div>
                                <div class="checkbox">
                                    <input id="checkbox1" type="checkbox">
                                    <label for="checkbox1">
                                        CTR
                                    </label>
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Charts -->
        <div class="row">
            <div class="col-lg-12">
                <div class="ibox float-e-margins">
                    <div class="ibox-content">
                        <div>
                            <div id="lineChart"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-12">
                <div class="ibox float-e-margins">
                    <div class="ibox-content">
                        <div class="text-center">
                            <div id="scatter"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-12">
                <div class="ibox float-e-margins">
                    <div class="ibox-content">
                        <div>
                            <div id="stocked"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<!-- Flot -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.tooltip.min.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.spline.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.resize.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.pie.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.symbol.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/flot/jquery.flot.time.js');?>"></script>

<!-- Peity -->
<!-- Disable if not used. -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/peity/jquery.peity.min.js');?>"></script>
<!-- Causes error because link is broken.
<script src="<?php echo base_url('theme/inspinia/js/demo/peity-demo.js');?>"></script>
-->

<!-- jqGrid -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/jqGrid/i18n/grid.locale-en.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/jqGrid/jquery.jqGrid.min.js');?>"></script>

<!-- d3 and c3 charts -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/d3/d3.min.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/c3/c3.min.js');?>"></script>

<!-- jQuery UI -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/jquery-ui/jquery-ui.min.js');?>"></script>

<!-- Jvectormap -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/jvectormap/jquery-jvectormap-2.0.2.min.js');?>"></script>
<script src="<?php echo base_url('theme/inspinia/js/plugins/jvectormap/jquery-jvectormap-world-mill-en.js');?>"></script>

<!-- EayPIE -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/easypiechart/jquery.easypiechart.js');?>"></script>

<!-- Sparkline -->
<!-- Disable if not used. -->
<script src="<?php echo base_url('theme/inspinia/js/plugins/sparkline/jquery.sparkline.min.js');?>"></script>

<!-- Sparkline demo data  -->
<!-- Causes error because link is broken.
<script src="<?php echo base_url('theme/inspinia/js/demo/sparkline-demo.js');?>"></script>
-->

<!-- Homepage Graphs: TODO: Refactor -->
<script>

    $(document).ready(function () {
        // Map Area
        var mapData = {
            "US": 298,
            "SA": 200,
            "DE": 220,
            "FR": 540,
            "CN": 120,
            "AU": 760,
            "BR": 550,
            "IN": 200,
            "GB": 120,
        };

        $('#world-map').vectorMap({
            map: 'world_mill_en',
            backgroundColor: "transparent",
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
            },
        });

        // Header table

        var data2 = [
            [gd(2012, 1, 1), 7], [gd(2012, 1, 2), 6], [gd(2012, 1, 3), 4], [gd(2012, 1, 4), 8],
            [gd(2012, 1, 5), 9], [gd(2012, 1, 6), 7], [gd(2012, 1, 7), 5], [gd(2012, 1, 8), 4],
            [gd(2012, 1, 9), 7], [gd(2012, 1, 10), 8], [gd(2012, 1, 11), 9], [gd(2012, 1, 12), 6],
            [gd(2012, 1, 13), 4], [gd(2012, 1, 14), 5], [gd(2012, 1, 15), 11], [gd(2012, 1, 16), 8],
            [gd(2012, 1, 17), 8], [gd(2012, 1, 18), 11], [gd(2012, 1, 19), 11], [gd(2012, 1, 20), 6],
            [gd(2012, 1, 21), 6], [gd(2012, 1, 22), 8], [gd(2012, 1, 23), 11], [gd(2012, 1, 24), 13],
            [gd(2012, 1, 25), 7], [gd(2012, 1, 26), 9], [gd(2012, 1, 27), 9], [gd(2012, 1, 28), 8],
            [gd(2012, 1, 29), 5], [gd(2012, 1, 30), 8], [gd(2012, 1, 31), 25]
        ];

        var data3 = [
            [gd(2012, 1, 1), 800], [gd(2012, 1, 2), 500], [gd(2012, 1, 3), 600], [gd(2012, 1, 4), 700],
            [gd(2012, 1, 5), 500], [gd(2012, 1, 6), 456], [gd(2012, 1, 7), 800], [gd(2012, 1, 8), 589],
            [gd(2012, 1, 9), 467], [gd(2012, 1, 10), 876], [gd(2012, 1, 11), 689], [gd(2012, 1, 12), 700],
            [gd(2012, 1, 13), 500], [gd(2012, 1, 14), 600], [gd(2012, 1, 15), 700], [gd(2012, 1, 16), 786],
            [gd(2012, 1, 17), 345], [gd(2012, 1, 18), 888], [gd(2012, 1, 19), 888], [gd(2012, 1, 20), 888],
            [gd(2012, 1, 21), 987], [gd(2012, 1, 22), 444], [gd(2012, 1, 23), 999], [gd(2012, 1, 24), 567],
            [gd(2012, 1, 25), 786], [gd(2012, 1, 26), 666], [gd(2012, 1, 27), 888], [gd(2012, 1, 28), 900],
            [gd(2012, 1, 29), 178], [gd(2012, 1, 30), 555], [gd(2012, 1, 31), 993]
        ];

        var dataset = [
            {
                label: "Number of orders",
                data: data3,
                color: "#1ab394",
                bars: {
                    show: true,
                    align: "center",
                    barWidth: 24 * 60 * 60 * 600,
                    lineWidth:0
                }

            }, {
                label: "Payments",
                data: data2,
                yaxis: 2,
                color: "#1C84C6",
                lines: {
                    lineWidth:1,
                        show: true,
                        fill: true,
                    fillColor: {
                        colors: [{
                            opacity: 0.2
                        }, {
                            opacity: 0.4
                        }]
                    }
                },
                splines: {
                    show: false,
                    tension: 0.6,
                    lineWidth: 1,
                    fill: 0.1
                },
            }
        ];


        var options = {
            xaxis: {
                mode: "time",
                tickSize: [3, "day"],
                tickLength: 0,
                axisLabel: "Date",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Arial',
                axisLabelPadding: 10,
                color: "#d5d5d5"
            },
            yaxes: [{
                position: "left",
                max: 1070,
                color: "#d5d5d5",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Arial',
                axisLabelPadding: 3
            }, {
                position: "right",
                clolor: "#d5d5d5",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: ' Arial',
                axisLabelPadding: 67
            }
            ],
            legend: {
                noColumns: 1,
                labelBoxBorderColor: "#000000",
                position: "nw"
            },
            grid: {
                hoverable: false,
                borderWidth: 0
            }
        };

        function gd(year, month, day) {
            return new Date(year, month - 1, day).getTime();
        }

        var previousPoint = null, previousLabel = null;

        $.plot($("#flot-dashboard-chart"), dataset, options);

        c3.generate({
            bindto: '#lineChart',
            data:{
                columns: [
                    ['data1', 30, 200, 100, 400, 150, 250],
                    ['data2', 50, 20, 10, 40, 15, 25]
                ],
                colors:{
                    data1: '#1ab394',
                    data2: '#BABABA'
                }
            }
        });

        c3.generate({
            bindto: '#slineChart',
            data:{
                columns: [
                    ['data1', 30, 200, 100, 400, 150, 250],
                    ['data2', 130, 100, 140, 200, 150, 50]
                ],
                colors:{
                    data1: '#1ab394',
                    data2: '#BABABA'
                },
                type: 'spline'
            }
        });

        c3.generate({
            bindto: '#scatter',
            data:{
                xs:{
                    data1: 'data1_x',
                    data2: 'data2_x'
                },
                columns: [
                    ["data1_x", 3.2, 3.2, 3.1, 2.3, 2.8, 2.8, 3.3, 2.4, 2.9, 2.7, 2.0, 3.0, 2.2, 2.9, 2.9, 3.1, 3.0, 2.7, 2.2, 2.5, 3.2, 2.8, 2.5, 2.8, 2.9, 3.0, 2.8, 3.0, 2.9, 2.6, 2.4, 2.4, 2.7, 2.7, 3.0, 3.4, 3.1, 2.3, 3.0, 2.5, 2.6, 3.0, 2.6, 2.3, 2.7, 3.0, 2.9, 2.9, 2.5, 2.8],
                    ["data2_x", 3.3, 2.7, 3.0, 2.9, 3.0, 3.0, 2.5, 2.9, 2.5, 3.6, 3.2, 2.7, 3.0, 2.5, 2.8, 3.2, 3.0, 3.8, 2.6, 2.2, 3.2, 2.8, 2.8, 2.7, 3.3, 3.2, 2.8, 3.0, 2.8, 3.0, 2.8, 3.8, 2.8, 2.8, 2.6, 3.0, 3.4, 3.1, 3.0, 3.1, 3.1, 3.1, 2.7, 3.2, 3.3, 3.0, 2.5, 3.0, 3.4, 3.0],
                    ["data1", 1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5, 1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5, 1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3],
                    ["data2", 2.5, 1.9, 2.1, 1.8, 2.2, 2.1, 1.7, 1.8, 1.8, 2.5, 2.0, 1.9, 2.1, 2.0, 2.4, 2.3, 1.8, 2.2, 2.3, 1.5, 2.3, 2.0, 2.0, 1.8, 2.1, 1.8, 1.8, 1.8, 2.1, 1.6, 1.9, 2.0, 2.2, 1.5, 1.4, 2.3, 2.4, 1.8, 1.8, 2.1, 2.4, 2.3, 1.9, 2.3, 2.5, 2.3, 1.9, 2.0, 2.3, 1.8]
                ],
                colors:{
                    data1: '#1ab394',
                    data2: '#BABABA'
                },
                type: 'scatter'
            }
        });

        c3.generate({
            bindto: '#stocked',
            data:{
                columns: [
                    ['data1', 30,200,100,400,150,250],
                    ['data2', 50,20,10,40,15,25]
                ],
                colors:{
                    data1: '#1ab394',
                    data2: '#BABABA'
                },
                type: 'bar',
                groups: [
                    ['data1', 'data2']
                ]
            }
        });

        c3.generate({
            bindto: '#gauge',
            data:{
                columns: [
                    ['data', 91.4]
                ],

                type: 'gauge'
            },
            color:{
                pattern: ['#1ab394', '#BABABA']

            }
        });

        c3.generate({
            bindto: '#pie',
            data:{
                columns: [
                    ['data1', 30],
                    ['data2', 120]
                ],
                colors:{
                    data1: '#1ab394',
                    data2: '#BABABA'
                },
                type : 'pie'
            }
        });

    });
</script>

<!-- Homepage Table -->
<script>
$(document).ready(function () {

    // Examle data for jqGrid
    var mydata = [
        {id: "1", invdate: "2010-05-24", name: "test", note: "note", tax: "10.00", total: "2111.00"} ,
        {id: "2", invdate: "2010-05-25", name: "test2", note: "note2", tax: "20.00", total: "320.00"},
        {id: "3", invdate: "2007-09-01", name: "test3", note: "note3", tax: "30.00", total: "430.00"},
        {id: "4", invdate: "2007-10-04", name: "test", note: "note", tax: "10.00", total: "210.00"},
        {id: "5", invdate: "2007-10-05", name: "test2", note: "note2", tax: "20.00", total: "320.00"},
        {id: "6", invdate: "2007-09-06", name: "test3", note: "note3", tax: "30.00", total: "430.00"},
        {id: "7", invdate: "2007-10-04", name: "test", note: "note", tax: "10.00", total: "210.00"},
        {id: "8", invdate: "2007-10-03", name: "test2", note: "note2", amount: "300.00", tax: "21.00", total: "320.00"},
        {id: "9", invdate: "2007-09-01", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"},
        {id: "11", invdate: "2007-10-01", name: "test", note: "note", amount: "200.00", tax: "10.00", total: "210.00"},
        {id: "12", invdate: "2007-10-02", name: "test2", note: "note2", amount: "300.00", tax: "20.00", total: "320.00"},
        {id: "13", invdate: "2007-09-01", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"},
        {id: "14", invdate: "2007-10-04", name: "test", note: "note", amount: "200.00", tax: "10.00", total: "210.00"},
        {id: "15", invdate: "2007-10-05", name: "test2", note: "note2", amount: "300.00", tax: "20.00", total: "320.00"},
        {id: "16", invdate: "2007-09-06", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"},
        {id: "17", invdate: "2007-10-04", name: "test", note: "note", amount: "200.00", tax: "10.00", total: "210.00"},
        {id: "18", invdate: "2007-10-03", name: "test2", note: "note2", amount: "300.00", tax: "20.00", total: "320.00"},
        {id: "19", invdate: "2007-09-01", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"},
        {id: "21", invdate: "2007-10-01", name: "test", note: "note", amount: "200.00", tax: "10.00", total: "210.00"},
        {id: "22", invdate: "2007-10-02", name: "test2", note: "note2", amount: "300.00", tax: "20.00", total: "320.00"},
        {id: "23", invdate: "2007-09-01", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"},
        {id: "24", invdate: "2007-10-04", name: "test", note: "note", amount: "200.00", tax: "10.00", total: "210.00"},
        {id: "25", invdate: "2007-10-05", name: "test2", note: "note2", amount: "300.00", tax: "20.00", total: "320.00"},
        {id: "26", invdate: "2007-09-06", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"},
        {id: "27", invdate: "2007-10-04", name: "test", note: "note", amount: "200.00", tax: "10.00", total: "210.00"},
        {id: "28", invdate: "2007-10-03", name: "test2", note: "note2", amount: "300.00", tax: "20.00", total: "320.00"},
        {id: "29", invdate: "2007-09-01", name: "test3", note: "note3", amount: "400.00", tax: "30.00", total: "430.00"}
    ];

    // Configuration for jqGrid Example 1
    $("#table_list_1").jqGrid({
        data: mydata,
        datatype: "local",
        height: 250,
        styleUI : 'Bootstrap',
        autowidth: true,
        // shrinkToFit: true,
        autowidth:true,
        autoHeight:true,
        rowNum: 10,
        rowList: [10, 20, 30],
        colNames: ['Campaign', 'Spend', 'conv.', 'imp', 'clicks', 'cpc', 'cpm', 'CVR', 'CTR', 'Compare'],
        colModel: [
            {name: 'id', index: 'id', width: 60, sorttype: "int"},
            {name: 'invdate', index: 'invdate', width: 90, sorttype: "date", formatter: "date"},
            {name: 'name', index: 'name', width: 100},
            {name: 'amount', index: 'amount', width: 80, align: "right", sorttype: "float", formatter: "number"},
            {name: 'tax', index: 'tax', width: 80, align: "right", sorttype: "float"},
            {name: 'total', index: 'total', width: 80, align: "right", sorttype: "float"},
            {name: 'note', index: 'note', width: 150, sortable: false},
            {name: 'note', index: 'note', width: 150, sortable: false},
            {name: 'note', index: 'note', width: 150, sortable: false},
            {name: "closed", width: 70, align: "center",
            formatter: "checkbox", formatoptions: { disabled: false},
            edittype: "checkbox", editoptions: {value: "Yes:No", defaultValue: "Yes"},
            stype: "select", searchoptions: { sopt: ["eq", "ne"], 
                value: ":Any;true:Yes;false:No" } },
        ],
        beforeSelectRow: function (rowid, e) {
            var $self = $(this),
                iCol = $.jgrid.getCellIndex($(e.target).closest("td")[0]),
                cm = $self.jqGrid("getGridParam", "colModel"),
                localData = $self.jqGrid("getLocalRow", rowid);
            if (cm[iCol].name === "closed") {
                localData.closed = $(e.target).is(":checked");
            }

            return true; // allow selection
        },
        pager: "#pager_list_1",
        viewrecords: true,
        // caption: "Example jqGrid 1",
        hidegrid: false,
        gridview: true,

    });

    // Add responsive to jqGrid
    $(window).bind('resize', function () {
        var width = $('.jqGrid_wrapper').width();
        $('#table_list_1').setGridWidth(width);
        $('#table_list_2').setGridWidth(width);
    });
});

</script>