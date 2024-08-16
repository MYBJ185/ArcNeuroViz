import os
import h5py

from PyQt6.QtGui import QIcon
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from collections import defaultdict
from data_processing.data_loader import load_data_from_h5, sort_key

from ui_compiled.main_window import Ui_ArcNeuroViz

from pages.import_settings_page import ImportSettingsWindow
from pages.rhd2avzproject_page import Rhd2AVZ
from pages.import_from_folder_page import ImportFromFolder
from pages.model_page import ModelPage

from widgets.BrainModelWidget import BrainModelWidget
from widgets.OpenGLWaveWiget import CustomOpenGLWidget
from widgets.VTK_model_viewer import VTKModelViewer
from widgets.main_wave_pyqtgraph_widget import WaveformWidget


class MainWindow(QMainWindow, Ui_ArcNeuroViz):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.vtk_viewer = None
        self.model_widget = None
        self.model_widget_layout = None
        self.model_container = None
        self.waveform_container = None
        self.waveform_widget_layout = None
        self.waveform_widget = None
        self.brain_widget = None
        self.model_window = None
        self.renderer = None
        self.vtk_widget = None
        self.opengl_widget = None
        self.opengl_layout = None
        self.opengl_container = None
        self.setupUi(self)

        # 初始化模型
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["no working dir set:"])
        self.treeView.setModel(self.model)

        # 初始化时创建抽象的结构
        self.initialize_abstract_tree_structure()

        self.settings_window = None
        self.rhd2avz_window = None
        self.import_from_folder_window = None
        self.actionAbout = None
        self.actionExit = None
        self.actionOpen = None
        self.actionOpenFromFolder = None
        self.actionSave = None
        self.rotator = None
        self.iren = None
        self.ren = None

        self.working_dir = None
        self.setWindowIcon(QIcon('assets\\mainIcon.png'))
        self.init_actions()

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setFixedSize(1015, 720)

        # 延迟初始化 OpenGL
        # self.init_custom_opengl_widget()
        # self.initialize_brain_widget()
        self.init_waveform_widget()
        self.initialize_vtk_viewer()

    def initialize_vtk_viewer(self):
        """初始化 VTK 模型查看器"""
        self.vtk_viewer = VTKModelViewer(self.BrainWidget)
        self.vtk_viewer.initialize()

    def initialize_brain_widget(self):
        """在指定位置和大小初始化 BrainModelWidget"""
        self.brain_widget = QWidget(self)
        print("Initializing BrainModelWidget...")
        # 设置位置和大小
        self.brain_widget.setGeometry(QtCore.QRect(10, 29, 280, 201))

        self.opengl_layout = QVBoxLayout(self.brain_widget)
        self.opengl_layout.setContentsMargins(0, 0, 0, 0)
        print("Creating BrainModelWidget...")
        # 使用指定的 .obj 文件路径初始化 BrainModelWidget
        obj_file_path = r"D:\Dev\LNZN\ArcNeuroViz\models\processed_regions"
        self.opengl_widget = BrainModelWidget(obj_file_path, self.brain_widget)
        print("BrainModelWidget created.")
        self.opengl_layout.addWidget(self.opengl_widget)
        print("BrainModelWidget added to layout.")
        self.brain_widget.show()  # 显示小部件

    # 在 MainWindow 类中添加以下方法
    def init_waveform_widget(self):
        self.waveform_container = QWidget(self)
        self.waveform_container.setGeometry(305, 30, 705, 680)

        self.waveform_widget_layout = QVBoxLayout(self.waveform_container)
        self.waveform_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.waveform_widget = WaveformWidget(self.waveform_container)
        self.waveform_widget_layout.addWidget(self.waveform_widget)

        # 将容器添加到主窗口中
        self.waveform_container.show()

    def init_custom_opengl_widget(self):
        self.opengl_container = QWidget(self)
        self.opengl_container.setGeometry(305, 30, 705, 680)  # 设置位置和尺寸

        self.opengl_layout = QVBoxLayout(self.opengl_container)
        self.opengl_layout.setContentsMargins(0, 0, 0, 0)

        self.opengl_widget = CustomOpenGLWidget(self.opengl_container)
        self.opengl_layout.addWidget(self.opengl_widget)

        # 将容器添加到主窗口中
        self.opengl_container.show()

        # 在 MainWindow 中应用圆角
        self.opengl_widget.set_rounded_corners(5)

    def initialize_abstract_tree_structure(self):
        """初始化空的抽象树结构"""
        # 例如，创建一个只有PortA和Hardware1的空结构
        port_a_item = QtGui.QStandardItem("Port example")
        hardware_item = QtGui.QStandardItem("Hardware example")
        channel_item = QtGui.QStandardItem("Channel example")

        hardware_item.appendRow(channel_item)
        port_a_item.appendRow(hardware_item)
        self.model.appendRow(port_a_item)

        self.treeView.expandAll()

    def init_actions(self):
        """初始化菜单栏动作"""
        self.actionOpen = QtGui.QAction("Import data from Raw Data(slow)", self)
        self.actionOpenFromFolder = QtGui.QAction("Import data from ANZ project(fast)", self)
        self.actionSave = QtGui.QAction("Save data to ANZ project", self)

        self.actionExit = QtGui.QAction("Exit", self)
        self.actionAbout = QtGui.QAction("About", self)

        # 绑定动作到菜单栏
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpenFromFolder)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)

        self.menuHelp.addAction(self.actionAbout)

        # 绑定动作到槽函数
        # noinspection PyUnresolvedReferences
        self.actionOpen.triggered.connect(self.open_settings_window)  # 打开导入窗口
        # noinspection PyUnresolvedReferences
        self.actionOpenFromFolder.triggered.connect(self.open_from_folder_window)
        # noinspection PyUnresolvedReferences
        self.actionSave.triggered.connect(self.open_rhd2avz_window)  # 打开导入窗口
        # noinspection PyUnresolvedReferences
        self.actionExit.triggered.connect(self.close)  # 点击Exit退出应用

    def open_model_window(self):
        """打开模型窗口"""
        if not self.model_window:
            print("Opening model window...")
            self.model_window = ModelPage()
            self.model_window.mainWindow = self
            self.model_window.init()
        self.model_window.show()

    def open_from_folder_window(self):
        """打开设置窗口"""
        if not self.settings_window:
            print("Opening from_folder_window window...")
            self.import_from_folder_window = ImportFromFolder()
            self.import_from_folder_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
            self.import_from_folder_window.mainWindow = self
        self.import_from_folder_window.show()
        self.import_from_folder_window.set_output_log()

    def open_settings_window(self):
        """打开设置窗口"""
        if not self.settings_window:
            print("Opening settings window...")
            self.settings_window = ImportSettingsWindow()
            self.settings_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
            self.settings_window.mainWindow = self
        self.settings_window.show()
        self.settings_window.set_output_log()

    def open_rhd2avz_window(self):
        if not self.rhd2avz_window:
            print("Opening .rhd to avz window...")
            self.rhd2avz_window = Rhd2AVZ()
            self.rhd2avz_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
            self.rhd2avz_window.mainWindow = self
        self.rhd2avz_window.show()
        self.rhd2avz_window.set_output_log()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """窗口关闭事件"""
        # 确保窗口正常关闭
        # 如果有的话关闭其余打开的窗口
        if self.settings_window:
            self.settings_window.close()
        if self.rhd2avz_window:
            self.rhd2avz_window.close()
        if self.import_from_folder_window:
            self.import_from_folder_window.close()
        if self.model_window:
            self.model_window.close()
        event.accept()

    def check_working_dir(self):
        """检查工作目录配置文件是否存在"""
        if self.working_dir:
            self.model.setHorizontalHeaderLabels([f"{self.working_dir}"])
            working_dir_config_file = self.working_dir + '\\amplifier_channels.txt'
            if not os.path.exists(working_dir_config_file):
                print(f"Amplifier config file found at {working_dir_config_file}")
                port_channel_mapping = parse_amplifier_channels(self.working_dir)
                rename_amplifier_files(self.working_dir, port_channel_mapping)
                self.populate_tree_view(port_channel_mapping)  # 调用 populate_tree_view 来填充树视图
            else:
                print(f"Amplifier config file found at {working_dir_config_file}")
                port_channel_mapping = parse_amplifier_channels(self.working_dir)
                rename_amplifier_files(self.working_dir, port_channel_mapping)
                self.populate_tree_view(port_channel_mapping)  # 调用 populate_tree_view 来填充树视图

    def populate_tree_view(self, port_channel_mapping):
        """
        Populate the QTreeView with the parsed amplifier channel information.
        :param port_channel_mapping: dict, the parsed amplifier channel mapping from parse_amplifier_channels.
        """
        # 清空当前模型的所有项
        self.model.clear()
        self.model.setHorizontalHeaderLabels([f"{self.working_dir}"])
        # 遍历端口和硬件的结构来填充树视图
        for port, hardware_data in port_channel_mapping.items():
            # 创建端口项
            port_item = QtGui.QStandardItem(f"电极:{port}")
            self.model.appendRow(port_item)

            # 创建一个字典来跟踪硬件节点
            hardware_items = {}

            # Channel编号从1开始刷新
            channel_counter = 1

            # 遍历硬件信息
            for _, board_stream, chip_channel in hardware_data:
                hardware_key = f"board_stream {board_stream + 1}"

                # 如果该硬件项已经存在，则获取它，否则创建新的硬件项
                if hardware_key not in hardware_items:
                    hardware_item = QtGui.QStandardItem(hardware_key)
                    hardware_items[hardware_key] = hardware_item
                    port_item.appendRow(hardware_item)
                else:
                    hardware_item = hardware_items[hardware_key]

                # 创建通道项，通道编号从1开始
                channel_item_text = f"Channel {channel_counter} (Chip {chip_channel + 1})"
                channel_item = QtGui.QStandardItem(channel_item_text)
                hardware_item.appendRow(channel_item)

                # 增加通道计数器
                channel_counter += 1

        # 展开所有项
        self.treeView.expandAll()


