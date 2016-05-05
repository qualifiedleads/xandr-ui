pageLoader = {}
pageLoader.start = function() {
    $("#full_loader").css("display", "table");
}
pageLoader.stop = function() {
    $("#full_loader").css("display", "none");
}
modals = {}
modals.confirm = function(message="Default message?", fn=null) {
    var modal_ob = "#confirm_modal";
    $(modal_ob+' .modal-body').html(message);
    $(modal_ob+' [type="submit"]').unbind("click").click(fn);
    $(modal_ob).modal("show");
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
    var user_modal = "#edit_user_modal";
    var user_form = "#edit_user_form";

    $(user_modal).modal("show");
    $(user_form)[0].reset();
    $(user_modal + " input").prop("disabled", true);
    $(user_modal + " select").prop("disabled", true);
    $(user_modal + " button").prop("disabled", true);

    var fill_form = function(data) {
        var user = data[0];
        $(user_form + ' input[name="user_id"]').val(user.user_id);
        $(user_form + ' input[name="name"]').val(user.name);
        $(user_form + ' input[name="username"]').val(user.username);
        $(user_form + ' input[name="email"]').val(user.email);
        $(user_form + ' input[name="company"]').val(user.company);
        $(user_form + ' input[name="apnx_id"]').val(user.apnx_id);
        // Select type.
        $(user_form + ' select option').each(function(){
            $(this).prop("selected", false);
            if($(this).val() == user.role_id) {
                $(this).prop("selected", true);
            }
        });
        // Select status.
        $(user_form + ' input[name="status"]').each(function(){
            $(this).prop("checked", false);
            if($(this).val() == user.status) {
                $(this).prop("checked", true);
            }
        });
    }

    $.ajax({
        url: "users/json/get_by_id?id="+id,
        method: "get",
        success: function(response) {
            setTimeout(function(){
                $(user_modal + " input").prop("disabled", false);
                $(user_modal + " select").prop("disabled", false);
                $(user_modal + " button").prop("disabled", false);
                fill_form(response);
            }, 500);
        }
    });
}
users.update = function(e, f) {
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
                    $("#edit_user_modal").modal("hide");
                    $(f)[0].reset();
                }
            }, 1000);
        }
    })
}
users.delete = function(id, self) {
    var name = $(self).parents("tr").find("td").get(0).innerText;
    var message = "Do you want to delete "+name+"?";
    var fn = function()
    {
        $("#confirm_modal").modal("hide");
        pageLoader.start();

        $.ajax({
            url: "users",
            method: "post",
            data: "task=delete&id="+id,
            error: function(jqXHR) {
                setTimeout(function() {
                    // Show toastr notice.
                    toastr.options.positionClass = "toast-top-center";
                    toastr.error(jqXHR.statusText, "Error "+jqXHR.status);
                }, 1000);
            },
            success: function(response) {
                setTimeout(function(){
                    if(response.status == "ok") {
                        // Show success toastr notice.
                        toastr.options.positionClass = "toast-top-center";
                        toastr.success(response.message, "Success");
                        users.updateTable("#users_table", response.data);
                    }
                    else {
                        // Show error toastr notice.
                        toastr.options.positionClass = "toast-top-center";
                        toastr.error(response.message, "Error");
                    }
                    // Stop Loader.
                    pageLoader.stop();
                }, 1000);
            }
        });
    }
    modals.confirm(message, fn);
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
                            '<a class="btn btn-default btn-xs" onclick="users.delete('+data['user_id']+',this)" title="Delete"><i class="fa fa-trash-o"></i></a> '
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
            url: "users/json/get_all",
            method: "get",
            success: function(response) {
                builContents(response);
            }
        });
    }
}