# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'u2_bmstu.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(791, 410)
        self.start_button = QtWidgets.QPushButton(Form)
        self.start_button.setGeometry(QtCore.QRect(680, 280, 111, 51))
        self.start_button.setObjectName("start_button")
        self.end_button = QtWidgets.QPushButton(Form)
        self.end_button.setGeometry(QtCore.QRect(680, 340, 111, 51))
        self.end_button.setObjectName("end_button")
        self.video_frame = QtWidgets.QLabel(Form)
        self.video_frame.setGeometry(QtCore.QRect(20, 10, 661, 401))
        self.video_frame.setText("")
        self.video_frame.setObjectName("video_frame")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.start_button.setText(_translate("Form", "НАЧАТЬ"))
        self.end_button.setText(_translate("Form", "ЗАВЕРШИТЬ"))
