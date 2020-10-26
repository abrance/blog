
import os
from pathlib import Path

import glob2
from flask import send_from_directory, send_file, jsonify, redirect, request

from settings.config import Config, app
from apps.log import logger
from tools.apis import my_ocr
from apps.utils import res, error


@app.route('/')
def welcome():
    return redirect('index')


@app.route('/index')
def index():
    index_name = os.path.join(Config.static_path, 'index.html')
    return send_file(index_name)


@app.route('/apps')
def app_ls():
    _app_ls = ['books', 'tools']
    return jsonify({'res': _app_ls})
    # return jsonify(_t)


@app.route('/books')
def books_list():
    """
    静态文件 列表
    """
    books_path = str(Path(Config.static_path)/"books")
    html_list = glob2.glob(r'{}/*.html'.format(books_path))
    html_book_list = [os.path.split(i)[1] for i in html_list]
    logger.info(html_book_list)
    # index_page = 'index.html'
    # if index_page in html_book_list:
    #     html_book_list.remove(index_page)

    _res = res(html_book_list)
    return jsonify(_res)


@app.route('/books/<path:filename>')
def books(filename):
    """
    静态文件 访问接口，提供阅读
    """
    book_name = os.path.join(Config.static_path, 'books', filename)
    return send_file(book_name)


@app.route('/static/<path:filename>')
def emacs_build(filename=None):
    """
    静态文件提供下载
    """
    return send_from_directory(Config.static_path, filename, as_attachment=True)


@app.route('/tools')
def tool_ls():
    """
    工具列表
    """
    tools = ['ocr']
    return jsonify(res(tools))


@app.route('/tools/<tool_name>', methods=['POST', 'GET'])
def tool_imp(tool_name):
    """
    工具实现
    :param tool_name: ocr
    :return:
    """
    if request.method == "GET":
        tool_page = Path(Config.static_path) / (tool_name+'.html')
        return send_file(tool_page)

    elif request.method == "POST":
        me_dc = {
            'ocr': my_ocr
        }
        ret, msg, code = me_dc.get(tool_name)(request)
        if ret:
            return jsonify(res(ret))
        else:
            return jsonify(error(msg, code))
    else:
        return jsonify(error('no support method type'))
