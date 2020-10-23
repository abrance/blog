import random
import string


def res(data):
    return {'res': data}


def random_str(num: int):
    if isinstance(num, int) and 0 < num < 100:
        salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
        return salt
    else:
        return ''
