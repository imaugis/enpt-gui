# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db1.ui'
#
# Created: Wed Jun 13 16:40:17 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog1(object):
    def setupUi(self, Dialog1):
        Dialog1.setObjectName(_fromUtf8("Dialog1"))
        Dialog1.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog1.resize(239, 470)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog1.sizePolicy().hasHeightForWidth())
        Dialog1.setSizePolicy(sizePolicy)
        self.Wa = QtGui.QWidget(Dialog1)
        self.Wa.setGeometry(QtCore.QRect(10, 10, 221, 200))
        self.Wa.setAcceptDrops(False)
        self.Wa.setObjectName(_fromUtf8("Wa"))
        self.LElabel1 = QtGui.QLineEdit(Dialog1)
        self.LElabel1.setGeometry(QtCore.QRect(30, 280, 201, 27))
        self.LElabel1.setObjectName(_fromUtf8("LElabel1"))
        self.LElabel2 = QtGui.QLineEdit(Dialog1)
        self.LElabel2.setGeometry(QtCore.QRect(30, 310, 201, 27))
        self.LElabel2.setObjectName(_fromUtf8("LElabel2"))
        self.label = QtGui.QLabel(Dialog1)
        self.label.setGeometry(QtCore.QRect(10, 250, 131, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.PBicone = QtGui.QPushButton(Dialog1)
        self.PBicone.setGeometry(QtCore.QRect(130, 220, 100, 27))
        self.PBicone.setAutoDefault(True)
        self.PBicone.setObjectName(_fromUtf8("PBicone"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog1)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 430, 201, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.PBannule = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.PBannule.setDefault(True)
        self.PBannule.setObjectName(_fromUtf8("PBannule"))
        self.horizontalLayout.addWidget(self.PBannule)
        self.PBvalide = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.PBvalide.setAutoDefault(True)
        self.PBvalide.setObjectName(_fromUtf8("PBvalide"))
        self.horizontalLayout.addWidget(self.PBvalide)
        self.label_2 = QtGui.QLabel(Dialog1)
        self.label_2.setGeometry(QtCore.QRect(110, 355, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.LEcom = QtGui.QLineEdit(Dialog1)
        self.LEcom.setGeometry(QtCore.QRect(30, 385, 201, 27))
        self.LEcom.setObjectName(_fromUtf8("LEcom"))
        self.PBcom = QtGui.QPushButton(Dialog1)
        self.PBcom.setGeometry(QtCore.QRect(10, 350, 100, 27))
        self.PBcom.setAutoDefault(True)
        self.PBcom.setObjectName(_fromUtf8("PBcom"))

        self.retranslateUi(Dialog1)
        QtCore.QMetaObject.connectSlotsByName(Dialog1)
        Dialog1.setTabOrder(self.LElabel1, self.LElabel2)
        Dialog1.setTabOrder(self.LElabel2, self.PBcom)
        Dialog1.setTabOrder(self.PBcom, self.LEcom)
        Dialog1.setTabOrder(self.LEcom, self.PBannule)
        Dialog1.setTabOrder(self.PBannule, self.PBvalide)
        Dialog1.setTabOrder(self.PBvalide, self.PBicone)

    def retranslateUi(self, Dialog1):
        Dialog1.setWindowTitle(QtGui.QApplication.translate("Dialog1", "Nouvelle Rubrique", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog1", "Labels", None, QtGui.QApplication.UnicodeUTF8))
        self.PBicone.setText(QtGui.QApplication.translate("Dialog1", "Icone", None, QtGui.QApplication.UnicodeUTF8))
        self.PBannule.setText(QtGui.QApplication.translate("Dialog1", "Annuler", None, QtGui.QApplication.UnicodeUTF8))
        self.PBvalide.setText(QtGui.QApplication.translate("Dialog1", "Valider", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog1", " (optionnelle)", None, QtGui.QApplication.UnicodeUTF8))
        self.PBcom.setText(QtGui.QApplication.translate("Dialog1", "Commande", None, QtGui.QApplication.UnicodeUTF8))

