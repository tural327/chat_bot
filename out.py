# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graf.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(522, 510)
        self.message_line = QtWidgets.QLineEdit(Form)
        self.message_line.setGeometry(QtCore.QRect(20, 440, 331, 51))
        self.message_line.setObjectName("message_line")
        self.Send = QtWidgets.QPushButton(Form)
        self.Send.setGeometry(QtCore.QRect(360, 440, 141, 51))
        self.Send.setAutoFillBackground(False)
        self.Send.setObjectName("Send")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 341, 421))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Send.setText(_translate("Form", "SEND"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
