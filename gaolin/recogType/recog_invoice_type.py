import numpy as np
import os

os.environ['GLOG_minloglevel'] = '3'

import sys
import glob
import caffe

FILE_DIR = os.path.dirname(os.path.realpath(__file__))


class InvoiTypeRecog():
    def __init__(self, \
                 model_def=FILE_DIR + '/' + 'models/fapiao_type.prototxt', \
                 model_weights=FILE_DIR + '/' + 'models/fapiao_type_4500.caffemodel', \
                 mean_file=FILE_DIR + '/' + 'models/fapiao_mean.binaryproto'):

        if True:
            caffe.set_device(1)
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()

        self.model_def = model_def
        self.model_weights = model_weights
        self.net = caffe.Net(model_def, model_weights, caffe.TEST)

        mean_blob = caffe.proto.caffe_pb2.BlobProto()
        mean_blob.ParseFromString(open(mean_file, 'rb').read())
        mean_npy = caffe.io.blobproto_to_array(mean_blob)
        self.mean = mean_npy[0, :, 0, 0]

        self.type = -1
        self.threshold = 0.5

    def __call__(self, image):
        self.predictions = self.recog(image)
        return self.type

    def recog(self, image):
        net = self.net
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        transformer.set_transpose('data', (2, 0, 1))
        transformer.set_mean('data', self.mean)
        transformer.set_raw_scale('data', 255.0)
        transformer.set_channel_swap('data', (2, 1, 0))
        net.blobs['data'].data[...] = transformer.preprocess('data', image)
        predict = net.forward()
        prob = net.blobs['prob'].data[0].flatten()
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
    im_names = glob.glob(os.path.join(image_path, "*.jpg"))
    '''
    Type of Invoice
    '''
    invoice_type = ['quota', 'elect', 'airticket', 'spec_and_normal', 'spec_and_normal_bw', 'trainticket']
    for im_name in im_names:
        im = caffe.io.load_image(im_name)
        index = recog(im)
        if index > 0:
            print(invoice_type[index])
