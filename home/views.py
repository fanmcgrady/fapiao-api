# 设置只用前两个GPU
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

# 分类
# 加载fp
import shutil
import sys
import zipfile

sys.path.append("/home/ocr/fapiao/fp")
from fp.TextBoxes import recog_invoice_type
global_recog = recog_invoice_type.InvoiTypeRecog()

import API
import datetime
import json
import base64

from django.http import JsonResponse, HttpResponse
import traceback
from django.shortcuts import render

def index(request):
    return render(request, 'allInOne.html')

def testType(request):
    ret = {}
    try:
        # POST压缩包中的文件
        filename = request.POST['fileInZip']

        # 文件已通过getFileList方法上传到upload目录，此时不需要上传了
        # 拼接目录
        file_path = os.path.join('upload', filename)
        full_path = os.path.join('allstatic', file_path)

        ret = API.runType(full_path)

    except Exception as e:
        traceback.print_exc()

    return HttpResponse(json.dumps(ret))

# 批量上传获取文件列表
def getFileList(request):
    if request.method == "POST":
        # 是否使用服务器上的文件，第二个参数是默认值false
        try:
            use_server_path = request.POST.get('useServerPath', 'false')

            if use_server_path == 'true':
                # 随机文件名
                server_path = request.POST['pathInput']
                filename, zip_dir = generate_random_name(server_path)
                # 拼接存放位置路径
                file_path = os.path.join('upload', filename)
                full_path = os.path.join('allstatic', file_path)

                shutil.copyfile(server_path, full_path)  # 复制文件
            else:
                obj = request.FILES.get('fapiao')
                # 随机文件名
                filename, zip_dir = generate_random_name(obj.name)
                # 拼接存放位置路径
                file_path = os.path.join('upload', filename)
                full_path = os.path.join('allstatic', file_path)

                # 上传文件写入
                f = open(full_path, 'wb')
                for chunk in obj.chunks():
                    f.write(chunk)
                f.close()
        except Exception as e:
            traceback.print_exc()

        file_list = []

        try:
            # 是否是zip文件，批量
            if os.path.splitext(full_path)[1] == '.zip':
                # 读zip文件
                file_zip = zipfile.ZipFile(full_path, 'r')
                # 拼接处理后图片路径
                upload_dir = os.path.join('allstatic/upload', zip_dir)
                out_dir = os.path.join('allstatic/out', zip_dir)
                line_dir = os.path.join('allstatic/line', zip_dir)

                # 遍历压缩包内文件 判断扩展名只要图片
                for file in file_zip.namelist():
                    if file.endswith('.jpg') or \
                            file.endswith('.jpeg') or \
                            file.endswith('.png') or \
                            file.endswith('.bmp'):

                        # 创建三个目录 存放压缩包内所有图片的分析后文件
                        upload_file = os.path.join(upload_dir, file)
                        upload_file_root, _ = os.path.split(upload_file)
                        out_file = os.path.join(out_dir, file)
                        out_file_root, _ = os.path.split(out_file)
                        line_file = os.path.join(line_dir, file)
                        line_file_root, _ = os.path.split(line_file)

                        if not os.path.exists(upload_file_root):
                            os.makedirs(upload_file_root)
                        if not os.path.exists(out_file_root):
                            os.makedirs(out_file_root)
                            os.makedirs(os.path.join(out_file_root, 'tmp'))
                        if not os.path.exists(line_file_root):
                            os.makedirs(line_file_root)

                        # 解压到上传目录
                        file_zip.extract(file, upload_dir)
                        file_with_zipfold = os.path.join(zip_dir, file)
                        file_list.append(file_with_zipfold)
                file_zip.close()
                # 清除完整路径
                os.remove(full_path)
            else:
                # 单个处理
                file_list.append(filename)

            # 向前端传值
            ret = {
                'status': True,
                'path': file_path,
                'out': file_list
            }
            # 打印错误内容
        except Exception as e:
            print(e)
            ret = {'status': False, 'path': file_path, 'out': str(e)}

        return HttpResponse(json.dumps(ret))


# API
def QR_API(request):
    if request.method == "POST":
        try:
            base64_data = request.POST['picture']
            # 随机文件名
            filename, _ = generate_random_name()
            # 拼接存放位置路径
            file_path = os.path.join('upload', filename)
            full_path = os.path.join('allstatic', file_path)

            # 文件写入
            with open(full_path, "wb") as f:
                f.write(base64.b64decode(base64_data))
        except Exception as e:
            traceback.print_exc()

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

        # 删除文件
        if (os.path.exists(full_path)):
            os.remove(full_path)

        return JsonResponse(ret)


def Type_API(request):
    if request.method == "POST":
        try:
            base64_data = request.POST['picture']
            # 随机文件名
            filename, _ = generate_random_name()
            # 拼接存放位置路径
            file_path = os.path.join('upload', filename)
            full_path = os.path.join('allstatic', file_path)

            # 文件写入
            with open(full_path, "wb") as f:
                f.write(base64.b64decode(base64_data))
        except Exception as e:
            traceback.print_exc()

        try:
            # 识别 给前端传值
            type = API.runType(full_path)
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

            # if type == 'quota':
            #     type = "95"
            # elif type == 'elect':
            #     type = "10"
            # elif type == 'airticket':
            #     type = "93"
            # elif type == 'special':
            #     type = "01"
            # elif type == 'trainticket':
            #     type = "92"
            # else:
            #     type = "00"

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

        # 删除文件
        # if (os.path.exists(full_path)):
        #     os.remove(full_path)

        return JsonResponse(ret)


# 按日期生成文件名
def generate_random_name(file_name=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if file_name is None:
        ext = ".jpg"
    else:
        _, ext = os.path.splitext(file_name)

    return timestamp + ext, timestamp
