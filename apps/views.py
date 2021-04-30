import json
import os
from pathlib import Path

import glob2
from flask import send_from_directory, send_file, jsonify, redirect, request, make_response

from settings.config import Config, app
from apps.log import logger
from tools.apis import my_ocr
from apps.utils import res, error
from apps.models import db


@app.route('/')
def welcome():
    return redirect('index')


@app.route('/index')
def index():
    index_name = os.path.join(Config.static_path, 'index.html')
    return send_file(index_name)


@app.route('/titles')
def titles():
    titles_name = os.path.join(Config.static_path, 'titles.html')
    return send_file(titles_name)


@app.route('/expr')
def expr():
    expr_name = os.path.join(Config.static_path, 'expr.html')
    return send_file(expr_name)


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
    # books_path = str(Path(Config.static_path)/"books")
    # html_list = glob2.glob(r'{}/*.html'.format(books_path))
    # html_book_list = [os.path.split(i)[1] for i in html_list]
    # logger.info(html_book_list)

    info = request.args
    group, page, limit = info.get('group'), info.get('page'), info.get('limit')
    logger.info('{} {} {}'.format(group, page, limit))
    html_book_list = db.book_list()
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


@app.route('/lichen/list/title', methods=["GET"])
def list_title():
    """
    获取title列表
    :return:
    """
    # info = request.form
    # request.args 是get(路径)传参；好像会将 数字读成字符串
    info = request.args

    page = info.get('page')
    if isinstance(page, str) and page.isdigit() and 0 < int(page) < 100:
        page = int(page)
        title_ls = db.list_title(page)
        return jsonify(res(title_ls))
    else:
        return jsonify(error('unexpect exception'))


@app.route('/lichen/logging', methods=['POST'])
def logging():
    """
    登录
    :return:
    """
    info = request.form
    username, password = info.get('username'), info.get('password')
    if username and password and isinstance(username, str) and\
            isinstance(password, str) and len(password) == 32 and len(username) < 20:
        # _password = my_md5.bin_and_md5(password)
        logger.info("{} {}".format(username, password))
        ret = db.logging(username, password)
        if ret:
            # 设置cookie
            response = make_response(jsonify(res(ret)))
            response.set_cookie('primary_id', str(ret.get('primary_id')), max_age=3*24*60*60)
            response.set_cookie('user', ret.get('nickname'), max_age=3*24*60*60)
            return response
        else:
            return jsonify(res(False))
    else:
        logger.error('unexpect exception')
        return jsonify(error('unexpect exception'))


@app.route('/lichen/create_title', methods=["POST"])
def create_title():
    """
    发表主题
    :return:
    """
    info = request.form
    nickname, primary_id = info.get('username'), info.get('primary_id')
    title, subtitle, label_id_ls = info.get('title'), info.get('subtitle'), info.get('label_id_ls')
    logger.info('{} {} {} {} {}'.format(nickname, primary_id, title, subtitle, label_id_ls))
    try:
        assert isinstance(title, str) and isinstance(subtitle, str) and \
               isinstance(primary_id, str) and primary_id.isdigit() and isinstance(label_id_ls, str)
        label_id_ls = json.loads(label_id_ls)
        assert label_id_ls and isinstance(label_id_ls, list)
        label_id_ls = [int(i) for i in label_id_ls if i.isdigit]

    except AssertionError:
        logger.info('create title param error')
        return jsonify(error('param error'))
    ret = db.create_title(title, subtitle, int(primary_id), nickname, label_id_ls)
    return jsonify(res(ret))


@app.route('/lichen/list/label', methods=['GET'])
def list_label():
    """
    查询所有label
    :return:
    """
    ret_ls = db.list_label()
    return jsonify(res(ret_ls))


@app.route('/lichen/title/<title_id>', methods=['GET'])
def inquire_title(title_id):
    """
    单个主题查询
    :return:
    """
    try:
        assert isinstance(title_id, str) and title_id.isdigit()
    except AssertionError:
        logger.info('param error')
        return jsonify(error('param error'))
    title_id = int(title_id)
    ret = db.inquiry_title(title_id)
    return jsonify(res(ret))


@app.route('/lichen/title_page/<title_id>', methods=['GET'])
def inquire_title_page(title_id):
    """
    单个主题页面请求
    :param title_id:
    :return:
    """
    titles_name = os.path.join(Config.static_path, 'title_comments.html')
    return send_file(titles_name)


@app.route('/lichen/create_comment', methods=['POST'])
def create_comment():
    """
    创建留言
    :return:
    """
    info = request.form
    nickname, primary_id = info.get('username'), info.get('primary_id')
    title_id_str, comment = info.get('title_id'), info.get('comment')
    logger.info('{} {} {} {}'.format(nickname, primary_id, title_id_str, comment))
    try:
        assert isinstance(title_id_str, str) and isinstance(comment, str) and \
               isinstance(primary_id, str) and primary_id.isdigit()
    except AssertionError:
        logger.info('create title param error')
        return jsonify(error('param error'))
    title_id = int(title_id_str)
    ret = db.create_comment(title_id, int(primary_id), nickname, comment)
    return jsonify(res(ret))
