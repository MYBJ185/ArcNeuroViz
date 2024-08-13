import os
import re
import sys
import time
import h5py
from enum import Enum

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
        self.working_dir = "D:\Dev\LNZN\test_ANV_project"  # 工作目录

    def load_rhd_data(self, f_p: str):
        """
        Load data from RHD file and store it.
        :param f_p: str, the path of the RHD file.
        """
        print(f"Loading data from {f_p}...")
        try:
            self.data, record_time, sample_rate = read_rhd_data(f_p)
            self.metadata = {'record_time': record_time, 'sample_rate': sample_rate}
            import_settings_window_console(f"\nSuccessfully loaded data!")
        except Exception as e:
            import_settings_window_console(f"Failed to load data from {f_p}: {str(e)}")
            self.data = None

    def save_rhd_data(self, f_p: str):
        """
        Load the RHD data from the specified file path and save it into the working directory.
        :param f_p: str, the path of the RHD file.
        """
        # 先加载数据
        self.load_rhd_data(f_p)

        if self.data is None:
            import_settings_window_console("No data to save after loading.")
            return

        try:
            # 创建必要的目录
            amplifier_dir = os.path.join(self.working_dir, 'processed_amplifier_data')
            os.makedirs(amplifier_dir, exist_ok=True)

            # 保存 amplifier_data 到 processed_amplifier_data 目录
            amplifier_data = self.data['amplifier_data']
            for ii in range(amplifier_data.shape[0]):
                fp = os.path.join(amplifier_dir, f'amplifier_channel{ii + 1}.h5')
                with h5py.File(fp, 'w') as ff:
                    ff.create_dataset('dataset_name', data=amplifier_data[ii])
            import_settings_window_console(f"Saved amplifier_data to {amplifier_dir}")

            # 保存 spike_triggers 到 spike_triggers.h5
            spike_triggers_path = os.path.join(self.working_dir, 'spike_triggers.h5')
            save_data_to_h5(spike_triggers_path, self.data['spike_triggers'])
            import_settings_window_console(f"Saved spike_triggers to {spike_triggers_path}")

            # 保存 amplifier_channels 到 amplifier_channels.h5
            amplifier_channels_path = os.path.join(self.working_dir, 'amplifier_channels.h5')
            save_data_to_h5(amplifier_channels_path, self.data['amplifier_channels'])
            import_settings_window_console(f"Saved amplifier_channels to {amplifier_channels_path}")

            import_settings_window_console("All data saved successfully.")

        except Exception as e:
            import_settings_window_console(f"Failed to save data: {str(e)}")

    # 以下文件/文件夹保存到working_dir目录下
    # 读取f_p指引的rhd文件，读取rhd后，根据data['amplifier_data'].shape[0]的值，保存amplifier_data数据到processed_amplifier_data文件夹
    # 保存spike_triggers数据到spike_triggers.h5
    # 保存amplifier_channels数据到amplifier_channels.h5

    def get_data(self):
        """
        获取加载的数据
        :return: dict, the loaded data or None if not loaded.
        """
        return self.data


def load_processed_data(directory, num_files=16):
    dt_list = []
    for ii in range(num_files):
        f_p = os.path.join(directory, 'amplifier_channel{0}.h5'.format(ii + 1))
        with h5py.File(f_p, 'r') as ff:
            dataset = ff['dataset_name'][:]
            dt_list.append(dataset)
        if ii % 10 == 0:
            pass
            # print(f"Loaded data from {f_p}")
    return dt_list


def load_data_from_h5(file_name):
    dt = []
    with h5py.File(file_name, 'r') as hf:
        # 遍历文件中的所有组
        for group_name in hf.keys():
            group = hf[group_name]
            item = {}
            # 遍历组中的所有数据集
            for key in group.keys():
                dataset = group[key]
                if dataset.shape == ():  # 如果数据集是标量
                    item[key] = dataset[()]  # 直接获取其值
                else:
                    item[key] = dataset[:]  # 否则将其作为数组处理
            dt.append(item)
    return dt


def save_data_to_h5(file_name, dt):
    with h5py.File(file_name, 'w') as hf:
        for ii, item in enumerate(dt):
            group = hf.create_group(f"item_{ii + 1}")
            for key, value in item.items():
                group.create_dataset(key, data=value)
    print(f"Data saved to {file_name}")


def sort_key(cn):
    name = cn['custom_channel_name']
    if isinstance(name, bytes):
        name = name.decode('utf-8')

    # 使用正则表达式拆分字母和数字部分
    match = re.match(r"([A-Za-z]+)([0-9]+)", name)
    if match:
        letter_part = match.group(1)
        number_part = int(match.group(2))
        return letter_part, number_part
    else:
        return name, 0  # 如果匹配不到，直接返回原始字符串


class LoadMode(Enum):
    SAVE = 1
    LOAD = 2


if __name__ == "__main__":
    pass

    mode = LoadMode.LOAD

    if mode == LoadMode.SAVE:
        # 开始计时
        tic = time.time()
        loader = RHDDataLoader()
        # loader.load_rhd_data("D:\Dev\LNZN\ArcNeuroViz\\tools\load_intan_rhd_format\sampledata.rhd")
        loader.load_rhd_data("D:\Dev\LNZN\s0633_0615_0690_221219_114735.rhd")
        print(loader.data)
        data = loader.data['amplifier_data']
        spike_triggers = loader.data['spike_triggers']
        print(spike_triggers[0])
        amplifier_channels = loader.data['amplifier_channels']
        print(amplifier_channels[0])
        aux_input_channels = loader.data['aux_input_channels']
        output_dir = 'processed_amplifier_data'
        os.makedirs(output_dir, exist_ok=True)

        # 保存 spike_triggers 到 h5 文件
        save_data_to_h5('spike_triggers.h5', spike_triggers)

        # 保存 amplifier_channels 到 h5 文件
        save_data_to_h5('amplifier_channels.h5', amplifier_channels)

        for i in range(328):
            file_path = os.path.join(output_dir, 'amplifier_channel{0}.h5'.format(i + 1))
            with h5py.File(file_path, 'w') as f:
                f.create_dataset('dataset_name', data=data[i])
        print("文件已成功生成")

        # 结束计时
        toc = time.time()
        # Example: Print the shape of each dataset
        # 打印时间
        print(f"Time elapsed: {toc - tic:.2f} seconds")

    if mode == LoadMode.LOAD:
        tic = time.time()
        output_dir = 'processed_amplifier_data'

        data_list = load_processed_data(output_dir, num_files=32)
        # 加载 spike_triggers.h5 文件
        spike_triggers = load_data_from_h5('spike_triggers.h5')
        # print("Spike Triggers Data:", spike_triggers)

        # 加载 amplifier_channels.h5 文件
        amplifier_channels = load_data_from_h5('amplifier_channels.h5')
        # print("Amplifier Channels Data:", amplifier_channels)
        toc = time.time()
        print(f"Time elapsed: {toc - tic:.2f} seconds")
        # print(amplifier_channels[316])
        # print(amplifier_channels[316]['custom_channel_name'].decode('utf-8'))
        # print(amplifier_channels[0])

        # 对 amplifier_channels 列表进行排序
        sorted_amplifier_channels = sorted(amplifier_channels, key=sort_key)

        # for spike_trigger in spike_triggers:
        #     print(spike_trigger)
        # 打印排序后的结果
        for channel in sorted_amplifier_channels:
            print(channel)
        print(amplifier_channels[316])
