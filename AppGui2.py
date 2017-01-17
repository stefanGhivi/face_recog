from PyQt4 import QtCore, QtGui
from QtCapture import QtCapture
import predict
import TakePhoto
import update
import os
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.MainWin=MainWindow
        self.centralwidget = QtGui.QWidget(MainWindow)

        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.predict_button = QtGui.QPushButton(self.centralwidget)
        self.predict_button.setMaximumSize(QtCore.QSize(200, 20))
        self.predict_button.setObjectName(_fromUtf8("predict_button"))
        self.predict_button.clicked.connect(self.predict)
        self.reset_button = QtGui.QPushButton(self.centralwidget)
        self.reset_button.setMaximumSize(QtCore.QSize(200, 20))
        self.reset_button.setObjectName(_fromUtf8("reset button"))
        self.reset_button.clicked.connect(self.reset)
        self.verticalLayout.addWidget(self.predict_button,QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.update_button = QtGui.QPushButton(self.centralwidget)
        self.update_button.setMaximumSize(QtCore.QSize(200, 20))
        self.update_button.setObjectName(_fromUtf8("update_button"))
        self.update_button.clicked.connect(self.update)
        self.verticalLayout.addWidget(self.update_button,QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.employee_label = QtGui.QLabel(self.centralwidget)
        self.employee_label.setMaximumSize(QtCore.QSize(200, 20))
        self.employee_label.setObjectName(_fromUtf8("employee_label"))
        self.verticalLayout.addWidget(self.employee_label, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.employee_name_field = QtGui.QLineEdit(self.centralwidget)
        self.employee_name_field.setMaximumSize(QtCore.QSize(200, 24))
        self.employee_name_field.setObjectName(_fromUtf8("employee_name_field"))
        self.verticalLayout.addWidget(self.employee_name_field,QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.predicted_image = QtGui.QLabel(self.centralwidget)
        self.predicted_image.setObjectName(_fromUtf8("predicted_image"))
        self.horizontalLayout.addWidget(self.predicted_image, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))
        self.predict_button.setText(_translate("MainWindow", "Predict", None))
        self.update_button.setText(_translate("MainWindow", "Update", None))
        self.employee_label.setText(_translate("MainWindow", "Employee name", None))
        self.predicted_image.setText(_translate("MainWindow", "TextLabel", None))
        self.predicted_image.hide()
        self.start_video()

    def start_video(self):
        print 'recording '
        self.capture = None
        if not self.capture:
            self.capture = QtCapture(self.label)
            # self.capture.setFPS(1)
        self.capture.start()
            # self.capture.show()


    def update(self):

        self.capture.stop()
        self.capture.deleteLater()
        TakePhoto.get_photo()
        update.update('test_image.png',str(self.employee_name_field.text()))
        os.remove('test_image.png')
        self.start_video()

    def predict(self):

        # self.predicted_image.setMinimumWidth(self.label.frameGeometry().width())
        # self.predicted_image.setMinimumHeight(self.label.frameGeometry().height())
        self.capture.stop()
        self.capture.deleteLater()
        TakePhoto.get_photo()
        photo,name=predict.predict('test_image.png')
        fh = open("image_to_save.png", "wb")
        fh.write(photo.decode('base64'))
        fh.close()

        # os.remove('test_image.png')

        self.predicted_image.setPixmap(QtGui.QPixmap('image_to_save.png'))
        # os.remove('image_to_save.png')
        self.predicted_image.show()

    def reset(self):
        self.predicted_image.hide()
        self.predicted_image.setVisible(False)
        self.predicted_image.setMaximumHeight(0)
        self.predicted_image.setMaximumWidth(0)
        self.MainWin.resize(self.MainWin.minimumSizeHint())
        # self.predicted_image.setMinimumWidth(self.label.frameGeometry().width())
        # self.predicted_image.setMinimumHeight(self.label.frameGeometry().height())

        self.start_video()
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())