import sys

import cv2
import numpy as np
import os
from cv2 import dnn

FILE_DIR = os.path.dirname(os.path.realpath(__file__))


class InvoiTypeRecog():
    def __init__(self, \
                 model_def=FILE_DIR + '/' + 'models/fapiao_type.prototxt', \
                 model_weights=FILE_DIR + '/' + 'models/fapiao_type_4500.caffemodel'):

        self.model_def = model_def
        self.model_weights = model_weights

        self.type = -1
        self.threshold = 0.5

    def __call__(self, image):
        self.predictions = self.recog(image)
        return self.type

    def recog(self, image):
        blob = dnn.blobFromImage(image, 1, (256, 256), (104, 117, 123))
        net = dnn.readNetFromCaffe(self.model_def, self.model_weights)
        net.setInput(blob)
        prob = net.forward()
        if np.max(prob) > self.threshold:
            self.type = np.argmax(prob)
        else:
            self.type = -1
            print('No Invoice Found.')
        return self.type


if __name__ == "__main__":
    print('args: image_path[option]')
    if len(sys.argv) == 2:
        image_path = sys.argv[1]
    else:
        image_path = '/home/public/Pics/Special.30.20181203/'

    recog = InvoiTypeRecog()
    import glob

    im_names = glob.glob(os.path.join(image_path, "*.jpg"))

    '''
    Type of Invoice
    '''
    invoice_type = ['quota', 'elect', 'airticket', 'spec_and_normal', 'spec_and_normal_bw', 'trainticket']
    for im_name in im_names:
        im = cv2.imread(im_name)
        index = recog(im)
        if index > 0:
            print(invoice_type[index])

