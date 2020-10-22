
import os

import glob2
from flask import send_from_directory, send_file, jsonify, redirect

from init import app, static_path
from utils import res


@app.route('/')
def welcome():
    return redirect('index')


@app.route('/index')
def index():
    index_name = os.path.join(static_path, 'index.html')
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
    html_list = glob2.glob(r'{}/*.html'.format(static_path))
    html_book_list = [os.path.split(i)[1] for i in html_list]

    _res = res(html_book_list)
    # dir_name = os.path.join(static_path, )
    return jsonify(_res)


@app.route('/books/<path:filename>')
def books(filename):
    """
    静态文件 访问接口，提供阅读
    """
    book_name = os.path.join(static_path, filename)
    return send_file(book_name)


@app.route('/static/<path:filename>')
def emacs_build(filename=None):
    """
    静态文件提供下载
    """
    return send_from_directory(static_path, filename, as_attachment=True)
