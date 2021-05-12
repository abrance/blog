from pathlib import Path

from flask import Flask
from flask_cors import CORS


class Config(object):
    """
    global config
    """
    DEBUG = False
    #
    # # LOG_LEVEL = "DEBUG"
    # LOG_LEVEL = "INFO"
    #
    # # DB
    # host = "localhost"
    # port = 3306
    # user = 'root'
    # password = 123456
    root_path = Path.cwd()
    static_path = str(root_path/'static')
    upload_path = str(root_path/'upload')


app = Flask(__name__, static_url_path=Config.static_path, static_folder=Config.static_path)
CORS(app, supports_credentials=True)
# json化后中文 unicode码问题
app.config['JSON_AS_ASCII'] = False
# app.config['UPLOADED_PHOTOS_DEST'] = Config.upload_path
# app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES


if __name__ == '__main__':
    print(Config.root_path)
