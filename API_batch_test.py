# 增值税发票二维码识别接口
import base64
import os
import sys
import glob

import requests

HOST = "http://202.115.103.60:8000"


# 发票二维码识别接口
def run_qrcode(file_name):
    url = HOST + '/qr_api'

    with open(file_name, "rb") as f:
        base64_data = base64.b64encode(f.read())

    params = {
        'picture': base64_data
    }

    response = requests.post(url, data=params)
    return response.json()


# 发票分类接口
def run_type(file_name):
    url = HOST + '/type_api'

    with open(file_name, "rb") as f:
        base64_data = base64.b64encode(f.read())

    params = {
        'picture': base64_data
    }

    response = requests.post(url, data=params)
    return response.json()


if __name__ == '__main__':
    print('args: image_path[option]')
    if len(sys.argv) == 2:
        image_path = sys.argv[1]
    else:
        image_path = '/home/public/Pics/Special.30.20181203/'

    im_names = glob.glob(os.path.join(image_path, "*.jpg"))
    for filename in im_names:
        print(run_qrcode(filename))
        print(run_type(filename))

