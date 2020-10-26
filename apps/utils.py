import random
import string
import time

from apps.log import logger


def error(msg, code=400):
    return {'code': code, 'res': '', 'msg': msg}


def res(data):
    return {'code': 200, 'res': data}


def random_str(num: int):
    if isinstance(num, int) and 0 < num < 100:
        salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
        return salt
    else:
        return ''


def timing_(func):
    # 2020/4/10 计时装饰器
    def wrapper(*args, **kwargs):
        start_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time-start_time
        logger.info("{}消耗时间为{}".format(func.__name__, cost_time))
        return ret
    return wrapper
