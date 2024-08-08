from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
from vtkmodules.vtkRenderingCore import vtkRenderer
from ui_compiled.main_window import Ui_ArcNeuroViz
from widgets.brain_region_widget import CustomInteractorStyle, load_model, load_models_from_folder
from widgets.brain_region_rotator import BrainRegionRotator


class MainWindow(QMainWindow, Ui_ArcNeuroViz):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.rotator = None
        self.iren = None
        self.ren = None
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_512.png'))

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }
        """)
        self.setFixedSize(1080, 720)

        self.init_renderer()
        self.init_vtk_widget()
        self.init_rotator()

    def init_renderer(self):
        """初始化渲染器"""
        self.ren = vtkRenderer()
        self.ren.SetBackground(13 / 255, 27 / 255, 42 / 255)

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

    # def init_timer(self):
    #     """初始化定时器"""
    #     self.angle = 0
    #     self.timer = QtCore.QTimer(self)
    #     self.timer.timeout.connect(self.rotate_model)
    #     self.rotation_enabled = False  # 旋转功能默认关闭

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
        self.BrainWidget.Finalize()
