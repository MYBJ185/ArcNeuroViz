import sys

from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor, vtkRenderer

from ui_compiled.NeuroVizMainWindow import Ui_NeuroVizMainWindow


class MainWindow(QMainWindow, Ui_NeuroVizMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_512.png'))

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #14213d;
            }
        """)
        self.setFixedSize(1080, 720)

        # 创建数据源
        print("Creating source...")
        source = vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)

        # 创建映射器
        print("Creating mapper...")
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # 创建演员
        print("Creating actor...")
        actor = vtkActor()
        actor.SetMapper(mapper)

        # 创建渲染器
        print("Creating renderer...")
        self.ren = vtkRenderer()
        self.ren.AddActor(actor)
        self.ren.SetBackground(0.1, 0.2, 0.4)  # 设置背景颜色，确保背景不是黑色

        # 将渲染器添加到 QVTKRenderWindowInteractor
        print("Adding renderer to QVTKRenderWindowInteractor...")
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # 设置摄像机
        print("Resetting camera...")
        self.ren.ResetCamera()

        # 初始化和启动交互器
        print("Initializing interactor...")
        self.iren.Initialize()
        print("Starting interactor...")
        self.iren.Start()
        print("Interactor started.")
        # 强制刷新渲染窗口
        self.vtkWidget.GetRenderWindow().Render()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.vtkWidget.Finalize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
