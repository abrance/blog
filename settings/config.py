import os


class Config(object):
    """
    global config
    """
    # DEBUG = False
    #
    # # LOG_LEVEL = "DEBUG"
    # LOG_LEVEL = "INFO"
    #
    # # DB
    # host = "localhost"
    # port = 3306
    # user = 'root'
    # password = 123456
    static_path = os.path.join(os.path.abspath('./'), 'static')


