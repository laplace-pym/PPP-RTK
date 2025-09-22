import math
import csv
import os


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


def convert_coordinates(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"输入文件 {input_file} 不存在，请检查路径")
        return

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8',
                                                                 newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['field.x', 'field.y']  # 增加高斯投影坐标字段名
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            # 输出调试信息，查看当前行数据
            # print(f"当前行数据：{row}")  # 打印出当前行数据，帮助调试

            try:
                latitude = row['latitude']
                longitude = row['longitude']

                # 检查经纬度是否为空，去除前后空格，避免读取错误
                if not latitude.strip() or not longitude.strip():
                    print(f"经纬度数据缺失: {row}, 跳过此行")
                    continue  # 跳过缺失经纬度的行

                # 转换为高斯投影坐标
                x, y = LatLon2XY(latitude, longitude)
                row['field.x'] = x
                row['field.y'] = y
                writer.writerow(row)

            except ValueError as e:
                print(f"无法解析数据行: {row}，错误: {e}")

    print(f"转换完成，结果已保存到 {output_file}")


# 输入输出文件路径，使用os.path.join确保路径兼容
input_txt = r'D:\personal\Desktop\gnss_utc.txt'  # 输入文件路径
output_txt = r'D:\personal\Desktop\gnss_gaos2.txt'  # 输出文件路径
convert_coordinates(input_txt, output_txt)
