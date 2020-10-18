
import os

from flask import send_from_directory, send_file, jsonify

from init import app
from utils import res
# import utils


@app.route('/')
def welcome():
    return '<h1>welcome</h1>'


@app.route('/books')
def books_list():
    """
    静态文件 列表
    """
    static_path = os.path.join(os.path.abspath('./'), 'static')
    import glob2
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
    static_path = os.path.join(os.path.abspath('./'), 'static')
    dir_name = os.path.join(static_path, filename)
    return send_file(dir_name)


@app.route('/static/<path:filename>')
def emacs_build(filename=None):
    """
    静态文件提供下载
    """
    static_path = os.path.join(os.path.abspath('./'), 'static')
    return send_from_directory(static_path, filename, as_attachment=True)
