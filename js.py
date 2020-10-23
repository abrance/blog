import linecache

from settings.config import Config
import glob2

from apps.log import logger


"""
这是一个加入js 脚本的脚本，将static下html文件一键添加脚本。
因为只是一个小功能，没有将它封装，也不存在什么 测试脚本了。
"""


js = '<script type="text/javascript" src="https://cdn.bootcdn.net/ajax/libs/jquery/1.11.3/jquery.js">' \
     '</script><script> $(function () {$("a").attr("target", "_blank");})</script>'


def edit_js_in_html(_js):

    html_ls = glob2.glob('{}/*.html'.format(Config.static_path))
    logger.info('html_ls: {}'.format(html_ls))

    for i in html_ls:
        # 2020/10/21 获取第二行
        logger.info(i)
        length = len(linecache.getlines(i))
        if length <= 1:
            continue
        reverse_2 = linecache.getline(i, length-1)
        logger.info('-2: {}'.format(reverse_2))
        if '</script>' in reverse_2:
            continue
        else:
            reverse_1 = linecache.getline(i, length)
            logger.info('-1: {}'.format(reverse_1))
            with open(i, 'r+') as f:
                for index, line in enumerate(f.readlines()):
                    if index == length-1:
                        f.writelines([js+'\n', reverse_1])


edit_js_in_html(js)
