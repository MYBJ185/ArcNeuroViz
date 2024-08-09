from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QMainWindow
from vtkmodules.vtkRenderingCore import vtkRenderer
from ui_compiled.main_window import Ui_ArcNeuroViz
from widgets.brain_region_widget import CustomInteractorStyle, load_model, load_models_from_folder
from widgets.brain_region_rotator import BrainRegionRotator
from pages.import_settings_page import ImportSettingsWindow


class MainWindow(QMainWindow, Ui_ArcNeuroViz):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.settings_window = None  # 添加一个属性来存储设置窗口的实例
        self.actionAbout = None
        self.actionExit = None
        self.actionSave = None
        self.actionOpen = None
        self.rotator = None
        self.iren = None
        self.ren = None
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_512.png'))
        self.init_actions()
        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setFixedSize(1080, 720)

        self.init_renderer()
        self.init_vtk_widget()
        self.init_rotator()

    def init_actions(self):
        """初始化菜单栏动作"""
        self.actionOpen = QtGui.QAction("Import data from...", self)
        self.actionExit = QtGui.QAction("Exit", self)
        self.actionAbout = QtGui.QAction("About", self)

        # 绑定动作到菜单栏
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        # 绑定动作到槽函数
        self.actionOpen.triggered.connect(self.open_settings_window)  # 打开导入窗口
        self.actionExit.triggered.connect(self.close)  # 点击Exit退出应用

    def open_settings_window(self):
        """打开设置窗口"""
        if not self.settings_window:
            print("Opening settings window...")
            self.settings_window = ImportSettingsWindow()
            self.settings_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
        self.settings_window.show()
        self.settings_window.set_output_log()

    def init_renderer(self):
        """初始化渲染器"""
        self.ren = vtkRenderer()
        # self.ren.SetBackground(13 / 255, 27 / 255, 42 / 255)
        self.ren.SetBackground(27/255, 27/255, 27/255)
        # 加载脑壳模型文件
        load_model(self.ren, 'models\\monkeyBrainShell.obj', (224 / 255, 225 / 255, 221 / 255), 0)
        # 加载猴脑脑区模型文件夹中的所有obj文件
        load_models_from_folder(self.ren, 'models\\processed_regions', 1)

    def init_vtk_widget(self):
        """初始化 VTK 模型部件"""

        self.BrainWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.BrainWidget.GetRenderWindow().GetInteractor()

        # 清除交互器的所有检测器
        # self.iren.RemoveAllObservers()
        style = CustomInteractorStyle(start_rotation_callback=self.start_rotation,
                                      stop_rotation_callback=self.stop_rotation)
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)

        # 初始化和启动交互器
        self.iren.Initialize()
        self.iren.Start()

        # 强制刷新渲染窗口
        self.BrainWidget.GetRenderWindow().Render()

    def init_rotator(self):
        """初始化旋转控制"""
        self.rotator = BrainRegionRotator(self.ren)
        self.rotator.start_rotation()

    def start_rotation(self):
        """开启模型旋转"""
        self.rotator.start_rotation()

    def stop_rotation(self):
        """关闭模型旋转"""
        self.rotator.stop_rotation()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """窗口关闭事件"""
        # 停止模型旋转
        self.stop_rotation()

        # 停止VTK窗口的渲染
        self.BrainWidget.GetRenderWindow().Finalize()

        # 关闭交互器
        if self.iren is not None:
            self.iren.TerminateApp()

        # 确保窗口正常关闭
        event.accept()
