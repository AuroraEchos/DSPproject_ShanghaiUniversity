import base64
import hashlib
import hmac
import json
import os
import csv
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import requests
from pydub import AudioSegment


class Gen_req_url(object):
    """生成请求的url"""

    def sha256base64(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        # self.schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise Exception("invalid request url:" + requset_url)
        self.path = host[edidx:]
        self.host = host[:edidx]

    # build websocket auth request url
    def assemble_ws_auth_url(self, requset_url, api_key, api_secret, method="GET"):
        self.parse_url(requset_url)
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(self.host, date, method, self.path)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        values = {
            "host": self.host,
            "date": date,
            "authorization": authorization
        }

        return requset_url + "?" + urlencode(values)


def gen_req_body(apiname, APPId, file_path=None):
    """
    生成请求的body
    :param apiname
    :param APPId: Appid
    :param file_name:  文件路径
    :return:
    """
    if apiname == 'createFeature':

        with open(file_path, "rb") as f:
            audioBytes = f.read()
        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "createFeature",
                    "groupId": "iFLYTEK_examples_groupId",
                    "featureId": "iFLYTEK_examples_featureId",
                    "featureInfo": "iFLYTEK_examples_featureInfo",
                    "createFeatureRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "resource": {
                    "encoding": "lame",
                    "sample_rate": 16000,
                    "channels": 1,
                    "bit_depth": 16,
                    "status": 3,
                    "audio": str(base64.b64encode(audioBytes), 'UTF-8')
                }
            }
        }
    elif apiname == 'createGroup':

        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "createGroup",
                    "groupId": "iFLYTEK_examples_groupId",
                    "groupName": "iFLYTEK_examples_groupName",
                    "groupInfo": "iFLYTEK_examples_groupInfo",
                    "createGroupRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            }
        }
    elif apiname == 'deleteFeature':

        body = {
            "header": {
                "app_id": APPId,
                "status": 3

            },
            "parameter": {
                "s782b4996": {
                    "func": "deleteFeature",
                    "groupId": "iFLYTEK_examples_groupId",
                    "featureId": "iFLYTEK_examples_featureId",
                    "deleteFeatureRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            }
        }
    elif apiname == 'queryFeatureList':

        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "queryFeatureList",
                    "groupId": "iFLYTEK_examples_groupId",
                    "queryFeatureListRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            }
        }
    elif apiname == 'searchFea':

        with open(file_path, "rb") as f:
            audioBytes = f.read()
        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "searchFea",
                    "groupId": "iFLYTEK_examples_groupId",
                    "topK": 1,
                    "searchFeaRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "resource": {
                    "encoding": "lame",
                    "sample_rate": 16000,
                    "channels": 1,
                    "bit_depth": 16,
                    "status": 3,
                    "audio": str(base64.b64encode(audioBytes), 'UTF-8')
                }
            }
        }
    elif apiname == 'searchScoreFea':

        with open(file_path, "rb") as f:
            audioBytes = f.read()
        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "searchScoreFea",
                    "groupId": "iFLYTEK_examples_groupId",
                    "dstFeatureId": "iFLYTEK_examples_featureId",
                    "searchScoreFeaRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "resource": {
                    "encoding": "lame",
                    "sample_rate": 16000,
                    "channels": 1,
                    "bit_depth": 16,
                    "status": 3,
                    "audio": str(base64.b64encode(audioBytes), 'UTF-8')
                }
            }
        }
    elif apiname == 'updateFeature':

        with open(file_path, "rb") as f:
            audioBytes = f.read()
        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "updateFeature",
                    "groupId": "iFLYTEK_examples_groupId",
                    "featureId": "iFLYTEK_examples_featureId",
                    "featureInfo": "iFLYTEK_examples_featureInfo_update",
                    "updateFeatureRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "resource": {
                    "encoding": "lame",
                    "sample_rate": 16000,
                    "channels": 1,
                    "bit_depth": 16,
                    "status": 3,
                    "audio": str(base64.b64encode(audioBytes), 'UTF-8')
                }
            }
        }
    elif apiname == 'deleteGroup':
        body = {
            "header": {
                "app_id": APPId,
                "status": 3
            },
            "parameter": {
                "s782b4996": {
                    "func": "deleteGroup",
                    "groupId": "iFLYTEK_examples_groupId",
                    "deleteGroupRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            }
        }
    else:
        raise Exception(
            "输入的apiname不在[createFeature, createGroup, deleteFeature, queryFeatureList, searchFea, searchScoreFea,updateFeature]内，请检查")
    return body


def req_url(api_name, APPId, APIKey, APISecret, file_path=None):
    """
    开始请求
    :param APPId: APPID
    :param APIKey:  APIKEY
    :param APISecret: APISecret
    :param file_path: body里的文件路径
    :return:
    """
    gen_req_url = Gen_req_url()
    body = gen_req_body(apiname=api_name, APPId=APPId, file_path=file_path)
    request_url = gen_req_url.assemble_ws_auth_url(requset_url='https://api.xf-yun.com/v1/private/s782b4996', method="POST", api_key=APIKey, api_secret=APISecret)

    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': '$APPID'}
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    tempResult = json.loads(response.content.decode('utf-8'))
    #print(tempResult)

    return tempResult


def apiname_description():

    # 1.创建声纹特征库 createGroup
    # 2.添加音频特征 createFeature
    # 3.查询特征列表 queryFeatureList
    # 4.特征比对1:1 searchScoreFea
    # 5.特征比对1:N searchFea
    # 6.更新音频特征 updateFeature
    # 7.删除指定特征 deleteFeature
    # 8.删除声纹特征库 deleteGroup
    # 9.音频base64编码后数据(不超过4M),音频格式需要16K、16BIT的MP3音频

    return None


def encode(input_audiopath):
    filename = os.path.basename(input_audiopath)
    if filename.endswith(".wav"):
        audio = AudioSegment.from_wav(input_audiopath)
        audio = audio.set_frame_rate(16000).set_sample_width(2)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        audio_outputfolder = "Recognition\\temporary_audio"
        mp3_output_path = os.path.join(audio_outputfolder, mp3_filename)
        audio.export(mp3_output_path, format="mp3")

        return mp3_output_path


def decode(response):
    response = response
    text = response['payload']['searchScoreFeaRes']['text']
    decoded_text = base64.b64decode(text).decode('utf-8')
    result = json.loads(decoded_text)
    score = result['score']

    return score


def save_scores_to_csv(test_audio_path, reference_audio_paths, output_file):
    APPId = "4a99b8bf"
    APISecret = "YjY5MTYwMzkwZDU5YWI3Y2NkYjY4Nzg5"
    APIKey = "cd660d6d6314c04bfabe16c6a66e1a9a"

    # 创建声纹特征库
    req_url(api_name='createGroup', APPId=APPId, APIKey=APIKey, APISecret=APISecret)

    # 编码测试音频
    test_audio_path = encode(test_audio_path)

    # 检查是否成功编码
    if test_audio_path is None:
        print("测试音频编码失败")
        return

    rows = []  # 用于存储分数和路径的行数据

    # 遍历参考音频和进行五次比较
    for reference_audio_path in reference_audio_paths:

        # 编码参考音频
        reference_audio_path_encoded = encode(reference_audio_path)

        # 检查是否成功编码
        if reference_audio_path_encoded is None:
            print("参考音频编码失败，跳过该文件")
            continue

        scores = []  # 存储五次比较的分数

        for _ in range(5):
            # 添加声纹特征
            gen_req_body(apiname='createFeature', APPId=APPId, file_path=reference_audio_path_encoded)
            req_url(api_name='createFeature', APPId=APPId, APIKey=APIKey, APISecret=APISecret, file_path=reference_audio_path_encoded)

            # 进行声纹识别
            result = req_url(api_name='searchScoreFea', APPId=APPId, APIKey=APIKey, APISecret=APISecret, file_path=test_audio_path)

            # 解码
            score = decode(response=result)

            scores.append(score)

        # 保存分数和路径
        row = [reference_audio_path]
        row.extend(scores)
        rows.append(row)

    # 保存分数和路径到CSV文件
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ["Score_Path"] + [f"Score{i}" for i in range(1, 6)]
        writer.writerow(header)
        writer.writerows(rows)

def find_max_score_from_csv(csv_file):
    max_score = 0.0
    max_score_path = ""

    with open(csv_file, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Read header row

        for row in reader:
            score_path, *scores = row
            scores = list(map(float, scores))
            max_score_for_path = max(scores)

            if max_score_for_path > max_score:
                max_score = max_score_for_path
                max_score_path = score_path

    return max_score, max_score_path



def result_display():
    file_path = "Recognition\\temporary_audio\\scores.csv"
    max_score, max_score_path = find_max_score_from_csv(file_path)

    if max_score_path:
        max_score_filename = os.path.basename(max_score_path)  
        max_score_filename_no_extension = os.path.splitext(max_score_filename)[0]

        if max_score_filename_no_extension=="Hui_Zhao":
            #print(f"相似度: {max_score}")
            #print(f"预测结果: 赵慧")
            result = f"相似度: {max_score}\n预测结果: 赵慧"

        elif max_score_filename_no_extension=="Jiajia_Hu":
            #print(f"相似度: {max_score}")
            #print(f"预测结果: 胡佳佳")
            result = f"相似度: {max_score}\n预测结果: 胡佳佳"

        elif max_score_filename_no_extension=="Junjia_Ma":
            #print(f"相似度: {max_score}")
            #print(f"预测结果: 马俊佳")
            result = f"相似度: {max_score}\n预测结果: 马俊佳"

        elif max_score_filename_no_extension=="Zhenjie_Ma":
            #print(f"相似度: {max_score}")
            #print(f"预测结果: 马振杰")
            result = f"相似度: {max_score}\n预测结果: 马振杰"

        elif max_score_filename_no_extension=="Wenhao_Liu":
            #print(f"相似度: {max_score}")
            #print(f"预测结果: 刘文豪")
            result = f"相似度: {max_score}\n预测结果: 刘文豪"

    else:
        #print("No scores found in the file.")
        result = "No scores found in the file."

    return result


def predicted(test_audio_path):

    reference_audio_paths = [
    "Recognition\\original_audio\\Hui_Zhao.wav",
    "Recognition\\original_audio\\Jiajia_Hu.wav",
    "Recognition\\original_audio\\Junjia_Ma.wav",
    "Recognition\\original_audio\\Wenhao_Liu.wav",
    "Recognition\\original_audio\\Zhenjie_Ma.wav",
    ]

    output_file = "Recognition\\temporary_audio\\scores.csv"
    save_scores_to_csv(test_audio_path, reference_audio_paths, output_file)
    return result_display()



