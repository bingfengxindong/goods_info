function email_verify() {
    var email = $("#inputText1").val();
    if(email == ""){
        $("#email_verify_text").html("<b style='color: red'>邮箱不能为空！</b>")
    }else{
        $("#email_verify_text").html("<b style='color: green'>邮箱符合要求！</b>")
    }
}
function phone_verify() {
    var phone_number = $("#inputText2").val();
    if(phone_number == ""){
        $("#phone_verify_text").html("<b style='color: red'>手机号码不能为空！</b>")
    }else(
        $("#phone_verify_text").html("<b style='color: green'>手机号码符合要求！</b>")
    )
}
function nickname_verify() {
    var nickname = $("#inputText3").val();
    var nickname_len = nickname.length;
    if(nickname == ""){
        $("#nickname_verify_text").html("<b style='color: red'>用户名不能为空！</b>")
    }else if(nickname_len < 4){
        $("#nickname_verify_text").html("<b style='color: red'>用户名不能低于四位！</b>")
    }else{
        $("#nickname_verify_text").html("<b style='color: green'>用户名符合要求！</b>")
    }
}
function pwd_verify() {
    var pwd = $("#inputPassword1").val();
    var pwd_len = pwd.length;
    if(pwd == ""){
        $("#pwd_verify_text").html("<b style='color: red'>密码不能为空！</b>")
    }else if(pwd_len < 8){
        $("#pwd_verify_text").html("<b style='color: red'>密码不能低于八位！</b>")
    }else{
        $("#pwd_verify_text").html("<b style='color: green'>密码符合要求！</b>")
    }
}
function confirm_pwd_verify() {
    var pwd = $("#inputPassword1").val();
    var confirm_pwd = $("#inputPassword2").val();
    if(confirm_pwd == ""){
        $("#confirm_pwd_verify_text").html("<b style='color: red'>确认密码不能为空！</b>")
    }else if(confirm_pwd != pwd){
        $("#confirm_pwd_verify_text").html("<b style='color: red'>两次密码不同，请确认密码！</b>")
    }else{
        $("#confirm_pwd_verify_text").html("<b style='color: green'>密码符合要求！</b>")
    }
}