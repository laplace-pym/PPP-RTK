import math
import csv

def LatLon2XY(latitude, longitude):
    """
    :param latitude, longitude: 纬度、经度
    :return x, y: 高斯投影后的坐标
    """
    latitude = float(latitude)
    longitude = float(longitude)
    a = 6378137.0
    e2 = 0.0066943799013
    latitude2Rad = (math.pi / 180.0) * latitude

    beltNo = int((longitude + 1.5) / 3.0)
    L = beltNo * 3
    l0 = longitude - L
    tsin = math.sin(latitude2Rad)
    tcos = math.cos(latitude2Rad)
    t = math.tan(latitude2Rad)
    m = (math.pi / 180.0) * l0 * tcos
    et2 = e2 * pow(tcos, 2)
    et3 = e2 * pow(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
        4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
    N = a / math.sqrt(1 - et3)

    x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
            61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
            5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)
    return x, y

def calculate_distance(x1, y1, x2, y2):
    """
    计算两点间的欧几里得距离
    :param x1, y1: 第一个点的高斯投影坐标
    :param x2, y2: 第二个点的高斯投影坐标
    :return: 距离值
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def convert_coordinates(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['field.x', 'field.y', 'cumulative_distance']  # 增加累计距离字段
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        previous_x, previous_y = None, None  # 用于存储上一行的坐标
        total_distance = 0  # 初始化总距离为0

        for row in reader:
            try:
                latitude = row['corrected_latitude']
                longitude = row['corrected_longitude']

                # 检查经纬度是否为空，去除前后空格，避免读取错误
                if not latitude or not longitude or latitude.strip() == '' or longitude.strip() == '':
                    print(f"经纬度数据缺失: {row}, 跳过此行")
                    continue  # 跳过缺失经纬度的行

                # 转换为高斯投影坐标
                x, y = LatLon2XY(latitude, longitude)
                row['field.x'] = x
                row['field.y'] = y

                # 计算距离，如果有上一行数据
                if previous_x is not None and previous_y is not None:
                    distance = calculate_distance(previous_x, previous_y, x, y)
                    total_distance += distance  # 累加距离

                # 将累计距离添加到当前行
                row['cumulative_distance'] = total_distance

                writer.writerow(row)

                # 更新上一行坐标
                previous_x, previous_y = x, y

            except ValueError as e:
                print(f"无法解析数据行: {row}，错误: {e}")

    print(f"转换完成，结果已保存到 {output_file}")

# 输入输出文件路径
input_txt = 'D:\\personal\\Desktop\\ins.txt'  # 输入文件路径
output_txt = 'D:\\personal\\Desktop\\ms6111.txt'  # 输出文件路径
convert_coordinates(input_txt, output_txt)
