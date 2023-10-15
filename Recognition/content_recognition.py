import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib


lfasr_host = 'https://raasr.xfyun.cn/v2/api'
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, upload_file_path):
        appid="4a99b8bf"
        secret_key="344e2137a4918553229881ec6c91b6e0"
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        result = json.loads(response.text)
        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        status = 3
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            result = json.loads(response.text)
            data=result
            status = result['content']['orderInfo']['status']
            if status == 4:
                break
            time.sleep(5)
        order_result_json = json.loads(result['content']['orderResult'])
        lattice_list = order_result_json['lattice']
        transcriptions = []
        for lattice in lattice_list:
            json_1best = json.loads(lattice['json_1best'])
            transcription = json_1best['st']['rt'][0]['ws']
            transcriptions.append("".join([word["cw"][0]["w"] for word in transcription]))

        return transcriptions




# 讯飞开放平台


def text_output(file_path):
    api=RequestApi(upload_file_path=file_path)
    return api.get_result()
