# Form implementation generated from reading ui file 'ui/NeuroVizMainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_NeuroVizMainWindow(object):
    def setupUi(self, NeuroVizMainWindow):
        NeuroVizMainWindow.setObjectName("NeuroVizMainWindow")
        NeuroVizMainWindow.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        NeuroVizMainWindow.setEnabled(True)
        NeuroVizMainWindow.resize(1080, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NeuroVizMainWindow.sizePolicy().hasHeightForWidth())
        NeuroVizMainWindow.setSizePolicy(sizePolicy)
        NeuroVizMainWindow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(parent=NeuroVizMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vtkWidget = QVTKRenderWindowInteractor(parent=self.centralwidget)
        self.vtkWidget.setGeometry(QtCore.QRect(270, 120, 540, 480))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtkWidget.sizePolicy().hasHeightForWidth())
        self.vtkWidget.setSizePolicy(sizePolicy)
        self.vtkWidget.setObjectName("vtkWidget")
        NeuroVizMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=NeuroVizMainWindow)
        self.statusbar.setObjectName("statusbar")
        NeuroVizMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(NeuroVizMainWindow)
        QtCore.QMetaObject.connectSlotsByName(NeuroVizMainWindow)

    def retranslateUi(self, NeuroVizMainWindow):
        _translate = QtCore.QCoreApplication.translate
        NeuroVizMainWindow.setWindowTitle(_translate("NeuroVizMainWindow", "ArcNeuroViz"))
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor