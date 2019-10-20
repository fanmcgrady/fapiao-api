from OCR import OCR2 as ocrVat
from OCR import OCR3 as veryVat
import sys
sys.path.append("/home/ocr/organize/OCR/OCR_ticket")
from OCR.OCR_ticket import predict
import keras.backend.tensorflow_backend as K
import time
import OCR.OCR_Chinese.predict_single as CH
import cv2
#2019.09.19 wt 载入发票识别使用税号模型
import OCR.tax_model.test_tax as tax


#verify_global_model = veryVat.load_model()
#global_model = ocrVat.load_model()

#tax_model = 0
#import tensorflow as tf
#with tf.device('/gpu:1'):
#    tax_model = tax.load_model()
tax_model = tax.load_model()

# global_model._make_predict_function()
# verify_global_model = veryVat.load_model()
# verify_global_model._make_predict_function()

def OCR(image_path, typeP, attribute, thresholding = 160):
    """
        用来连接OCR调用，通过home/views.py来预加载全局模型
        imgae_path 输入图片路径，识别图片为行提取结果
    """

    time11 = time.time()

    #global verify_global_model
    #global global_model
    global tax_model

    with K.get_session().graph.as_default():
        if typeP == 'normal' and attribute == 'verifyCode':
            print('model:    3_global_model')
            #out, _ = veryVat.predict(image_path, verify_global_model)
            out = tax.predict(image_path, tax_model)
        elif typeP == 'train':
            out = predict.predict_single(image_path)
        else:
            print('model:    global_model')
            #out, _ = ocrVat.predict(image_path, global_model)
            out = tax.predict(image_path, tax_model)

    time12 = time.time()
    print(attribute + ' 识别耗时：   ' + str(time12 - time11))

    return out

# caffe 模型
# import fp.TextBoxes.detect_textline as dt
# global_caffe_model = dt.load_caffe_model()

# wt 2019.09.12 ocr中文模型载入
def netOcr():
    net = CH.Res20_CRNN(input_channels=1, output_channels=1557).cuda()      #char_classes=1557
    path = 'OCR/OCR_Chinese/weights/epoch1_loss_0.038813.pth'    #模型权重路径
    checkpoint = CH.torch.load(path, map_location='cuda:0')
    net.load_state_dict(checkpoint['model_state_dict'])     #加载模型
    net.eval()
    def func(imagePath):
        img = cv2.imread(imagePath, flags=cv2.IMREAD_GRAYSCALE)
        return  CH.predict_single(img, net)
    return func

ChiOcr = netOcr()
#ChiOcr =0 

