
import os
from init import app
from flask import send_from_directory, send_file


@app.route('/')
def welcome():
    return '<h1>welcome</h1>'

@app.route('/books/<path:filename>')
def books(filename=None):
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
