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

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1b2a;
            }
        """)
        self.setFixedSize(1080, 720)

        # 创建渲染器
        self.ren = vtkRenderer()
        self.ren.SetBackground(13/255, 27/255, 42/255)

        # 加载第一个模型
        self.load_model('model\\MonkeyBrainShell.obj', (224/255, 225/255, 221/255), 0.3)
        # 加载第二个模型
        self.load_model('model\\monkeyPolyModel.obj', (119/255, 141/255, 169/255), 1)  # 绿色

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

    def load_model(self, file_path, color, opacity):
        # 创建并设置 OBJ 读取器
        obj_reader = vtkOBJReader()
        print(f"Loading OBJ file from: {file_path}")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"Error: File does not exist at {file_path}")
            return

        obj_reader.SetFileName(file_path)
        obj_reader.Update()

        # 检查是否成功读取文件
        output = obj_reader.GetOutput()
        if output.GetNumberOfPoints() == 0:
            print(f"Error: Failed to load OBJ model from {file_path}")
            return
        else:
            print(f"Successfully loaded OBJ model from {file_path}")

        # 创建映射器
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(obj_reader.GetOutputPort())

        # 创建演员
        actor = vtkActor()
        actor.SetMapper(mapper)

        # 设置模型颜色
        actor.GetProperty().SetColor(color)  # RGB 值，范围 0 到 1
        actor.GetProperty().SetOpacity(opacity)  # 透明度，范围 0.0 到 1.0
        # 将演员添加到渲染器
        self.ren.AddActor(actor)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.vtkWidget.Finalize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
