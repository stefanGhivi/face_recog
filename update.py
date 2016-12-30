import getopt
import cv2
import numpy as np
import sys

from PIL import Image

from Photo import Photo
from database import create

recognizer = cv2.createLBPHFaceRecognizer()
args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
args = dict(args)
cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")
cascade = cv2.CascadeClassifier(cascade_fn)


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def update(image, name):
    image = Image.open(image).convert('L')
    image = np.array(image, 'uint8')
    recognizer.load('saved_recognizer.xml')
    faces = detect(image, cascade)
    if len(faces) >= 2 or len(faces) == 0 or not faces:
        raise Exception("Incorrect number of faces detected")

    photo = Photo(0, name, image)
    person_id = create(photo)

    (x, y, w, h) = faces
    cv2.imshow("Training image...", image[y: y + h, x: x + w])
    cv2.waitKey(50)
    recognizer.update([image[y: y + h, x: x + w], ], np.array(person_id))
    recognizer.save('saved_recognizer.xml')
