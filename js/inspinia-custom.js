pageLoader = {}
pageLoader.start = function() {
    $("#full_loader").css("display", "table");
}
pageLoader.stop = function() {
    $("#full_loader").css("display", "none");
}
users = {}
users.view = function(id) {
    console.log("View user "+id);
}
users.new = function() {
    $("#new_user_modal").modal("show");
}
users.add = function(e, f) {
    e.preventDefault();
    var userinfo = f.serialize();
    $(f).find("button").prop("disabled", true);
    $(f).find("input").prop("disabled", true);
    $(f).find("select").prop("disabled", true);
    $.ajax({
        url: "users",
        method: "post",
        data: userinfo,
        error: function(jqXHR) {
            setTimeout(function() {
                // Show toastr notice.
                toastr.options.positionClass = "toast-top-center";
                toastr.error(jqXHR.statusText, "Error "+jqXHR.status);
                // Disable form fields.
                $(f).find("input").prop("disabled", false);
                $(f).find("select").prop("disabled", false);
                $(f).find("button").prop("disabled", false);
            }, 1000);
        },
        success: function(response) {
            setTimeout(function() {
                // Disable form fields.
                $(f).find("input").prop("disabled", false);
                $(f).find("select").prop("disabled", false);
                $(f).find("button").prop("disabled", false);
                // Show toastr notice.
                if(response.status == "error") {
                    toastr.options.positionClass = "toast-top-center";
                    toastr.error(response.message, "Error");
                }
                else if(response.status == "ok") {
                    users.updateTable("#users_table", response.data);
                    toastr.options.positionClass = "toast-top-center";
                    toastr.success(response.message, "Success");
                    $("#new_user_modal").modal("hide");
                    $(f)[0].reset();
                }
            }, 1000);
        }
    })
}
users.edit = function(id) {
    $("#edit_user_modal").modal("show");
    $("#edit_user_modal input").prop("disabled", true);
    $("#edit_user_modal select").prop("disabled", true);
    $("#edit_user_modal button").prop("disabled", true);
    var fill_form = function(json_array) {

    }
    
}
users.delete = function(id) {
    console.log("Delete user "+id);
}
users.updateTable = function(id = "#users_table", data) {
    var builContents = function(json_array) {
        var entries = "";
                for(n in json_array) {
                    var data = json_array[n];
                    var status_label = (data['status'] == "active")? "label-primary" : "label-danger";
                    entries +=
                    '<tr>'+
                        '<td>'+
                            data['name']+
                        '</td>'+
                        '<td>'+
                            data['role_name']+
                        '</td>'+
                        '<td>'+
                            data['username']+
                        '</td>'+
                        '<td>'+
                            data['email']+
                        '</td>'+
                        '<td>'+
                            '<span class="label '+status_label+'">'+data['status']+'</span>'+
                        '</td>'+
                        '<td>'+
                            '<a class="btn btn-default btn-xs" onclick="users.view('+data['user_id']+')" title="Vew Details"><i class="fa fa-eye"></i></a> '+
                            '<a class="btn btn-default btn-xs" onclick="users.edit('+data['user_id']+')" title="Edit"><i class="fa fa-pencil"></i></a> '+
                            '<a class="btn btn-default btn-xs" onclick="users.delete('+data['user_id']+')" title="Delete"><i class="fa fa-trash-o"></i></a> '
                        '</td>'+
                    '</tr>';
                }
                $(id+" tbody").html(entries);
                $(id).footable();
    }
    if(data) {
        builContents(data);
    }
    else {
        $.ajax({
            url: "users/json/getall",
            method: "get",
            success: function(response) {
                builContents(response);
            }
        });
    }
}