'''
author：张帆
这个脚本爬取易视腾“企业学院”，分析json文件获取所有视频/图片的下载地址
'''
import requests
import json
from copy import deepcopy
import time

# 分析出的目录id
# 获取地址：http://cosepg.public.taipan.bcs.ottcn.com:8084/ysten-epg/epg/getCatgInfo.shtml?abilityString=%7B%22deviceGroupIds%22%3A%5B%221746%22%5D%2C%22userGroupIds%22%3A%5B%5D%2C%22districtCode%22%3A%22110000%22%2C%22abilities%22%3A%5B%224K-1%7Ccp-TENCENT%22%5D%2C%22businessGroupIds%22%3A%5B%5D%7D&templateId=21600137
catgIds = [2220684, 2220685, 2220686, 2220688,
           2220691, 2220693, 2220694, 2220695]

# epg系统，请求某目录资源列表
urlCatg = "http://cosepg.public.taipan.bcs.ottcn.com:8084/ysten-epg/epg/getPsList.shtml"
# epg系统，请求某个资源的详情
urlPs = 'http://cosepg.public.taipan.bcs.ottcn.com:8084/ysten-epg/epg/getDetail.shtml'

# 请求目录资源列表的参数
payloadCatg = {'templateId': '21600137', 'pageSize': '240', 'pageNo': '1',
               'abilityString': '%7B%22deviceGroupIds%22%3A%5B%221746%22%5D%2C%22userGroupIds%22%3A%5B%5D%2C%22districtCode%22%3A%22110000%22%2C%22abilities%22%3A%5B%224K-1%7Ccp-TENCENT%22%5D%2C%22businessGroupIds%22%3A%5B%5D%7D'}
# 请求资源详情的参数
payloadPs = {'abilityString': '%7B%22deviceGroupIds%22%3A%5B%221746%22%5D%2C%22userGroupIds%22%3A%5B%5D%2C%22districtCode%22%3A%22110000%22%2C%22abilities%22%3A%5B%224K-1%7Ccp-TENCENT%22%5D%2C%22businessGroupIds%22%3A%5B%5D%7D', 'templateId': '21600137'}

# 伪装请求头，把自己模拟成安卓设备
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'}

for catg in catgIds:
    realpayload = deepcopy(payloadCatg)
    realpayload['catgId'] = str(catg)
    r = requests.get(urlCatg, params=realpayload, headers=headers)
    res1 = json.loads(r.content.decode(encoding='utf-8'))
    print(f'目录ID：{catg}')
    for ps in res1["programSeries"]:
        realpayloadPs = deepcopy(payloadPs)
        realpayloadPs['psId'] = ps['psId']
        r = requests.get(urlPs, params=realpayloadPs, headers=headers)
        res2 = json.loads(r.content.decode(encoding='utf-8'))
        print(f"资源id：{ps['name']}")
        print(res2['data']['contentSource'])
        print(res2['data']['hImg'])
        print(res2['data']['vImg'])
        for source in res2['data']['sources']:
            print(source['name'], source['actionURL'])
        print()
    print("***********************************************************************************")
    print()
