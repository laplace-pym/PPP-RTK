# 定义输入文件和输出文件的路径
input_file = 'D:\\personal\\Desktop\\2\\q_5.txt'  # 假设原数据存储在data.txt中
output_file = 'D:\\personal\\Desktop\\2\\q_shai5.txt'  # 输出文件为filtered_data.txt

# 打开输入文件并读取数据
with open(input_file, 'r') as infile:
    # 读取所有行
    lines = infile.readlines()

# 创建一个空列表来存储筛选后的数据
filtered_lines = []

# 处理文件的每一行
for line in lines:
    # 分割每行数据，假设数据以逗号分隔
    columns = line.strip().split(',')

    # 判断 pos_qual 是否为 4 或 5
    if len(columns) > 2 and columns[2] in ['4']:
        filtered_lines.append(line)

# 将筛选后的数据写入到新文件
with open(output_file, 'w') as outfile:
    # 写入每一行数据
    outfile.writelines(filtered_lines)

print(f"筛选后的数据已保存到 {output_file}")
