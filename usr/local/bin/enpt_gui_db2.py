# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db2.ui'
#
# Created: Wed Jun 13 16:40:56 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog2(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName(_fromUtf8("Dialog2"))
        Dialog2.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog2.resize(444, 242)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog2.sizePolicy().hasHeightForWidth())
        Dialog2.setSizePolicy(sizePolicy)
        self.Wa = QtGui.QWidget(Dialog2)
        self.Wa.setGeometry(QtCore.QRect(10, 10, 190, 190))
        self.Wa.setAcceptDrops(False)
        self.Wa.setObjectName(_fromUtf8("Wa"))
        self.LElabel1 = QtGui.QLineEdit(Dialog2)
        self.LElabel1.setGeometry(QtCore.QRect(230, 40, 201, 27))
        self.LElabel1.setObjectName(_fromUtf8("LElabel1"))
        self.LElabel2 = QtGui.QLineEdit(Dialog2)
        self.LElabel2.setGeometry(QtCore.QRect(230, 70, 201, 27))
        self.LElabel2.setObjectName(_fromUtf8("LElabel2"))
        self.label = QtGui.QLabel(Dialog2)
        self.label.setGeometry(QtCore.QRect(210, 10, 131, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.PBicone = QtGui.QPushButton(Dialog2)
        self.PBicone.setGeometry(QtCore.QRect(50, 200, 100, 27))
        self.PBicone.setAutoDefault(True)
        self.PBicone.setObjectName(_fromUtf8("PBicone"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(230, 190, 201, 41))
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
        self.label_2 = QtGui.QLabel(Dialog2)
        self.label_2.setGeometry(QtCore.QRect(310, 115, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.LEcom = QtGui.QLineEdit(Dialog2)
        self.LEcom.setGeometry(QtCore.QRect(230, 145, 201, 27))
        self.LEcom.setObjectName(_fromUtf8("LEcom"))
        self.PBcom = QtGui.QPushButton(Dialog2)
        self.PBcom.setGeometry(QtCore.QRect(210, 110, 100, 27))
        self.PBcom.setAutoDefault(True)
        self.PBcom.setObjectName(_fromUtf8("PBcom"))

        self.retranslateUi(Dialog2)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)
        Dialog2.setTabOrder(self.LElabel1, self.LElabel2)
        Dialog2.setTabOrder(self.LElabel2, self.PBcom)
        Dialog2.setTabOrder(self.PBcom, self.LEcom)
        Dialog2.setTabOrder(self.LEcom, self.PBannule)
        Dialog2.setTabOrder(self.PBannule, self.PBvalide)
        Dialog2.setTabOrder(self.PBvalide, self.PBicone)

    def retranslateUi(self, Dialog2):
        Dialog2.setWindowTitle(QtGui.QApplication.translate("Dialog2", "Nouvelle Commande", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog2", "Labels", None, QtGui.QApplication.UnicodeUTF8))
        self.PBicone.setText(QtGui.QApplication.translate("Dialog2", "Icone", None, QtGui.QApplication.UnicodeUTF8))
        self.PBannule.setText(QtGui.QApplication.translate("Dialog2", "Annuler", None, QtGui.QApplication.UnicodeUTF8))
        self.PBvalide.setText(QtGui.QApplication.translate("Dialog2", "Valider", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog2", " (Obligatoire)", None, QtGui.QApplication.UnicodeUTF8))
        self.PBcom.setText(QtGui.QApplication.translate("Dialog2", "Commande", None, QtGui.QApplication.UnicodeUTF8))

