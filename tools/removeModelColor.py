import os

def process_txt_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('v '):
                parts = line.strip().split()
                if len(parts) > 4:
                    new_line = ' '.join(parts[:4]) + '\n'
                    outfile.write(new_line)
                else:
                    outfile.write(line)
            else:
                outfile.write(line)

def process_folder(input_folder_path, output_folder_path):
    # 检查输入文件夹是否存在
    if not os.path.isdir(input_folder_path):
        print(f"Error: Folder does not exist at {input_folder_path}")
        return

    # 创建输出文件夹如果不存在
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 获取输入文件夹中的所有txt文件
    files = [f for f in os.listdir(input_folder_path) if f.endswith('.txt')]
    for filename in files:
        input_file = os.path.join(input_folder_path, filename)
        output_file = os.path.join(output_folder_path, filename)
        process_txt_file(input_file, output_file)
        print(f"Processed file saved as {output_file}")

if __name__ == "__main__":
    input_folder_path = "..\\model\\regions"
    output_folder_path = "..\\model\\processed_regions"
    process_folder(input_folder_path, output_folder_path)
    print("All files have been processed.")
