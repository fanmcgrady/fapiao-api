import copy
import glob
import json
import os
import sys
import time

import cv2
import numpy as np

from TicToc import Timer
# 二维码
from gaolin.scanQRCode import JsonInterface
from home import views


def getArrayFromStr(strRes):
    sR = copy.deepcopy(strRes)
    index = sR.find(',', 0)
    resultArray = []
    while index >= 0:
        resultArray.append(sR[:index])
        sR = sR[index + 1:]
        index = sR.find(',', 0)
    resultArray.append(sR)
    return resultArray


def scanQRc(filepath):
    from gaolin.scanQRCode.scan_qrcode import recog_qrcode, recog_qrcode_ex

    image = cv2.imread(filepath, 0)

    str_info, position, state = recog_qrcode(image, roi=None)
    print("info:", str_info)
    print("pos:", position)

    # ***** if conventnal method is invalid ******
    # ***** then use the enhanced method   *******
    if str_info is '':
        height, width = image.shape[:2]
        roi = [0, 0, int(width / 4), int(height / 4)]
        # roi = None
        str_info, position, state = recog_qrcode_ex(image, roi)
        print("info(ex):", str_info)
        print("pos(ex):", position)
    # ***** **************************************

    return str_info, position


# 识别二维码
def runQR(filepath):
    try:
        info, position = scanQRc(filepath)
        print("info: {}, position: {}".format(info, position))
    except Exception as e:
        print(e)
        return None

    if info != '':

        resArray = getArrayFromStr(info)
        # js = InterfaceType.JsonInterface.invoice()
        js = JsonInterface.invoice()
        js.setVATInvoiceFromArray(resArray, "special")

        jsoni = js.dic['invoice']
        print(jsoni)
        return json.dumps(jsoni).encode().decode("unicode-escape")
    else:
        return None


# 识别类型
def runType(filepath, image_width=512, image_height=512):
    try:
        # im = caffe.io.load_image(filepath)
        ## load image with OpenCV
        im = cv2.imread(filepath)
        im = cv2.resize(im, (image_width, image_height))
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = im.astype(np.float32)
        im_max = np.max(im)
        im_min = np.min(im)
        im = (im - im_min) / (im_max - im_min)

        invoice_type = ['other', 'special', 'quota']
        index = views.global_recog(im)
        print("recog index: {}".format(index))
        if index < 0:
            return "other"
        typeP = invoice_type[index]
    except Exception as e:
        print(e)
        return "other"

    return typeP


if __name__ == '__main__':
    if len(sys.argv) == 3:
        image_path = sys.argv[1]
        image_type = sys.argv[2]
    else:
        print('use default args: path, type')
        image_path = '/home/public/Pics/Normal.1006.20190302/'
        image_type = '01'

    im_names = glob.glob(os.path.join(image_path, "*.jpg"))
    iSum = len(im_names)
    iLoop = 0
    iCorr = 0
    for filename in im_names:

        # if test be limited for 30 pieces uncomment flow 2 line
        #        if ((iLoop + 1) > 3):
        #            break
        # limited end
        iLoop += 1
        # print(run_qrcode(filename))
        # print(filename)
        sTime = time.time()
        detType = runType(filename)
        eTime = time.time()
        dTime = int((eTime - sTime) * 1000)
        if detType == 'special':
            detType = '01'
        else:
            detType = '00'

        if (detType == image_type):
            # Type Match : /home/public/Pics/Normal.268.20181213.Color/20181119_fuhua_2018111914543230.jpg
            print(dTime, 'ms, Match  :', filename)
            iCorr += 1
        else:
            # Type:   00 : /home/public/Pics/Special.14.20181226/Image_00013.jpg
            print(dTime, 'ms, Get', detType, ':', filename)

    print('------------------------------')
    print('Sum:', iLoop, ', Correct:', iCorr, ', Rate: ', int(iCorr * 100 / iLoop), '%')
    print('------------------------------')
