import copy
import json
import cv2

# 二维码
from gaolin.scanQRCode import JsonInterface

# 分类
# 加载fp
import sys
sys.path.append("/home/ocr/fapiao/fp")
from fp.TextBoxes import recog_invoice_type

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
    except:
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
def runType(filepath):
    try:
        recog = recog_invoice_type.InvoiTypeRecog()
        import caffe
        im = caffe.io.load_image(filepath)

        invoice_type = ['other', 'spec_and_normal']
        index = recog(im)
        print("recog index: {}".format(index))
        if index < 0:
            return "other"
        typeP = invoice_type[index]
    except:
        return "other"

    if typeP == 'spec_and_normal' or typeP == 'spec_and_normal_bw':
        typeP = 'special'

    return typeP


if __name__ == '__main__':
    filepath = "Image_00175.jpg"
    runType(filepath)
