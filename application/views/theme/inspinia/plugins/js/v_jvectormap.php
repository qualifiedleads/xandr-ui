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

        var vmap = new jvm.Map({
            container: $('#world_map'),
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
                    values: mapData,
                    scale: ["#1ab394", "#22d6b1"],
                    normalizeFunction: 'polynomial'
                }]
            },
            onRegionTipShow: function(event, label, code){
                label.html(
                    label.html()
                    +' <br/>hits: '+mapData[code]
                );
            }
        });
    </script>
