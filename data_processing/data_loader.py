import os
import sys
import numpy as np

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
        self.metadata = None  # 用于存储附加的元数据
        self.output_dir = "D:/Dev/LNZN/ArcNeuroViz/saved_data"  # 保存数据的目录

    def load_rhd_data(self, file_path: str):
        """
        Load data from RHD file and store it.
        :param file_path: str, the path of the RHD file.
        """
        try:
            self.data, record_time, sample_rate = read_rhd_data(file_path)
            self.metadata = {'record_time': record_time, 'sample_rate': sample_rate}
            import_settings_window_console(f"\nSuccessfully loaded data!")
        except Exception as e:
            import_settings_window_console(f"Failed to load data from {file_path}: {str(e)}")
            self.data = None

    def save_to_npy(self):
        """
        Save the loaded data to .npy files.
        """
        if self.data is None:
            import_settings_window_console("No data to save.")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            # Save data to .npy files
            for key, value in self.data.items():
                file_path = os.path.join(self.output_dir, f"{key}.npy")
                np.save(file_path, value)
                import_settings_window_console(f"Saved {key} to {file_path}")

            # Save metadata to a separate .npy file
            metadata_file_path = os.path.join(self.output_dir, "metadata.npy")
            np.save(metadata_file_path, self.metadata)
            import_settings_window_console(f"Saved metadata to {metadata_file_path}")

        except Exception as e:
            import_settings_window_console(f"Failed to save data to .npy files: {str(e)}")

    def load_from_npy(self):
        """
        Load data from .npy files in the output directory.
        """
        if not os.path.exists("D:"):
            import_settings_window_console("Output directory does not exist.")
            return

        try:
            self.data = {}
            for file_name in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file_name)
                if file_name.endswith(".npy"):
                    key = file_name.replace(".npy", "")
                    self.data[key] = np.load(file_path, allow_pickle=True)
                    import_settings_window_console(f"Loaded {key} from {file_path}")

            # Load metadata separately
            metadata_file_path = os.path.join(self.output_dir, "metadata.npy")
            if os.path.exists(metadata_file_path):
                self.metadata = np.load(metadata_file_path, allow_pickle=True).item()
                import_settings_window_console(f"Loaded metadata from {metadata_file_path}")

        except Exception as e:
            import_settings_window_console(f"Failed to load data from .npy files: {str(e)}")

    def get_data(self):
        """
        获取加载的数据
        :return: dict, the loaded data or None if not loaded.
        """
        return self.data


if __name__ == "__main__":
    loader = RHDDataLoader()
    # 从 .npy 文件中读取数据
    loader.load_from_npy()
