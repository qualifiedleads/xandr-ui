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