$.fn.paminta = function(callback){
    var notify_style = {arrowShow:true,position:"bottom center",className:"error",autoHideDelay:3000,showDuration:100,hideDuration:100}
    var the_form = this;
    $(this).submit(function(){
        var pamintas = $(this).find('[data-paminta]');
        var errors = 0;
        pamintas.removeClass("paminta-blow");
        $(this).find('[data-paminta]').each(function(n){
            var field = $(this);
            /* Validate text */
            if($(this).attr('data-paminta') == "text"){
                if($.trim(field.val()) == ""){
                    field.trigger("focus").notify("This field is required", notify_style);
                    setTimeout(function(){field.addClass("paminta-blow")},1);
                    errors++;
                    return false;
                }
                else{
                    field.removeClass("paminta-blow");
                }
            }

            /* Validate password */
            if($(this).attr('data-paminta') == "password"){
                if($.trim(field.val()) == ""){
                    field.trigger("focus").notify("This field is required", notify_style);
                    setTimeout(function(){field.addClass("paminta-blow")},1);
                    errors++;
                    return false;
                }
                else{
                    if(field.val().length < 6){
                        field.trigger("focus").notify("Too short (<6).", notify_style);
                        setTimeout(function(){field.addClass("paminta-blow")},1);
                        errors++;
                        return false;
                    }
                    else{
                        field.removeClass("paminta-blow");
                    }
                }
            }

            /* Validate email */
            if($(this).attr('data-paminta') == "email"){
                var rmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                if($.trim(field.val()) == ""){
                    field.trigger("focus").notify("This field is required", notify_style);
                    setTimeout(function(){field.addClass("paminta-blow")},1);
                    errors++;
                    return false;
                }
                else{
                    if(!rmail.test(field.val())){
                        field.trigger("focus").notify("Invalid email.", notify_style);
                        setTimeout(function(){field.addClass("paminta-blow")},1);
                        errors++;
                        return false;
                    }
                    else{
                        field.removeClass("paminta-blow");
                    }
                }
            }

            /* Validate url */
            if($(this).attr('data-paminta') == "url"){
                var rurls = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
                if($.trim(field.val()) == ""){
                    field.trigger("focus").notify("This field is required", notify_style);
                    setTimeout(function(){field.addClass("paminta-blow")},1);
                    errors++;
                    return false;
                }
                else{
                    if(!rurls.test(field.val())){
                        field.trigger("focus").notify("Invalid url.", notify_style);
                        setTimeout(function(){field.addClass("paminta-blow")},1);
                        errors++;
                        return false;
                    }
                    else{
                        field.removeClass("paminta-blow");
                    }
                }
            }
        });
        if(errors == 0){
            if(typeof callback == "function"){
                return callback();
            }
            else{
                return true;
            }
        }
        else{
            return false;
        }
    });
    $(this).find('[type="reset"]').click(function(){the_form.find("input").removeClass("paminta-blow");});
}