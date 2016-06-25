    <script src="<?php echo base_url('theme/inspinia/js/plugins/jvectormap/jquery-jvectormap-2.0.2.min.js');?>"></script>
    <script src="<?php echo base_url('theme/inspinia/js/plugins/jvectormap/jquery-jvectormap-world-mill-en.js');?>"></script>
    <script>
        var mapData = {
            "US": 498,
            "SA": 200,
            "CA": 130,
            "DE": 220,
            "FR": 540,
            "CN": 120,
            "AU": 760,
            "BR": 550,
            "IN": 200,
            "GB": 120,
            "RU": 2000
        };
        var mapData2 = {
            "US": 1,
            "SA": 2,
            "CA": 3,
            "DE": 4,
            "FR": 5,
            "CN": 6,
            "AU": 7,
            "BR": 8,
            "IN": 9,
            "GB": 10,
            "RU": 11
        };

        var mapData3 = {
            "CN": 1,
            "SG": 2,
            "JP": 3,
            "PH": 4,
            "IN": 5,
            "TH": 6,
            "MY": 7,
            "VN": 8,
        };

        var dataSource = mapData;

        $('#world_map').vectorMap({
            backgroundColor: "transparent",
            regionStyle: {
                initial: {
                    "fill": '#e4e4e4',
                    "fill-opacity": 1,
                    "stroke": 'none',
                    "stroke-width": 0,
                    "stroke-opacity": 0
                }
            },
            series: {
                regions: [{
                    values: dataSource,
                    scale: ["#22d6b1","#027f49"],
                    normalizeFunction: 'polynomial'
                }]
            },
            onRegionTipShow: function(event, label, code){
                label.html(
                    label.html()
                    +' <br/>hits: '+dataSource[code]
                );
                //console.log(code);
            }
        });
        /*
            TO DO: Implement dynamic update function.
            
            #1 Initialize map instance.
            //  var mapObject = $('#world_map').vectorMap('get', 'mapObject');

            #2 Change data source
            //  dataSource = new_value;

            #3 Apply new values. 
            // mapObject.series.regions[0].setValues(mapData2)
        */
        
    </script>
