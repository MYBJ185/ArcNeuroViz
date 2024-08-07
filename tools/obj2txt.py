import os

def rename_files_to_txt(folder_path):
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"Error: Folder does not exist at {folder_path}")
        return

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # 获取文件名和扩展名
            base_name = os.path.splitext(filename)[0]
            new_file_path = os.path.join(folder_path, base_name + '.txt')
            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {base_name}.txt")
def rename_files_to_obj(folder_path):
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"Error: Folder does not exist at {folder_path}")
        return

    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # 获取文件名和扩展名
            base_name = os.path.splitext(filename)[0]
            new_file_path = os.path.join(folder_path, base_name + '.obj')
            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {base_name}.obj")

if __name__ == "__main__":
    folder_path = "..\\model\\regions"
    # rename_files_to_txt(folder_path)
    # print("All files have been renamed to .txt")
    rename_files_to_obj(folder_path)
    print("All files have been renamed to .obj")
