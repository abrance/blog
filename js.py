import linecache

from apps.init import static_path
import glob2

from apps.log import logger

js = '<script type="text/javascript" src="https://cdn.bootcdn.net/ajax/libs/jquery/1.11.3/jquery.js">' \
     '</script><script> $(function () {console.log($("a").attr("target", "_blank"));})</script>'


def edit_js_in_html(_js):

    html_ls = glob2.glob('{}/*.html'.format(static_path))
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
