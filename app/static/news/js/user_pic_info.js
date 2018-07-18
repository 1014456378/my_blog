function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $('.pic_info').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url:"/user/user_pic_info",
            type:"post",
            dataType:"json",
            success:function (data) {
                if (data.result == 1) {
                    alert('请选择图片')
                } else {
                    $('.now_user_pic').attr('src', data.pic);
                    $('.user_center_pic img', parent.document).attr('src', data.pic);
                    $('.lgin_pic', parent.document).attr('src', data.pic);
                }
            }
        });
    });
})