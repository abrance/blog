# -*- coding: utf-8 -*-

import datetime
from models import Database
from web3 import Web3, HTTPProvider

# 区块链节点URL
nodeUri = 'http://192.168.40.11:22000'
w3 = Web3(HTTPProvider(nodeUri))

w3.eth.defaultAccount = w3.eth.accounts[0]

# 存证智能合约地址
eviadress = Web3.toChecksumAddress("0x0ee6ff9d95c2cbd25a16f1225c90f725825ba029")
eviabi = '[{"constant":false,"inputs":[{"name":"param1","type":"bytes"},{"name":"param2","type":"bytes"}],"name":"mergeBytes","outputs":[{"name":"","type":"bytes"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"filenameHash","type":"bytes"},{"name":"fileHash","type":"bytes"}],"name":"getEvidence","outputs":[{"name":"code","type":"uint256"},{"name":"fnHash","type":"bytes"},{"name":"fHash","type":"bytes"},{"name":"fUpLoadTime","type":"uint256"},{"name":"saverAddress","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"evidenceCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"filenameHash","type":"bytes"},{"name":"fileHash","type":"bytes"},{"name":"fileUploadTime","type":"uint256"}],"name":"saveEvidence","outputs":[{"name":"code","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"returnValue","type":"uint256"},{"indexed":false,"name":"filenameHash","type":"bytes"},{"indexed":false,"name":"fileHash","type":"bytes"},{"indexed":false,"name":"fileUploadTime","type":"uint256"}],"name":"SaveEvent","type":"event"}]'
evidence = w3.eth.contract(
    address=eviadress,
    abi=eviabi,
)


class GetEvidence(object):
    def __init__(self, evidence):
        self.evidence = evidence
        self.db = Database()

    def get_evidence(self, filename_hash, file_hash):
        evi_ret = self.evidence.functions.getEvidence(filename_hash, file_hash).call()
        # 解析evi_ret数据
        return evi_ret

    def get_record_from_db(self, offset, max_length=1000):
        sql = "SELECT * FROM contract_record LIMIT %d OFFSET %d" % (max_length, offset)
        data = self.db.get_record_from_db(sql)
        return data

    def run(self):
        start_time = datetime.datetime.now()
        failed, success, offset = 0, 0, 0
        while True:
            records = self.get_record_from_db(offset)
            if not records:
                break
            offset += len(records)
            for record in records:
                file_hash = record['file_hash']
                filename_hash = record['filename_hash']
                result = self.get_evidence(filename_hash.encode(), file_hash.encode())
                assert isinstance(result, list)
                if result[0] == 0:
                    success += 1
                else:
                    failed += 1
                print("success: {}, failed: {}".format(success, failed))
        end_time = datetime.datetime.now()
        cost_time = (end_time - start_time).total_seconds()
        self.db.close()
        result_dict = {'success': success, 'failed': failed, 'total': success + failed, 'cost_time': cost_time}
        print("result_dict: {}".format(result_dict))
        return result_dict


if __name__ == "__main__":
    get_evidence = GetEvidence(evidence)
    get_evidence.run()
