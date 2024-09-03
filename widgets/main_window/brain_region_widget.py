import os

import vtk
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor, vtkRenderer


def parse_color_from_filename(filename):
    """
    从文件名中解析出颜色信息。
    文件名格式为：<name>-('<R>', '<G>', '<B>').obj
    返回 (R, G, B) 颜色值，范围在 0 到 1 之间。
    """
    try:
        name_parts = filename.split('-')
        color_part = name_parts[-1].strip(".obj")
        color_str = color_part.strip("()").replace("'", "")
        color_values = color_str.split(", ")
        color = tuple(float(c) for c in color_values)
        return color
    except Exception as e:
        print(f"Error parsing color from filename {filename}: {e}")
        return 1.0, 1.0, 1.0


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, start_rotation_callback=None, stop_rotation_callback=None):
        super(CustomInteractorStyle, self).__init__()
        self.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.left_button_press_event)
        self.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.right_button_press_event)
        self.AddObserver(vtk.vtkCommand.RightButtonReleaseEvent, self.right_button_release_event)
        self.AddObserver(vtk.vtkCommand.MouseWheelForwardEvent, self.mouse_wheel_forward_event)
        self.AddObserver(vtk.vtkCommand.MouseWheelBackwardEvent, self.mouse_wheel_backward_event)
        self.AddObserver(vtk.vtkCommand.MouseMoveEvent, self.mouse_move_event)
        self.selected_actor = None
        self.is_right_button_pressed = False
        self.start_rotation_callback = start_rotation_callback
        self.stop_rotation_callback = stop_rotation_callback

    def left_button_press_event(self, _, __):
        click_pos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, self.GetDefaultRenderer())

        new_actor = picker.GetActor()

        if new_actor:
            self.selected_actor = new_actor
            self.selected_actor.GetProperty().SetOpacity(0.0)  # Set new selected actor to be transparent

        self.OnLeftButtonDown()
        return

    def right_button_press_event(self, _, __):
        self.is_right_button_pressed = True
        if self.stop_rotation_callback:
            self.stop_rotation_callback()
        self.OnRightButtonDown()
        return

    def right_button_release_event(self, _, __):
        self.is_right_button_pressed = False
        if self.start_rotation_callback:
            self.start_rotation_callback()
        self.OnRightButtonUp()
        return

    def mouse_wheel_forward_event(self, _, __):
        self.GetDefaultRenderer().GetActiveCamera().Dolly(1.1)
        self.GetDefaultRenderer().ResetCameraClippingRange()
        self.OnMouseWheelForward()
        return

    def mouse_wheel_backward_event(self, _, __):
        self.GetDefaultRenderer().GetActiveCamera().Dolly(0.9)
        self.GetDefaultRenderer().ResetCameraClippingRange()
        self.OnMouseWheelBackward()
        return

    def mouse_move_event(self, _, __):
        if self.is_right_button_pressed:
            self.OnMouseMove()
        else:
            super(CustomInteractorStyle, self).OnMouseMove()

    def OnLeftButtonDown(self, obj=None, event=None):
        pass

    def OnLeftButtonUp(self, obj=None, event=None):
        pass

    def OnMiddleButtonDown(self, obj=None, event=None):
        pass

    def OnMiddleButtonUp(self, obj=None, event=None):
        pass

    def OnRightButtonDown(self, obj=None, event=None):
        super().OnLeftButtonDown()

    def OnRightButtonUp(self, obj=None, event=None):
        super().OnLeftButtonUp()

    def OnMouseWheelForward(self, obj=None, event=None):
        pass

    def OnMouseWheelBackward(self, obj=None, event=None):
        pass

    def OnChar(self, obj=None, event=None):
        pass

    def OnKeyPress(self, obj=None, event=None):
        pass

    def OnKeyRelease(self, obj=None, event=None):
        pass


def load_model(renderer: vtkRenderer, file_path: str, color: tuple, opacity: float) -> None:
    # 创建并设置 OBJ 读取器
    obj_reader = vtkOBJReader()
    # print(f"Loading OBJ file from: {file_path}")

    if not os.path.exists(file_path):
        print(f"Error: File does not exist at {file_path}")
        return

    obj_reader.SetFileName(file_path)
    obj_reader.Update()

    output = obj_reader.GetOutput()
    if output.GetNumberOfPoints() == 0:
        print(f"Error: Failed to load OBJ model from {file_path}")
        return
    else:
        pass
        # print(f"Successfully loaded OBJ model from {file_path}")

    # 创建映射器
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(obj_reader.GetOutputPort())

    # 创建Actor
    actor = vtkActor()
    actor.SetMapper(mapper)

    # 设置模型颜色和透明度
    actor.GetProperty().SetColor(list(color))
    actor.GetProperty().SetOpacity(opacity)
    # 将Actor添加到渲染器
    renderer.AddActor(actor)


def load_models_from_folder(renderer: vtkRenderer, folder_path: str, opacity: float) -> None:
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"Error: Folder does not exist at {folder_path}")
        return

    # 获取文件夹中的所有obj文件
    files = [f for f in os.listdir(folder_path) if f.endswith('.obj')]
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        color = parse_color_from_filename(filename)
        load_model(renderer, file_path, color, opacity)
