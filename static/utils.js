function get_difference_time(time_from_server) {
    let new_date = new Date().getTime();
    const timezone = 8;
    const offset = new Date().getTimezoneOffset();
    const local_time = new Date(new_date+offset*60*1000+timezone*60*60*1000);
    let t_before = local_time - Date.parse(time_from_server);
    let days = Math.floor(t_before/(24*60*60*1000));
    let leave = Math.floor(t_before%(24*60*60*1000));
    let hours = Math.floor(leave/(3600*1000));
    let minutes = Math.floor(leave%(3600*1000)/(60*1000));
    let time_str = '';
    if (days > 0)
    {
        time_str = `${days} 天前`;
    } else if (hours > 0)
    {
        time_str = `${hours} 小时前`;
    } else if (minutes > 0)
    {
        time_str = `${time_str} 分钟前`;
    }
    console.log(time_str)
    return time_str;
}