import csv

# 定义中国的经纬度范围
min_latitude = 18.0  # 最小纬度
max_latitude = 53.0  # 最大纬度
min_longitude = 73.0  # 最小经度
max_longitude = 135.0  # 最大经度


def filter_coordinates(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)  # 使用DictReader来处理列名
        fieldnames = reader.fieldnames  # 获取列名

        # 确保有经纬度和高度的列
        # if 'corrected_latitude' not in fieldnames or 'corrected_longitude' not in fieldnames or 'corrected_height' not in fieldnames:
        if 'latitude' not in fieldnames or 'longitude' not in fieldnames:
            print("输入文件中缺少必需的经纬度或高度字段")
            return

        # 初始化csv写入器
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头

        # 逐行读取并过滤
        for row in reader:
            try:
                # 获取经纬度和高度
                latitude = float(row['latitude'])
                longitude = float(row['longitude'])
                # altitude = row['corrected_height']  # 高度

                # 检查坐标是否在中国境内
                if min_latitude <= latitude <= max_latitude and min_longitude <= longitude <= max_longitude:
                    writer.writerow(row)
            except ValueError:
                continue  # 如果有无效数据，跳过此行



# 使用示例
input_file = 'D:\\personal\\Desktop\\2\\q_xd1.txt'  # 输入文件路径
output_file = 'D:\\personal\\Desktop\\2\\q_xd1.txt'  # 输出文件路径

filter_coordinates(input_file, output_file)
5