# 解析amplifier_channels.h5文件
def parse_amplifier_channels(working_dir):
    config_file = os.path.join(working_dir, 'amplifier_channels.h5')
    data_config = load_data_from_h5(config_file)
    data_config = sorted(data_config, key=sort_key)
    # 初始化数据结构
    port_hardware_channel_count = defaultdict(lambda: defaultdict(int))
    pcm = defaultdict(list)
    # 打印正在解析文件的消息
    print(f"Parsing {config_file}...")
    # 遍历每个通道的配置信息
    for idx, channel_info in enumerate(data_config):
        port_name = channel_info['port_name'].decode()  # 转换字节字符串为普通字符串
        board_stream = channel_info['board_stream']  # 获取硬件编号
        chip_channel = channel_info['chip_channel']  # 获取芯片通道号

        port_hardware_channel_count[port_name][board_stream] += 1
        # 将通道索引和芯片通道号一起存储
        pcm[port_name].append((idx + 1, board_stream, chip_channel))
    # 输出统计结果
    for port, hardware_dict in port_hardware_channel_count.items():
        print(f"Port {port}:")
        for hardware, channel_count in hardware_dict.items():
            print(f"  Hardware {hardware}: {channel_count} channels")
            pass
    return pcm


def rename_amplifier_files(working_dir, port_channel_mapping):
    processed_data_dir = os.path.join(working_dir, 'processed_amplifier_data')

    if not os.path.exists(processed_data_dir):
        # print(f"Processed data directory {processed_data_dir} does not exist.")
        return

    for port, channel_data in port_channel_mapping.items():
        for i, (channel_idx, board_stream, chip_channel) in enumerate(channel_data):
            old_filename = f'amplifier_channel{channel_idx}.h5'
            new_filename = f'{port}_channel{i + 1}_board_stream{board_stream+1}_chip{chip_channel+1}.h5'
            old_filepath = os.path.join(processed_data_dir, old_filename)
            new_filepath = os.path.join(processed_data_dir, new_filename)

            if os.path.exists(old_filepath):
                os.rename(old_filepath, new_filepath)
                # print(f"Renamed {old_filename} to {new_filename}")
            else:
                # print(f"{old_filename} does not exist, skipping.")
                pass


if __name__ == "__main__":
    # port_channel_mapping = parse_amplifier_channels('D:\\Dev\\LNZN\\test_ANV_project')
    # rename_amplifier_files('D:\\Dev\\LNZN\\test_ANV_project', port_channel_mapping)
    with h5py.File("D:\Dev\LNZN\\test_ANV_project\processed_amplifier_data"
                   "\Port A_channel1_board_stream1_chip1.h5", 'r') as f:
        dataset = f['dataset_name'][:]
        print(dataset)
