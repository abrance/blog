
import os

import glob2
from flask import send_from_directory, send_file, jsonify, redirect

from init import app
from settings.config import Config
from log import logger
# from tools.read_png import read
from utils import res


@app.route('/')
def welcome():
    return redirect('index')


@app.route('/index')
def index():
    index_name = os.path.join(Config.static_path, 'index.html')
    return send_file(index_name)


@app.route('/apps')
def app_ls():
    _app_ls = ['books']
    return jsonify({'res': _app_ls})
    # return jsonify(_t)


@app.route('/books')
def books_list():
    """
    静态文件 列表
    """
    html_list = glob2.glob(r'{}/*.html'.format(Config.static_path))
    html_book_list = [os.path.split(i)[1] for i in html_list]
    logger.info(html_book_list)
    index_page = 'index.html'
    if index_page in html_book_list:
        html_book_list.remove(index_page)

    _res = res(html_book_list)
    return jsonify(_res)


@app.route('/books/<path:filename>')
def books(filename):
    """
    静态文件 访问接口，提供阅读
    """
    book_name = os.path.join(Config.static_path, filename)
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


# @app.route('/tools/<tool_name>', methods='POST')
# def tool_imp(tool_name):
#     """
#     工具实现
#     :param tool_name: ocr
#     :return:
#     """
#     f_ls = request.files['file']
#     os.path.join(Config.static_path, )
#     f.save()
#
#     tool_map = {
#         'ocr': read
#     }
#     if tool_name in tool_map.keys():
#         tool = tool_map.get(tool_name)
