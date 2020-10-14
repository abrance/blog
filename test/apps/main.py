import requests


"""
test main.py
测试是否能连上服务，需要提前开启server
"""
def test_run():
    ret = requests.get('http://localhost:8888/')
    if ret.ok:
        return True

    
if __name__ == "__main__":
    print(test_run())
