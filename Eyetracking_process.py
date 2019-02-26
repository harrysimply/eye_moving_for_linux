# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Eyetracking_process.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(810, 474)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(630, 90, 151, 151))
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(250, 90, 171, 161))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 90, 161, 161))
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(40, 30, 111, 16))
        self.label_6.setObjectName("label_6")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 330, 741, 111))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(450, 90, 151, 161))
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(30, 290, 171, 17))
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "TextLabel"))
        self.label_2.setText(_translate("Dialog", "TextLabel"))
        self.label.setText(_translate("Dialog", "TextLabel"))
        self.label_6.setText(_translate("Dialog", "处理的相图："))
        self.label_3.setText(_translate("Dialog", "TextLabel"))
        self.label_4.setText(_translate("Dialog", "TextLabel"))
        self.label_7.setText(_translate("Dialog", "眼动轨迹的时间序列："))

