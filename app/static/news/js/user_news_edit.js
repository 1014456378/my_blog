function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    // $(".release_form").submit(function (e) {
    //     e.preventDefault();
    //     alert('1')
    //     var title = $('.input_txt2').val();
    //     var content = $('#rich_content').val();
    //     alert(title)
    //     alert(content)
    //     $.post('/user/user_news_edit',{
    //         'title':title,
    //         'content':content,
    //         'csrf_token':$('#csrf_token').val()
    //     },function (data) {
    //         if(data.result==1){
    //             $('.error_tip2').text('不能有空')
    //         }else{
    //             $(location).attr('href','/user/user_news_list')
    //         }
    //     });

        // TODO 发布完毕之后需要选中我的发布新闻
       // window.parent.fnChangeMenu(6)
        // // 滚动到顶部
        // window.parent.scrollTo(0, 0)
    // })
})