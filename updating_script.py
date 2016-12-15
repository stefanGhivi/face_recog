#!/usr/bin/python

# Import the required modules
import getopt

import cv2, os
import numpy as np
import sys
from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV.

# For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects

args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])

args = dict(args)
cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")

cascade = cv2.CascadeClassifier(cascade_fn)

test_termination = '.test'


def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .test extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith(test_termination)]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject_", ""))
        # Detect the face in the image
        #////////faces = faceCascade.detectMultiScale(image)
        faces = detect(image, cascade)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            #images.append(image[y: y + h, x: x + w])
            #labels.append(nbr)
            cv2.imshow("Training image...", image[y: y + h, x: x + w])
            cv2.waitKey(50)
            recognizer.train(images, np.array(labels))
    # return the images list and labels list
    return images, labels

# Path to the Dataset
path = './codegile_faces'
# Call the get_images_and_labels function and get the face images and the
# corresponding labels
images, labels = get_images_and_labels(path)
cv2.destroyAllWindows()

# Perform the tranining
recognizer.train(images, np.array(labels))

# Append the images with the extension .test into image_paths
image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(test_termination)]
for image_path in image_paths:
    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    #faces = faceCascade.detectMultiScale(predict_image)
    faces = detect(predict_image, cascade)
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject_", ""))
        if nbr_actual == nbr_predicted:
            print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
            cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
            cv2.waitKey(1000)
        else:
            print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)


