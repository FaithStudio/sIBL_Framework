# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './UI/sIBL_GUI_FTP.ui'
#
# Created: Sat Oct 10 15:52:01 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_sIBL_GUI_FTP_Form(object):
        def setupUi(self, sIBL_GUI_FTP_Form):
                sIBL_GUI_FTP_Form.setObjectName("sIBL_GUI_FTP_Form")
                sIBL_GUI_FTP_Form.resize(394, 245)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/sIBL_GUI FTP/Resources/Icon_Light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                sIBL_GUI_FTP_Form.setWindowIcon(icon)
                self.sIBL_GUI_FTP_Form_gridLayout = QtGui.QGridLayout(sIBL_GUI_FTP_Form)
                self.sIBL_GUI_FTP_Form_gridLayout.setObjectName("sIBL_GUI_FTP_Form_gridLayout")
                self.Logo_horizontalLayout = QtGui.QHBoxLayout()
                self.Logo_horizontalLayout.setObjectName("Logo_horizontalLayout")
                spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                self.Logo_horizontalLayout.addItem(spacerItem)
                self.Logo_label = QtGui.QLabel(sIBL_GUI_FTP_Form)
                self.Logo_label.setPixmap(QtGui.QPixmap(":/sIBL_GUI FTP/Resources/sIBL_GUI_Small_Logo.png"))
                self.Logo_label.setObjectName("Logo_label")
                self.Logo_horizontalLayout.addWidget(self.Logo_label)
                spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                self.Logo_horizontalLayout.addItem(spacerItem1)
                self.sIBL_GUI_FTP_Form_gridLayout.addLayout(self.Logo_horizontalLayout, 0, 0, 1, 1)
                self.Online_Repository_groupBox = QtGui.QGroupBox(sIBL_GUI_FTP_Form)
                self.Online_Repository_groupBox.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
                self.Online_Repository_groupBox.setObjectName("Online_Repository_groupBox")
                self.Online_Repository_groupBox_gridLayout = QtGui.QGridLayout(self.Online_Repository_groupBox)
                self.Online_Repository_groupBox_gridLayout.setObjectName("Online_Repository_groupBox_gridLayout")
                self.Current_File_label = QtGui.QLabel(self.Online_Repository_groupBox)
                self.Current_File_label.setObjectName("Current_File_label")
                self.Online_Repository_groupBox_gridLayout.addWidget(self.Current_File_label, 0, 0, 1, 1)
                self.Download_progressBar = QtGui.QProgressBar(self.Online_Repository_groupBox)
                self.Download_progressBar.setProperty("value", QtCore.QVariant(24))
                self.Download_progressBar.setObjectName("Download_progressBar")
                self.Online_Repository_groupBox_gridLayout.addWidget(self.Download_progressBar, 1, 0, 1, 1)
                self.sIBL_GUI_FTP_Form_gridLayout.addWidget(self.Online_Repository_groupBox, 1, 0, 1, 1)
                self.Buttons_horizontalLayout = QtGui.QHBoxLayout()
                self.Buttons_horizontalLayout.setObjectName("Buttons_horizontalLayout")
                spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                self.Buttons_horizontalLayout.addItem(spacerItem2)
                self.Buttons_groupBox = QtGui.QGroupBox(sIBL_GUI_FTP_Form)
                self.Buttons_groupBox.setObjectName("Buttons_groupBox")
                self.Buttons_gridLayout = QtGui.QGridLayout(self.Buttons_groupBox)
                self.Buttons_gridLayout.setObjectName("Buttons_gridLayout")
                self.Cancel_pushButton = QtGui.QPushButton(self.Buttons_groupBox)
                self.Cancel_pushButton.setObjectName("Cancel_pushButton")
                self.Buttons_gridLayout.addWidget(self.Cancel_pushButton, 0, 0, 1, 1)
                self.Buttons_horizontalLayout.addWidget(self.Buttons_groupBox)
                self.sIBL_GUI_FTP_Form_gridLayout.addLayout(self.Buttons_horizontalLayout, 3, 0, 1, 1)
                spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
                self.sIBL_GUI_FTP_Form_gridLayout.addItem(spacerItem3, 2, 0, 1, 1)

                self.retranslateUi(sIBL_GUI_FTP_Form)
                QtCore.QMetaObject.connectSlotsByName(sIBL_GUI_FTP_Form)

        def retranslateUi(self, sIBL_GUI_FTP_Form):
                sIBL_GUI_FTP_Form.setWindowTitle(QtGui.QApplication.translate("sIBL_GUI_FTP_Form", "sIBL_GUI FTP", None, QtGui.QApplication.UnicodeUTF8))
                self.Online_Repository_groupBox.setTitle(QtGui.QApplication.translate("sIBL_GUI_FTP_Form", "sIBL GUI - Online Repository", None, QtGui.QApplication.UnicodeUTF8))
                self.Cancel_pushButton.setText(QtGui.QApplication.translate("sIBL_GUI_FTP_Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import sIBL_GUI_FTP_rc
import sIBL_GUI_FTP_rc
import sIBL_GUI_FTP_rc
import sIBL_GUI_FTP_rc
import sIBL_GUI_FTP_rc
