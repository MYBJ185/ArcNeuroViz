import sys
import threading

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from data_processing.data_loader import RHDDataLoader
from ui_compiled.rhd2avz import Ui_rhd2avz
from tools.load_intan_rhd_format.load_intan_rhd_format import read_rhd_data


class QTextEditLogger:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        # 去除 message 末尾的多余换行符，并在追加到 text_edit 中时使用 `strip` 方法去除空行
        if message.strip():  # 只在 message 有内容时追加
            self.text_edit.append(message.rstrip())

    def flush(self):
        # 清空文本区域
        # self.text_edit.clear()
        pass


class Rhd2AVZ(QMainWindow, Ui_rhd2avz):
    def __init__(self) -> None:
        super(Rhd2AVZ, self).__init__()
        self.mainWindow = None  # 添加一个属性来存储主窗口的实例
        self.original_stdout = None
        self.log_output = None
        self.data_loader = RHDDataLoader()  # 初始化 RHDDataLoader 实例
        self.data_loader_thread = None
        self.setWindowIcon(QIcon('mainIcon.png'))
        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setupUi(self)
        self.setWindowTitle("ANV - Import data file")
        self.setFixedSize(372, 317)
        # 设置下拉菜单选项
        self.setup_comboboxes()

        # 连接按钮点击事件
        self.pushButton_browse.clicked.connect(self.open_files_dialog)
        self.pushButton_browse_2.clicked.connect(self.open_file_dialog)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.start_data_transfer)
        self.set_output_log()

    def set_output_log(self):
        """重定向标准输出流"""
        self.original_stdout = sys.stdout
        self.log_output = QTextEditLogger(self.textEdit_log)
        sys.stdout = self.log_output

    def setup_comboboxes(self):
        """设置下拉菜单选项"""
        self.comboBox_2.addItem(".rhd")  # 提供.rhd文件类型
        self.comboBox.addItems(["Auto Detect", "10kHz", "20kHz", "30kHz"])  # 提供三种采样率选择以及自动识别

    def open_file_dialog(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "RHD Files (*.rhd)")
        if file_path:
            self.lineEdit_path_2.setText(file_path)

    def open_files_dialog(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "Select Data Directory", "")
        if folder_path:
            self.lineEdit_path.setText(folder_path)

    def start_data_transfer(self):

        file_path = self.lineEdit_path_2.text()
        selected_samplerate = self.comboBox.currentText()

        self.mainWindow.working_dir = self.lineEdit_path.text()
        self.data_loader.working_dir = self.mainWindow.working_dir
        self.log_message(f"Working directory set to {self.mainWindow.working_dir}")
        self.log_message("Starting data transfer...")

        # 创建并启动数据加载线程，传递 data_loader 实例
        self.data_loader_thread = DataTransformerThread(self.data_loader, file_path, selected_samplerate)
        # self.data_loader_thread.data_loaded.connect(self.on_data_loaded)
        self.data_loader_thread.start()
        # self.data_loader.save_rhd_data(file_path)
        # 禁用控件
        self.pushButton.setEnabled(False)
        self.pushButton_browse.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.comboBox_2.setEnabled(False)

    def on_data_loaded(self, message):
        # 当数据加载完成后，重新启用控件并显示消息
        self.log_message(message)
        self.pushButton.setEnabled(True)
        self.pushButton_browse.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)

    def closeEvent(self, event) -> None:
        """窗口关闭事件，恢复标准输出流"""
        sys.stdout = self.original_stdout  # 恢复标准输出流
        event.accept()

    def log_message(self, message: str):
        self.textEdit_log.append(message)


class DataTransformerThread(threading.Thread):
    # 创建信号用于在数据加载完成后通知主线程
    data_loaded = pyqtSignal(str)

    def __init__(self, data_loader, file_path: str, samplerate: str):
        super().__init__()
        self.data_loader = data_loader
        self.file_path = file_path
        self.samplerate = samplerate
        self._pause_event = threading.Event()
        self._pause_event.set()  # 默认不暂停
        self._is_running = True

    def run(self):
        # 在后台线程中执行耗时操作
        print("Loading data from file...")

        # self.data_loader.save_rhd_data(self.file_path)
        # 等待5s
        read_rhd_data(self.file_path)
        # 数据加载完成后发送信号
        print(f"Data loaded from {self.file_path} with sample rate {self.samplerate}")

    def pause(self):
        """暂停线程执行"""
        self._pause_event.clear()

    def resume(self):
        """恢复线程执行"""
        self._pause_event.set()

    def stop(self):
        """停止线程"""
        self._is_running = False
        self._pause_event.set()
