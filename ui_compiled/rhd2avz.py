# Form implementation generated from reading ui file 'ui/rhd2avz.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_rhd2avz(object):
    def setupUi(self, rhd2avz):
        rhd2avz.setObjectName("rhd2avz")
        rhd2avz.resize(372, 326)
        rhd2avz.setWindowTitle("Arc NeuroWave Visualizer")
        self.centralwidget = QtWidgets.QWidget(parent=rhd2avz)
        self.centralwidget.setObjectName("centralwidget")
        self.label_path = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_path.setGeometry(QtCore.QRect(10, 10, 71, 26))
        self.label_path.setObjectName("label_path")
        self.lineEdit_path = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_path.setGeometry(QtCore.QRect(90, 10, 191, 26))
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.pushButton_browse = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_browse.setGeometry(QtCore.QRect(290, 10, 75, 26))
        self.pushButton_browse.setObjectName("pushButton_browse")
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 90, 191, 26))
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setObjectName("comboBox_2")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 90, 71, 26))
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 71, 26))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 130, 191, 26))
        self.comboBox.setEditable(True)
        self.comboBox.setCurrentText("Select a sample rate...")
        self.comboBox.setMaxVisibleItems(9)
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 130, 75, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 90, 75, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit_log = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(10, 170, 351, 141))
        self.textEdit_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.textEdit_log.setReadOnly(True)
        self.textEdit_log.setObjectName("textEdit_log")
        self.lineEdit_path_2 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_path_2.setGeometry(QtCore.QRect(90, 50, 191, 26))
        self.lineEdit_path_2.setObjectName("lineEdit_path_2")
        self.pushButton_browse_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_browse_2.setGeometry(QtCore.QRect(290, 50, 75, 26))
        self.pushButton_browse_2.setObjectName("pushButton_browse_2")
        self.label_path_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_path_2.setGeometry(QtCore.QRect(10, 50, 71, 26))
        self.label_path_2.setObjectName("label_path_2")
        rhd2avz.setCentralWidget(self.centralwidget)

        self.retranslateUi(rhd2avz)
        QtCore.QMetaObject.connectSlotsByName(rhd2avz)

    def retranslateUi(self, rhd2avz):
        _translate = QtCore.QCoreApplication.translate
        self.label_path.setText(_translate("rhd2avz", "Porject Path"))
        self.pushButton_browse.setText(_translate("rhd2avz", "Browse"))
        self.comboBox_2.setCurrentText(_translate("rhd2avz", "Select a data type..."))
        self.label.setText(_translate("rhd2avz", "Data Type"))
        self.label_2.setText(_translate("rhd2avz", "Sample rate"))
        self.pushButton.setText(_translate("rhd2avz", "OK"))
        self.pushButton_2.setText(_translate("rhd2avz", "Cancel"))
        self.pushButton_browse_2.setText(_translate("rhd2avz", "Browse"))
        self.label_path_2.setText(_translate("rhd2avz", "Data Path"))