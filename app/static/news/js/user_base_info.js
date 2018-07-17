function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {

    $(".base_info").submit(function (e) {
        e.preventDefault();

        var signature = $("#signature").val()
        var nick_name = $("#nick_name").val()
        var gender = $(".gender").val()

        if (!nick_name) {
            alert('请输入昵称')
            return
        }

        $.post('/user/user_base_info',{
            'name':nick_name,
            'csrf_token':$("#csrf_token").val(),
        },function (data) {
            if(data.result==1){
                alert('不能为空')
            }else{
                $('.user_center_name',parent.document).text(nick_name)
                $('#name',parent.document).text(nick_name)
            }
        })
        // TODO 修改用户信息接口
    })
})