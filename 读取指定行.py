def read_and_extract_lines(input_file, output_file):
    # 打开输入文件和输出文件
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # 读取所有行
        lines = infile.readlines()

        # 创建一个列表，存储需要输出的行
        selected_lines = []

        # 第一行
        selected_lines.append(lines[0])

        # 7530 到 12000 行
        # selected_lines.extend(lines[7530 - 1:12000])  # 注意索引是从0开始的，所以行号要减去1

        # 14120 到 22420 行
        # selected_lines.extend(lines[14120 - 1:22420])

        # 24340 到 28050 行
        selected_lines.extend(lines[27750 - 1:28050])

        # 将选中的行写入输出文件
        outfile.writelines(selected_lines)

    print(f"数据已成功提取到 {output_file} 文件中。")


# 输入和输出文件路径
input_file = 'D:\\personal\\Desktop\\2\\q_1.txt'  # 请替换为你的输入文件路径
output_file = 'D:\\personal\\Desktop\\2\\q_xd3.txt'  # 请替换为你希望输出的文件路径

# 调用函数执行操作
read_and_extract_lines(input_file, output_file)
