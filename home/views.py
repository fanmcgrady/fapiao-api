# 设置只用前两个GPU
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

import API
import datetime
import json
import base64

from django.http import JsonResponse


# API
def QR_API(request):
    if request.method == "POST":
        base64_data = request.POST['picture']
        # 随机文件名
        filename, _ = generate_random_name()
        # 拼接存放位置路径
        file_path = os.path.join('upload', filename)
        full_path = os.path.join('allstatic', file_path)

        # 文件写入
        with open(full_path, "wb") as f:
            f.write(base64.b64decode(base64_data))

        try:
            # 识别 给前端传值
            json_result = API.runQR(full_path)

            if json_result is None:
                ret = {
                    "returnStateInfo": {
                        "returnCode": "9999",
                        "returnMessage": "处理失败: 二维码识别不清晰，识别失败"
                    },
                    "invoice": ""
                }
            else:
                ret = {
                    "returnStateInfo": {
                        "returnCode": "0000",
                        "returnMessage": "处理成功"
                    },
                    "invoice": json.loads(str(json_result).replace("'", "\""))
                }

        # 打印错误原因
        except Exception as e:
            print(e)
            ret = {
                "returnStateInfo": {
                    "returnCode": "9999",
                    "returnMessage": "处理失败:" + str(e)
                },
                "invoice": ""
            }

        return JsonResponse(ret)


def Type_API(request):
    if request.method == "POST":
        base64_data = request.POST['picture']
        # 随机文件名
        filename, _ = generate_random_name()
        # 拼接存放位置路径
        file_path = os.path.join('upload', filename)
        full_path = os.path.join('allstatic', file_path)

        # 文件写入
        with open(full_path, "wb") as f:
            f.write(base64.b64decode(base64_data))

        try:
            # 识别 给前端传值
            type = API.runTypeWithCV(full_path)
            # ['quota', 'elect', 'airticket', 'special', 'trainticket']
            # 01 *增值税专用发票
            # 02 货运运输业增值税专用发票
            # 03 机动车销售统一发票
            # 04 *增值税普通发票
            # 10 *增值税普通发票(电子)
            # 11 *增值税普通发票(卷式)
            # 91 出租车票
            # 92 *火车票
            # 93 *飞机票
            # 94 汽车票
            # 95 *定额发票
            # 96 长途汽车票
            # 97 通用机打发票
            # 98 政府非税收收入一般缴款书
            # 00 其他类型
            # 注：增值税票目前不能区分具体种类，可统一返回01

            if type == 'quota':
                type = "95"
            elif type == 'elect':
                type = "10"
            elif type == 'airticket':
                type = "93"
            elif type == 'special':
                type = "01"
            elif type == 'trainticket':
                type = "92"
            else:
                type = "00"

            ret = {
                "returnCode": "0000",
                "returnMessage": "处理成功",
                "invoiceType": type
            }

        # 打印错误原因
        except Exception as e:
            print(e)
            ret = {
                "returnCode": "9999",
                "returnMessage": "处理失败:" + str(e),
                "invoiceType": type
            }

        return JsonResponse(ret)


# 按日期生成文件名
def generate_random_name(file_name=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if file_name is None:
        ext = ".jpg"
    else:
        _, ext = os.path.splitext(file_name)

    return timestamp + ext, timestamp
