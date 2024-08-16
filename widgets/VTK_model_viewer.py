from vtkmodules.vtkRenderingCore import vtkRenderer
from widgets.brain_region_widget import load_model, load_models_from_folder, CustomInteractorStyle
from widgets.brain_region_rotator import BrainRegionRotator


class VTKModelViewer:
    def __init__(self, brain_widget):
        self.brain_widget = brain_widget
        self.renderer = vtkRenderer()
        self.interactor = None
        self.rotator = None

    def initialize(self):
        """初始化 VTK 渲染器和加载模型"""
        self.renderer.SetBackground(27 / 255, 27 / 255, 27 / 255)
        self.brain_widget.GetRenderWindow().AddRenderer(self.renderer)
        self._load_models()
        self._setup_interactor()
        self.brain_widget.GetRenderWindow().Render()

    def _load_models(self):
        """加载模型文件"""
        load_model(self.renderer, 'models\\monkeyBrainShell.obj', (224 / 255, 225 / 255, 221 / 255), 0.3)
        load_models_from_folder(self.renderer, 'models\\processed_regions', 1)

    def _setup_interactor(self):
        """设置 VTK 交互器和自定义交互风格"""

        self.interactor = self.brain_widget.GetRenderWindow().GetInteractor()
        style = CustomInteractorStyle(start_rotation_callback=self.start_rotation,
                                      stop_rotation_callback=self.stop_rotation)
        style.SetDefaultRenderer(self.renderer)
        self.interactor.SetInteractorStyle(style)
        self.interactor.Initialize()
        self.interactor.Start()

    def start_rotation(self):
        """启动模型旋转"""
        if not self.rotator:
            self.rotator = BrainRegionRotator(self.renderer)
        self.rotator.start_rotation()

    def stop_rotation(self):
        """停止模型旋转"""
        if self.rotator:
            self.rotator.stop_rotation()

    def finalize(self):
        """终止 VTK 渲染器和交互器"""
        if self.interactor:
            self.brain_widget.GetRenderWindow().Finalize()
            self.interactor.TerminateApp()
