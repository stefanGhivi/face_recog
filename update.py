import getopt
import cv2
import numpy as np
import sys

from PIL import Image

from Photo import Photo
from database import create
import os

args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
args = dict(args)
cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")
cascade = cv2.CascadeClassifier(cascade_fn)


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(200, 200), maxSize=(250, 250),
                                     flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def update(path, name):
    person_id = 0
    recognizer = cv2.createLBPHFaceRecognizer(threshold=20.00)
    loaded = False
    try:
        recognizer.load('saved_recognizer.xml')
        loaded = True
    except:
        None
    image_paths=[os.path.join(path,f) for f in os.listdir(path)]
    c=0
    images = []
    labels = []
    for image_path in image_paths:

        image = Image.open(image_path).convert('L')
        image = np.array(image, 'uint8')
        faces = detect(image, cascade)
        if len(faces) >= 2 or len(faces) == 0 or not faces.any:
            raise Exception("Incorrect number of faces detected")
        if c==0 :
            photo = Photo(0, name, image)
            person_id = create(photo)
            c=1
        (x, y, w, h) = faces[0]
        images.append(image[y: y + h, x: x + w])
        labels.append(person_id)
    if loaded:
        recognizer.update(images, np.array(labels))
        print("update person with id  " + str(person_id))
    else:
        recognizer.train(images, np.array(labels))
        print("train person with id  " + str(person_id))

    recognizer.save('saved_recognizer.xml')