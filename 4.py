import csv


# 读取txt文件并筛选出field.pos_qual为4的所有数据
def filter_pos_qual(input_file, output_file):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        # 筛选出pos_qual为4的数据
        filtered_data = [row for row in reader if float(row['field.pos_qual']) == 4.0]

    # 将筛选后的数据写入到新文件
    with open(output_file, 'w', newline='') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # 写入文件头
        writer.writeheader()

        # 写入筛选后的数据
        writer.writerows(filtered_data)

    print(f"筛选完成，结果已保存到 {output_file}")


# 调用函数
input_file = 'D:\\personal\\Desktop\\2024.12.2\\chushi\\q_gaosi4.txt'  # 输入的txt文件路径
output_file = 'D:\\personal\\Desktop\\2024.12.2\\chushi\\q_5.txt'  # 输出的txt文件路径
filter_pos_qual(input_file, output_file)
