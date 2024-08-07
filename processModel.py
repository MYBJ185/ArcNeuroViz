def process_txt_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) > 4:
                new_line = ' '.join(parts[:4]) + '\n'
                outfile.write(new_line)
            else:
                outfile.write(line)

input_file = 'model\\model.txt'  # 输入文件名
output_file = 'model\\newModel.txt'  # 输出文件名

process_txt_file(input_file, output_file)
print(f"Processed file saved as {output_file}")
