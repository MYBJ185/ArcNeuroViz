import os
import sys
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2

from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor, vtkRenderer

from ui_compiled.NeuroVizMainWindow import Ui_ArcNeuroViz


class MainWindow(QMainWindow, Ui_ArcNeuroViz):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon_512.png'))

        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }
        """)
        self.setFixedSize(1080, 720)

        # 创建渲染器
        self.ren = vtkRenderer()
        self.ren.SetBackground(0, 0, 0)
        self.ren.SetBackground(13 / 255, 27 / 255, 42 / 255)
        # 创建并设置 OBJ 读取器
        obj_reader = vtkOBJReader()
        obj_path = 'D:\\Dev\\LNZN\\ArcNeuroViz\\model\\MonkeyBrianShell.obj'  # 使用绝对路径
        print(f"Loading OBJ file from: {obj_path}")

        # 检查文件是否存在
        if not os.path.exists(obj_path):
            print(f"Error: File does not exist at {obj_path}")
            return

        obj_reader.SetFileName(obj_path)
        obj_reader.Update()

        # 检查是否成功读取文件
        output = obj_reader.GetOutput()
        if output.GetNumberOfPoints() == 0:
            print(f"Error: Failed to load OBJ model from {obj_path}")
            return
        else:
            print(f"Successfully loaded OBJ model from {obj_path}")

        # 创建映射器
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(obj_reader.GetOutputPort())

        # 创建演员
        actor = vtkActor()
        actor.SetMapper(mapper)

        # 设置模型颜色
        actor.GetProperty().SetColor(119/255, 141/255, 169/255)

        # 将演员添加到渲染器
        self.ren.AddActor(actor)

        # 将渲染器添加到 QVTKRenderWindowInteractor
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # 设置摄像机
        self.ren.ResetCamera()

        # 初始化和启动交互器
        self.iren.Initialize()
        self.iren.Start()

        # 强制刷新渲染窗口
        self.vtkWidget.GetRenderWindow().Render()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.vtkWidget.Finalize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
