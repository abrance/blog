
from flask import Flask

from settings.config import Config

app = Flask(__name__, static_url_path=Config.static_path)
# json化后中文 unicode码问题
app.config['JSON_AS_ASCII'] = False
