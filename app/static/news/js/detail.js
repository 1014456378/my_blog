function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function(){
    talk_list_vue = new Vue({
        el:'.comment_list_con',
        delimiters: ['[[', ']]'],
        data:{
            talk_list:[]
        }
    });


    // 收藏
    $(".collection").click(function () {
        $.post('/collect',{
            'flag':1,
            'text_id':$('#text_id').val(),
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if(data.result==1){
                alert('请登陆')
            }else if(data.result==2){
                alert('请不要重复收藏')
                $('.collection').hide();
                $('.collected').show();
            }else{
                $('.collection').hide();
                $('.collected').show();
            }
        })
       
    })

    // 取消收藏
    $(".collected").click(function () {
        $.post('/collect',{
                    'flag':2,
                    'text_id':$('#text_id').val(),
                    'csrf_token':$('#csrf_token').val()
                },function (data) {
                    if(data.result==1){
                        alert('请登录')
                    }else if(data.result==2){
                        alert('未收藏')
                        $('.collection').show();
                        $('.collected').hide();
                    }else{
                        $('.collection').show();
                        $('.collected').hide();
                    }
                })
     
    })

        // 评论提交
    $(".comment_form").submit(function (e) {
        e.preventDefault();
        $.post('/get_talk',{
            'talk':$('.comment_input').val(),
            'text_id':$('#text_id').val(),
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if(data.result==1){
                alert('评论不能为空')
            }else{
                take_talk()
                $('.comment_input').val('')
            }
        })
    })

    $('.comment_list_con').delegate('a,input','click',function(){

        var sHandler = $(this).prop('class');

        if(sHandler.indexOf('comment_reply')>=0)
        {
            $(this).next().toggle();
        }

        if(sHandler.indexOf('reply_cancel')>=0)
        {
            $(this).parent().toggle();
        }



        if(sHandler.indexOf('reply_sub')>=0)
        {
            var msg=$(this).prev().val();
            //清空内容
            $(this).prev().val('');
            //隐藏回复
            $(this).parent().toggle();
            $.post('/get_stalk', {
                'talk': msg,
                'talk_id': $(this).attr('name'),
                'text_id': $('#text_id').val(),
                'csrf_token': $('#csrf_token').val()
            }, function (data) {
               if(data.result==1){
                   alert('评论不能为空')
               }else{
                    take_talk();
                    $('.reply_input').val('')
               }})
        }
    })
    take_talk()

})
function take_talk() {
    $.post('/talk',{
        'text_id':$('#text_id').val(),
        'csrf_token':$('#csrf_token').val()
    },function (data) {
        talk_list_vue.talk_list=data.talk_list;
        $('.comment_count span').text(data.count)
    });
}
