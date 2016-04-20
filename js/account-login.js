$("form").submit(function(e){e.preventDefault()});
var submit_signin = function(){
    var username = $("#signin_form input[name='username']");
    var password = $("#signin_form input[name='password']");
    var errors = 0;
    var notify_required = {arrowShow:true,position:"bottom center",className:"error",autoHideDelay:3000,showDuration:100,hideDuration:100}
    
    $("#signin_form input.required").removeClass("required");
    $("#signin_form .message_box").html("");

    if($.trim(username.val()) == ""){ // Check username.
        username.removeClass("required");
        setTimeout(function(){username.addClass("required").trigger("focus")},1);
        $("input[name='username']").notify("This field is required.",notify_required);
        errors++;
    }
    else{ // Username is good.
        username.removeClass("required");
        if($.trim(password.val()) == ""){ // Then check password.
            password.removeClass("required");
            setTimeout(function(){password.addClass("required").trigger("focus")},1);
            $("input[name='password']").notify("This field is required.",notify_required);
            errors++;
        }
        else{ // Password is good too.
            password.removeClass("required");
            $("#signin_form .login_message").css("display","none");
        }
    }
    if(errors == 0){ // Submitting state.
        $.ajax({
            "url" : top.location,
            "type" : "POST",
            "data" : $("#signin_form").serialize(),
            "success" : function(response){ // Submitted.
                setTimeout(function(){
                    // Login failed.
                    if(response.status == "error"){
                        $("#signin_form .message_template span.message").text(response.message);
                        var popup = $("#signin_form .message_template > div.alert-danger").clone(true).css("display","block").addClass("shaking");
                        $("#signin_form .message_box").html(popup);
                    }
                    // Login success.
                    if(response.status == "ok"){
                        top.location = response.message;
                    }
                    $("#signin_form input").removeAttr("disabled");
                    $("#signin_form a.btn").removeClass("wait disabled");
                    $("#signin_form a.submit").unbind("click").click(function(){return true});
                },1000);
            }
        });

        $("#signin_form input").attr("disabled","true");
        $("#signin_form a.btn").addClass("wait disabled");
        $("#signin_form a.submit").click(function(){return false});
    }
}
var submit_reset = function(){
    var rmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var email = $("#reset_form input[name='email']");
    var errors = 0;
    var notify_required = {arrowShow:true,position:"bottom center",className:"error",autoHideDelay:3000,showDuration:100,hideDuration:100}
    
    $("#reset_form input.required").removeClass("required");
    $("#reset_form .message_box").html("");

    if($.trim(email.val()) == ""){
        email.removeClass("required");
        setTimeout(function(){email.addClass("required").trigger("focus")},1);
        email.notify("This field is required.", notify_required);
        errors++;
    }
    else{
        if(!rmail.test(email.val())){
            email.removeClass("required");
            setTimeout(function(){email.addClass("required").trigger("focus")},1);
            email.notify("Email is invalid.", notify_required);
            errors++;
        }
        else{
            email.removeClass("required");
        }
    }
    if(errors == 0){
        $.ajax({
            "url" : top.location,
            "type" : "POST",
            "data" : $("#reset_form").serialize(),
            "success" : function(response){
                setTimeout(function(){
                    // Login failed.
                    if(response.status == "error"){
                        $("#reset_form .message_template span.message").text(response.message);
                        var popup = $("#reset_form .message_template > div.alert-danger").clone(true).css("display","block").addClass("shaking");
                        $("#reset_form .message_box").html(popup);
                    }
                    // Login success.
                    if(response.status == "ok"){
                        $("#reset_form .message_template span.message").text(response.message);
                        var popup = $("#reset_form .message_template > div.alert-success").clone(true).css("display","block").addClass("animate tada");
                        $("#reset_form .message_box").html(popup);
                    }
                    $("#reset_form input").removeAttr("disabled");
                    $("#reset_form a.btn").removeClass("wait disabled");
                    $("#reset_form a.submit").unbind("click").click(function(){return true});
                },1000);
            }
        });

        $("#reset_form input").attr("disabled","true");
        $("#reset_form a.btn").addClass("wait disabled");
        $("#reset_form a.submit").click(function(){return false});
    }
}
var submit_new_pass = function(){
    var npassword = $("#change_pass_form input[name='npassword']");
    var rpassword = $("#change_pass_form input[name='rpassword']");
    var errors = 0;
    var notify_required = {arrowShow:true,position:"bottom center",className:"error",autoHideDelay:3000,showDuration:100,hideDuration:100}
    
    $("#change_pass_form input.required").removeClass("required");
    $("#change_pass_form .message_box").html("");

    if($.trim(npassword.val()) == ""){
        npassword.removeClass("required");
        setTimeout(function(){npassword.addClass("required").trigger("focus")},1);
        npassword.notify("This field is required.", notify_required);
        errors++;
    }
    else{
        if($.trim(rpassword.val()) == ""){
            rpassword.removeClass("required");
            setTimeout(function(){rpassword.addClass("required").trigger("focus")},1);
            rpassword.notify("This field is required.", notify_required);
            errors++;
        }
        else if(npassword.val() != rpassword.val()){
            $("#change_pass_form .message_template span.message").text("Password mismatch.");
            var popup = $("#change_pass_form .message_template > div.alert-danger").clone(true).css("display","block").addClass("shaking");
            $("#change_pass_form .message_box").html(popup);
        }
        else{
            $.ajax({
                "url" : $("#change_pass_form").attr("action"),
                "type" : "POST",
                "data" : $("#change_pass_form").serialize(),
                "success" : function(response){
                    setTimeout(function(){
                        $("#change_pass_form a.btn").removeClass("wait disabled");
                        $("#change_pass_form a.submit").unbind("click").click(function(){return true});
                        // Action failed.
                        if(response.status == "error"){
                            $("#change_pass_form .message_template span.message").text(response.message);
                            var popup = $("#change_pass_form .message_template > div.alert-danger").clone(true).css("display","block").addClass("shaking");
                            $("#change_pass_form .message_box").html(popup);
                            $("#change_pass_form input").removeAttr("disabled");
                        }
                        // Action success.
                        if(response.status == "ok"){
                            $("#change_pass_form .message_template span.message").text(response.message);
                            var popup = $("#change_pass_form .message_template > div.alert-success").clone(true).css("display","block").addClass("animate tada");
                            $("#change_pass_form .message_box").html(popup);
                            $("#change_pass_button").text("Ok").unbind().click(function(){top.location="sessions"});
                        }
                    },1000);
                }
            });

            $("form input").attr("disabled","true");
            $("#change_pass_form a.btn").addClass("wait disabled");
            $("#change_pass_form a.submit").click(function(){return false});
        }
    }
}
$("#signin_button").click(submit_signin);
$("#signin_form").keypress(function(e) {
  if(e.which == 13) {
    submit_signin();
  }
});
$("#reset_button").click(submit_reset);
$("#reset_form").keypress(function(e) {
  if(e.which == 13) {
    submit_reset();
  }
});
$("#change_pass_button").click(submit_new_pass);
$("#change_pass_form").keypress(function(e) {
  if(e.which == 13) {
    submit_new_pass();
  }
});