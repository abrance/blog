
// function get_difference_time(time_from_server) {
//     let new_date = new Date().getTime();
//     let t_before = new_date - Date.parse(time_from_server);
//     let days = Math.floor(t_before/(24*60*60*1000));
//     let leave = Math.floor(t_before%(24*60*60*1000));
//     let hours = Math.floor(leave/(3600*1000));
//     let minutes = Math.floor(leave%(3600*1000)/(60*1000));
//     let time_str = '';
//     if (days > 0)
//     {
//         time_str = `${days} 天前`;
//     } else if (hours > 0)
//     {
//         time_str = `${hours} 小时前`;
//     } else if (minutes > 0)
//     {
//         time_str = `${time_str} 分钟前`;
//     }
//     return time_str;
// }

// 绑定事件 start
// const {get_difference_time} = require("./utils");

function log_in() {
    $(".mm").show();
}

// 登录成功后将用户信息加入页面中
function append_users_info() {
    console.assert(user);
    let user_info = $("#user-info");
    // display none
    $(".mm").hide();
    user_info.children("#log_in").hide();
    // TODO 个人信息需要做一下

    let user_part =
        `<div class="user-div">
            <ul class="user-ul">
                <li><p> ${user} </p></li>
            </ul>
         </div>`;
    user_info.append(user_part);
    $(".user-div").click(function (){
        let below = $(this).children(".below-user");
        if (below.length) {
            if (below.is(":visible")) below.hide()
            else if (below.is(":hidden")) below.show()
        }
        else {
            let ls =
                `<ul class="below-user">
                    <li><p>logout</p></li>
                    <li><p>settings</p></li>
                    <li><p>me</p></li>
                    <li><p>other</p></li>
                </ul>`
            $(this).append(ls);
            $(this).find("li p").each((i, obj)=> {
                $(obj).click(function () {
                    const val = $(this).text();
                    if (val === "logout")
                    {
                        $.removeCookie("primary_id");
                        $.removeCookie("user");
                        location.reload();
                    } else if (val === "settings")
                    {

                    }
                })
            })
        }
    })

    // user_info.mouseover()
}

// 登录成功后回调函数
function log_success(response) {
    let code = response["code"];
    if (code === 200)
    {
        let res = response['res'];
        if (res)
        {
            user = res['nickname'];
            primary_id = res['primary_id'];
            append_users_info();
        } else
        {
            alert('username or password wrong');
        }
    } else if (code === 404)
    {} else
    {
        alert('unexpect exception');
    }
}

function logging() {
    let username = $("#username").val();
    let password = $.md5($("#password").val());
    $.ajax({
        type: "POST",
        url: "/lichen/logging",
        data: {username: username, password: password},
        dataType: "JSON",
        success: log_success,
    })
}
// 绑定事件 end

function expr_title(response) {
    let code = response["code"];
    console.log(code);
    if (code === 200){
        let res = response['res'];
        console.log(res);
        for (let i=0; i<res.length; i++){
            let title_dc = res[i];
            let title = title_dc['title'];
            let nickname = title_dc['nickname'];
            let title_id = title_dc['title_id'];
            let label_ls = title_dc['label_ls'];
            let create_time = title_dc['create_time'];
            let last_modify_time = title_dc['last_modify_time'];
            let label_name_ls = [];
            let span_label = ``;
            label_ls.forEach((obj)=> {
                label_name_ls.push(obj[1]);
            });
            label_name_ls.forEach((obj, index)=>{
                if (index !== 0){
                    span_label += "."
                }
                span_label += `<a class="span-a-labels">${obj}</a>`
            })
            span_label.replace(".", "");
            let new_line =
                `<tr>
                    <td>${nickname}:</td>
                    <td>
                        <div class="tr-comment-style">
                            <a class="title-link" href=/lichen/title_page/${title_id}>${title}</a>
                            <br>
                            <small>
                                <span class="title-small">
                                    ${span_label}
                                    <a class="span-a-nickname">${nickname}</a>
                                    <span class="span-time">最后修改自${last_modify_time}</span>
                                    <span class="span-time">创建自${create_time}</span>
                                </span>
                            </small>
 
                        </div>
                    </td>
                </tr>`;
            $("#title-tb").append(new_line);

        }
    } else if (code === 404){

    }
}

function get_title(){
    $.ajax({
        type: "GET",
        url: "/lichen/list/title",
        data: {page: 1},
        dataType: "JSON",
        success: expr_title
    })
}

function post_title_success(response) {
    let code = response['code'];
    if (code === 200)
    {
        let res = response['res'];
        if (res)
        {
            // TODO 应该只需要刷新 titles的窗口
            window.location.reload();
        } else
        {
            // 失败什么也不做
            console.log(res);
        }
    } else if (code === 404)
    {
        console.log(response);
    } else
    {
        console.log("unexpect exception");
    }
}

function get_post_title() {
    let label_ls = $("#label_selector").select2('data');
    if (label_ls.length === 0) {
        alert('至少要有一个标签');
    } else {
        if (user) {
            let label_id_ls = [];

            label_ls.forEach((obj)=>{
                label_id_ls.push(obj.id);
            })

            console.log(label_id_ls);
            console.log(label_ls);

            let _title = $("#editor-title").val();
            // jQuery中去除空格回车等空白字符的方法
            if (_title.length > 0 && _title.trim().replace(/\s/g,"").length > 0)
            {
                let _subtitle = $("#editor-subtitle").val();
                $.ajax({
                    type: "POST",
                    url: "/lichen/create_title",
                    data: {
                        username: user,
                        primary_id: primary_id,
                        title: _title,
                        subtitle: _subtitle,
                        label_id_ls: JSON.stringify(label_id_ls)
                    },
                    // traditional:true,
                    dataType: "JSON",
                    success:post_title_success
                })
            }
            else {
                alert('标题至少要有');
            }
        } else {
            alert('先登录');
        }
    }
}