from PyQt4 import QtCore, QtGui
import cv2
import cv2.cv as cv

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''


class QtCapture(QtGui.QWidget):
    def __init__(self, label):
        super(QtGui.QWidget, self).__init__()
        self.fps = 24
        self.cap = cv2.VideoCapture(0)
        self.video_frame = label

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        import sys, getopt
        args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
        args = dict(args)

        cascade_fn = args.get('--cascade', "data/haarcascades/haarcascade_frontalface_alt.xml")

        cascade = cv2.CascadeClassifier(cascade_fn)
        ret, frame = self.cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        rects = detect(gray, cascade)
        draw_rects(frame, rects, (0, 255, 0))

        frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000. / self.fps)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(200, 200),maxSize=(250,250),
                                     flags=cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
