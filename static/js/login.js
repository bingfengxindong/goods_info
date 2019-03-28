function login_verify() {
    var text = $("#inputText1").val();
    if(text == ""){
        $("#login_verify_text").html("<b style='color: red;'>登录信息不能为空！</b>")
    }else{
        $("#login_verify_text").html("<b style='color: green;'>登录信息符合要求！</b>")
    }
}
function pwd_login_verify() {
    var pwd = $("#inputPassword1").val();
    var pwd_len = pwd.length;
    if(pwd == ""){
        $("#login_pwd_verify_text").html("<b style='color: red;'>密码不能为空！</b>")
    }else if(pwd_len < 8) {
        $("#login_pwd_verify_text").html("<b style='color: red;'>密码不能低于八位！</b>")
    }else{
        $("#login_pwd_verify_text").html("<b style='color: green;'>密码符合要求！</b>")
    }
}