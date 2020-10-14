
from flask import Flask
import os


static_path = os.path.join(os.path.abspath('./'), 'static')
print('static: {}'.format(static_path))
app = Flask(__name__, static_url_path=static_path)
