import hashlib
import random
import string
import time
from datetime import datetime

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


def time_string(t1):
    """
    时间求差返回字符
    :param t1: 减数
    :return: n s/m/d
    """
    logger.info('t1:{}'.format(t1))
    t2 = datetime.now()
    logger.info('{} {} {}'.format(type(t1), type(t2), t2))
    assert isinstance(t1, datetime) and isinstance(t2, datetime)
    t1 = t1 if t1 <= t2 else t2
    days = (t2-t1).days
    if days > 0:
        t_str = "{}天前".format(days)
    elif (t2-t1).seconds > 0:
        total_sec = (t2-t1).seconds
        if total_sec >= 3600:
            t_str = "{}小时前".format(total_sec//3600)
        elif total_sec >= 60:
            t_str = "{}分钟前".format(total_sec//60)
        else:
            t_str = "{}秒前".format(total_sec)
    else:
        t_str = "刚刚"
    logger.info(t_str)
    return t_str


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


# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
TWEPOCH = 1288834974657


class ClockException(Exception):
    def __init__(self):
        super(ClockException, self).__init__("Clock Error")


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    @staticmethod
    def _gen_timestamp():
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logger.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
            raise ClockException()

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


class MD5(object):
    """
    md5 稍微封装
    """
    def __init__(self):
        self.md5_obj = hashlib.md5()

    def bin_and_md5(self, _str):
        self.md5_obj.update(_str.encode())
        return self.md5_obj.hexdigest()


my_md5 = MD5()
worker = IdWorker(1, 1, 0)


if __name__ == '__main__':
    print(worker.get_id())
