#Libraries
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
class HelpWindow:
    def __init__(self):
        self.__loadGUI__()
    def __loadGUI__(self):
        self.frame = QtWidgets.QMainWindow()
        self.frame.resize(420, 150)
        self.frame.setWindowTitle("About")
        self.frame.setMinimumSize(QtCore.QSize(420, 150))
        self.frame.setMaximumSize(QtCore.QSize(420, 150))

        #Software name label
        self.label_name = QtWidgets.QLabel(self.frame)
        self.label_name.setGeometry(QtCore.QRect(5, 0, 250, 30))
        self.label_name.setText("Software: cTrader - Portfolio Manager")

        #Software version
        self.label_name = QtWidgets.QLabel(self.frame)
        self.label_name.setGeometry(QtCore.QRect(5, 12, 250, 30))
        self.label_name.setText("Version: 1.0.0 beta")

        #Bug notice_text
        self.bug_notice_text = QtWidgets.QLabel(self.frame)
        self.bug_notice_text.setGeometry(QtCore.QRect(5, 30, 400, 30))
        self.bug_notice_text.setText("If you notice a bug, malfunctions or propose new implementations, send a mail to:")

        #Bug mail_0
        self.mail_label_0 = QtWidgets.QLabel(self.frame)
        self.mail_label_0.setGeometry(QtCore.QRect(5, 40, 250, 30))
        self.mail_label_0.setText("info@tradingsystemsforyou.com")

        #Bug mail_1
        self.mail_label_1 = QtWidgets.QLabel(self.frame)
        self.mail_label_1.setGeometry(QtCore.QRect(5, 52, 250, 30))
        self.mail_label_1.setText("genlabtechita@gmail.com")

        #Separator
        self.sep = QtWidgets.QLabel(self.frame)
        self.sep.setGeometry(QtCore.QRect(0, 64, 450, 30))
        self.sep.setText("____________________________________________________________________________________________________________________________")

        #Realized_label
        self.real_label = QtWidgets.QLabel(self.frame)
        self.real_label.setGeometry(QtCore.QRect(5, 82, 450, 30))
        self.real_label.setText("Software realized by GEN LAB for TSFY - Robot trading")
        #website_0
        self.website_label_0 = QtWidgets.QLabel(self.frame)
        self.website_label_0.setGeometry(QtCore.QRect(5, 94, 450, 30))
        urlLink="<a href=\"http://www.tradingsystemsforyou.com\">www.tradingsystemsforyou.com</a>"
        self.website_label_0.setText(urlLink)
        self.website_label_0.setOpenExternalLinks(True)
        #website_1
        self.website_label_1 = QtWidgets.QLabel(self.frame)
        self.website_label_1.setGeometry(QtCore.QRect(5, 106, 450, 30))
        urlLink="<a href=\"http://www.genlabtech.net\">www.genlabtech.net</a>"
        self.website_label_1.setText(urlLink)
        self.website_label_1.setOpenExternalLinks(True)
        
        self.frame.show()