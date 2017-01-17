
import cv2

import cv2
import predict
import getopt
import cv2
import numpy as np
import sys
import os
from PIL import Image

from Photo import Photo
from database import create, read


def get_photo():

    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)
    valid_image = False
    while valid_image == False:
        camera_capture = get_image(camera)
        file = "test_image.png"
        cv2.imwrite(file, camera_capture)
        image = Image.open("test_image.png").convert('L')
        image = np.array(image, 'uint8')
        if len(predict.detect(image, predict.cascade)) != 1:
            print "no face detected"
            os.remove("test_image.png")
        else:
            print 'face detected'
            valid_image = True
    # for i in xrange(ramp_frames):
    #     temp = get_image(camera)
    print("Taking image...")
    camera_capture = get_image(camera)
    file = "test_image.png"
    cv2.imwrite(file, camera_capture)
    return camera_capture

def get_image(camera):
    retval, im = camera.read()
    return im


def get_photos_for_update():
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    args = dict(args)
    cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")
    cascade = cv2.CascadeClassifier(cascade_fn)
    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)
    # for i in xrange(ramp_frames):
    #     temp = get_image(camera)
    number_of_photos_desired = 15
    while number_of_photos_desired != 0:
        camera_capture = get_image(camera)
        file = "test_folder/test_image{0}.png".format(number_of_photos_desired)
        cv2.imwrite(file, camera_capture)
        image = Image.open("test_folder/test_image{0}.png".format(number_of_photos_desired)).convert('L')
        image = np.array(image, 'uint8')
        if len(predict.detect(image, predict.cascade)) != 1:
            print "no face detected"
            os.remove("test_folder/test_image{0}.png".format(number_of_photos_desired))
        else:
            print 'face detected'
            number_of_photos_desired -= 1







