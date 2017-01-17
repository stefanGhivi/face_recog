# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_version2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
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
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.predict_button = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.predict_button.sizePolicy().hasHeightForWidth())
        self.predict_button.setSizePolicy(sizePolicy)
        self.predict_button.setMinimumSize(QtCore.QSize(200, 20))
        self.predict_button.setMaximumSize(QtCore.QSize(200, 20))
        self.predict_button.setObjectName(_fromUtf8("predict_button"))
        self.predict_button.clicked.connect(self.predict)
        self.verticalLayout.addWidget(self.predict_button)
        self.update_button = QtGui.QPushButton(self.centralwidget)
        self.update_button.setMinimumSize(QtCore.QSize(200, 20))
        self.update_button.setMaximumSize(QtCore.QSize(200, 20))
        self.update_button.setObjectName(_fromUtf8("update_button"))
        self.update_button.clicked.connect(self.update)
        self.verticalLayout.addWidget(self.update_button)
        self.employee_label = QtGui.QLabel(self.centralwidget)
        self.employee_label.setMinimumSize(QtCore.QSize(200, 20))
        self.employee_label.setMaximumSize(QtCore.QSize(200, 20))
        self.employee_label.setObjectName(_fromUtf8("employee_label"))
        self.verticalLayout.addWidget(self.employee_label, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.employee_name_field = QtGui.QLineEdit(self.centralwidget)
        self.employee_name_field.setMinimumSize(QtCore.QSize(200, 20))
        self.employee_name_field.setMaximumSize(QtCore.QSize(200, 24))
        self.employee_name_field.setObjectName(_fromUtf8("employee_name_field"))
        self.verticalLayout.addWidget(self.employee_name_field)
        self.restart_button = QtGui.QPushButton(self.centralwidget)
        self.restart_button.setMinimumSize(QtCore.QSize(200, 20))
        self.restart_button.setMaximumSize(QtCore.QSize(200, 20))
        self.restart_button.setObjectName(_fromUtf8("restart_button"))
        self.restart_button.clicked.connect(self.reset)
        self.verticalLayout.addWidget(self.restart_button)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.predicted_image = QtGui.QLabel(self.centralwidget)
        self.predicted_image.setAlignment(QtCore.Qt.AlignCenter)
        self.predicted_image.setObjectName(_fromUtf8("predicted_image"))
        self.horizontalLayout.addWidget(self.predicted_image)
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
        self.update_button.setText(_translate("MainWindow", "Upload", None))
        self.employee_label.setText(_translate("MainWindow", "Employee name", None))
        self.restart_button.setText(_translate("MainWindow", "Restart", None))
        self.predicted_image.setText(_translate("MainWindow", "TextLabel", None))
        self.start_video()


    def start_video(self):
        self.capture = None
        if not self.capture:
            self.capture = QtCapture(self.label)
            # self.capture.setFPS(1)
        self.capture.start()
        # self.capture.show()


    def update(self):
        self.capture.stop()
        self.capture.deleteLater()
        TakePhoto.get_photos_for_update()
        update.update('test_folder', str(self.employee_name_field.text()))

        self.start_video()


    def predict(self):
        # self.predicted_image.setMinimumWidth(self.label.frameGeometry().width())
        # self.predicted_image.setMinimumHeight(self.label.frameGeometry().height())
        self.capture.stop()
        self.capture.deleteLater()
        TakePhoto.get_photo()
        try:
            photo, name = predict.predict('test_image.png')
            fh = open("image_to_save.png", "wb")
            fh.write(photo.decode('base64'))
            fh.close()

            # os.remove('test_image.png')

            self.predicted_image.setPixmap(QtGui.QPixmap('image_to_save.png'))
            # os.remove('image_to_save.png')
            self.predicted_image.show()
        except Exception as e:
            print e
        self.start_video()

    def reset(self):
        self.predicted_image.hide()
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