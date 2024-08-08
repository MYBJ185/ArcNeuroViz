from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
from vtkmodules.vtkRenderingCore import vtkRenderer
from ui_compiled.NeuroVizMainWindow import Ui_ArcNeuroViz
from widgets.vtk_widget import CustomInteractorStyle, load_model, load_models_from_folder


class MainWindow(QMainWindow, Ui_ArcNeuroViz):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_512.png'))

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }
        """)
        self.setFixedSize(1080, 720)

        # 创建渲染器
        self.ren = vtkRenderer()
        self.ren.SetBackground(13 / 255, 27 / 255, 42 / 255)

        # 加载脑壳模型文件
        load_model(self.ren, 'models\\MonkeyBrainShell.obj', (224 / 255, 225 / 255, 221 / 255), 0)
        # 加载猴脑脑区模型文件夹中的所有obj文件
        load_models_from_folder(self.ren, 'models\\processed_regions', 1)

        # 将渲染器添加到 QVTKRenderWindowInteractor
        self.BrainWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.BrainWidget.GetRenderWindow().GetInteractor()

        # 清除交互器的所有检测器
        self.iren.RemoveAllObservers()

        # 设置自定义的交互样式
        style = CustomInteractorStyle()
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)

        # 初始化和启动交互器
        self.iren.Initialize()
        self.iren.Start()

        # 强制刷新渲染窗口
        self.BrainWidget.GetRenderWindow().Render()

        # 设置定时器进行模型旋转
        self.angle = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.rotate_model)
        self.timer.start(16)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.BrainWidget.Finalize()

    def rotate_model(self):
        self.angle += 1
        self.ren.GetActiveCamera().Azimuth(1)
        self.BrainWidget.GetRenderWindow().Render()
