var currentCid = 0; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {

    // 首页分类切换
    // $('.menu li').click(function () {
    //     var clickCid = $(this).attr('data-cid')
    //     $('.menu li').each(function () {
    //         $(this).removeClass('active')
    //     })
    //     $(this).addClass('active')
    //
    //     if (clickCid != currentCid) {
    //         // TODO 去加载新闻数据
    //
    //     }
    // })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            data_querying = false;
            cur_page++;
            if (cur_page <= total_page) {
                updateNewsData();
            }
        }
    });
    art_list_vue = new Vue({
        el:'.list_con',
        delimiters: ['[[', ']]'],
        data:{
            art_list:[]
        }
    });
    updateNewsData()
})

function updateNewsData() {
    // TODO 更新新闻数据
    $.get('/art/',{
        'page':cur_page
    },function (data) {
        total_page=data.total_page;
        if(cur_page==1){
            art_list_vue.art_list=data.list;
        }else{

            art_list_vue.art_list=art_list_vue.art_list.concat(data.list);

        }
        data_querying=true
    })
}
