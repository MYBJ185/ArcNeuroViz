# Form implementation generated from reading ui file 'ui/model.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Model_window(object):
    def setupUi(self, Model_window):
        Model_window.setObjectName("Model_window")
        Model_window.resize(350, 200)
        self.centralwidget = QtWidgets.QWidget(parent=Model_window)
        self.centralwidget.setObjectName("centralwidget")
        self.BrainWidget = QVTKRenderWindowInteractor(parent=self.centralwidget)
        self.BrainWidget.setEnabled(True)
        self.BrainWidget.setGeometry(QtCore.QRect(0, -20, 350, 200))
        self.BrainWidget.setObjectName("BrainWidget")
        Model_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Model_window)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 22))
        self.menubar.setObjectName("menubar")
        Model_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Model_window)
        self.statusbar.setObjectName("statusbar")
        Model_window.setStatusBar(self.statusbar)

        self.retranslateUi(Model_window)
        QtCore.QMetaObject.connectSlotsByName(Model_window)

    def retranslateUi(self, Model_window):
        _translate = QtCore.QCoreApplication.translate
        Model_window.setWindowTitle(_translate("Model_window", "MainWindow"))
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor