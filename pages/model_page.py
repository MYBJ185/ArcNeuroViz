from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow

from vtkmodules.vtkRenderingCore import vtkRenderer

from ui_compiled.model import Ui_Model_window

from widgets.brain_region_rotator import BrainRegionRotator
from widgets.brain_region_widget import load_model, load_models_from_folder, CustomInteractorStyle


class ModelPage(QMainWindow, Ui_Model_window):
    def __init__(self) -> None:
        super(ModelPage, self).__init__()
        self.rotator = None
        self.iren = None
        self.ren = None
        self.mainWindow = None  # 添加一个属性来存储主窗口的实例

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setupUi(self)
        self.setWindowTitle("ANV - Import data file")
        self.setFixedSize(350, 200)

    def init(self):
        """初始化页面"""
        self.init_renderer()
        self.init_vtk_widget()
        self.init_rotator()

    def init_renderer(self):
        self.ren = vtkRenderer()
        # self.ren.SetBackground(13 / 255, 27 / 255, 42 / 255)
        self.ren.SetBackground(27/255, 27/255, 27/255)
        # 加载脑壳模型文件
        load_model(self.ren, 'models\\monkeyBrainShell.obj', (224 / 255, 225 / 255, 221 / 255), 0.3)
        # 加载猴脑脑区模型文件夹中的所有obj文件
        load_models_from_folder(self.ren, 'models\\processed_regions', 1)

    def init_vtk_widget(self):

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
