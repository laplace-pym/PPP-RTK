# 定义输入和输出文件路径
input_file = 'D:\\personal\\Desktop\\gnss_gaosi.txt'
output_file = 'D:\\personal\\Desktop\\gnss_gaosi66.txt'

# 定义需要减去的值
subtract_x = 3559618.0557950763
subtract_y = 377306.6823826219

# 读取输入文件内容
with open(input_file, 'r') as infile:
    lines = infile.readlines()

# 解析标题行，找到 x 和 y 的列索引
header = lines[0].strip().split(',')
x_index = header.index('field.x')
y_index = header.index('field.y')

# 打开输出文件进行写入
with open(output_file, 'w') as outfile:
    # 写入标题行
    outfile.write(','.join(header) + '\n')

    # 逐行处理文件
    for line in lines[1:]:  # 跳过标题行
        columns = line.strip().split(',')

        # 打印当前行数据和列数（用于调试）
        # print(f"Processing line: {line}")
        # print(f"Number of columns: {len(columns)}")

        # 确保这一行的数据列数足够
        if len(columns) > max(x_index, y_index):  # 确保有足够的列
            try:
                # 获取原始的x和y值
                x = float(columns[x_index])
                y = float(columns[y_index])

                # 计算新的x和y值
                new_x = x - subtract_x
                new_y = y - subtract_y

                # 更新x和y列
                columns[x_index] = str(new_x)
                columns[y_index] = str(new_y)

                # 写入更新后的行，其他列保持不变
                outfile.write(','.join(columns) + '\n')
            except ValueError:
                # 如果数据无法转换为浮点数，跳过这一行
                print(f"Skipping line due to invalid data: {line}")
                continue
        else:
            # 如果列数不足，跳过这一行
            print(f"Skipping line due to insufficient columns: {line}")

print("处理完成，输出文件已保存到", output_file)
