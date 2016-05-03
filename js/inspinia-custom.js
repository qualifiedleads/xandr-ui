pageLoader = {}
pageLoader.start = function() {
    $("#full_loader").css("display", "table");
}
pageLoader.stop = function() {
    $("#full_loader").css("display", "none");
}