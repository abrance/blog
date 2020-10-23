import random

from apps.utils import random_str


def test_random_str():
    n = random.randint(0, 100)
    ret = random_str(n)
    assert isinstance(ret, str) and len(ret) == n
