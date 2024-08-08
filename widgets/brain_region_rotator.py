from PyQt6 import QtCore
from vtkmodules.vtkRenderingCore import vtkRenderer


class BrainRegionRotator(QtCore.QObject):
    def __init__(self, renderer: vtkRenderer, interval: int = 16, parent=None):
        super(BrainRegionRotator, self).__init__(parent)
        self.renderer = renderer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.rotate_model)
        self.angle = 0
        self.rotation_enabled = False
        self.interval = interval

    def start_rotation(self):
        """开启模型旋转"""
        if not self.rotation_enabled:
            self.timer.start(self.interval)
            self.rotation_enabled = True
            # print("Rotation started")

    def stop_rotation(self):
        """关闭模型旋转"""
        if self.rotation_enabled:
            self.timer.stop()
            self.rotation_enabled = False
            # print("Rotation stopped")

    def toggle_rotation(self):
        """切换模型旋转功能的开启和关闭"""
        if self.rotation_enabled:
            self.stop_rotation()
        else:
            self.start_rotation()

    def rotate_model(self):
        """执行模型旋转"""
        self.angle += 1
        self.renderer.GetActiveCamera().Azimuth(1)
        self.renderer.GetRenderWindow().Render()
