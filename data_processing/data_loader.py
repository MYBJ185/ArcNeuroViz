import os
import sys

# 添加工具模块的路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../tools/load_intan_rhd_format'))
from tools.load_intan_rhd_format.load_intan_rhd_format import read_rhd_data


def import_settings_window_console(message: str):
    """
    Write a message to the console or log.
    :param message: str, the message to write.
    """
    print(message)  # 这里你可以使用其他方式将信息写入GUI界面的控制台


class RHDDataLoader:
    def __init__(self):
        self.data = None  # 用于存储读取到的数据

    def load_rhd_data(self, file_path: str):
        """
        Load data from RHD file and store it.
        :param file_path: str, the path of the RHD file.
        :return: dict, the data from the RHD file.
        """
        try:
            self.data = read_rhd_data(file_path)
            import_settings_window_console(f"\nSuccessfully loaded data!")
        except Exception as e:
            import_settings_window_console(f"Failed to load data from {file_path}: {str(e)}")
            self.data = None

    def get_data(self):
        """
        获取加载的数据
        :return: dict, the loaded data or None if not loaded.
        """
        return self.data


if __name__ == "__main__":
    loader = RHDDataLoader()
    loader.load_rhd_data("../../demo_data/20221219/leftV1_1/s0633_0615_0690_221219_114735.rhd")
