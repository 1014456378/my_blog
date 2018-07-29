function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $('.pass_info').submit(function (e) {
        e.preventDefault();
        var old_pass=$('#old_pass').val();
        var new_pass1=$('#new_pass1').val();
        var new_pass2=$('#new_pass2').val();
        $.post('/user/user_pass_info',{
            'old_pass':old_pass,
            'new_pass1':new_pass1,
            'new_pass2':new_pass2,
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if(data.result==1){
                alert('输入不能有空')
            }else if(data.result==2){
                alert('密码不正确')
            }else if(data.result==3){
                alert('两次输入的新密码不相同')
            }else{
                $('#old_pass').val('');
                $('#new_pass1').val('');
                $('#new_pass2').val('');
                alert('修改成功')

            }
        })



    })
})