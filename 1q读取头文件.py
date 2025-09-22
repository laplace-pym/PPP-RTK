import csv

# 将度分格式转换为十进制度格式
def dms_to_decimal(degrees, minutes):
    return degrees + minutes / 60

# 将 N/S 和 E/W 转换为正负号
def convert_to_decimal(lat, lon):
    if not lat or not lon:
        return None, None  # 返回空值以表示错误数据

    lat_deg = float(lat[:2])  # 纬度的度数
    lat_min = float(lat[2:])  # 纬度的分数
    lon_deg = float(lon[:3])  # 经度的度数
    lon_min = float(lon[3:])  # 经度的分数

    latitude = dms_to_decimal(lat_deg, lat_min)
    longitude = dms_to_decimal(lon_deg, lon_min)

    # 如果是南纬（S）或西经（W），就取负值
    if lat[0] == 'S':
        latitude = -latitude
    if lon[0] == 'W':
        longitude = -longitude

    return latitude, longitude

# 提取并转换数据
def extract_and_convert(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        lines = infile.readlines()

    # 保存结果
    output_data = []

    for line in lines:
        if line.startswith('$GPGGA'):
            parts = line.strip().split(',')

            # 确保行数据有效，避免索引错误
            if len(parts) < 15:  # 若数据不完整，跳过该行
                continue

            # 提取时间、纬度、经度
            time = parts[1]
            latitude = parts[2]
            lat_hemisphere = parts[3]  # N/S
            longitude = parts[4]
            lon_hemisphere = parts[5]  # E/W

            # 提取状态量（在第7位）
            status = parts[6]

            # 提取卫星数（在第8位）
            satellite_count = parts[7]

            # 转换经纬度为十进制度，确保不会转换空值
            latitude, longitude = convert_to_decimal(latitude, longitude)
            if latitude is None or longitude is None:  # 如果经纬度转换失败，跳过该行
                continue

            # 统一时间格式，假设日期固定为20250219
            formatted_time = '20250221' + time[:2] + time[2:4] + time[4:6] + '.' + time[7:]

            # 构建输出数据
            output_data.append({
                'UTC_time': formatted_time,
                'latitude': latitude,
                'longitude': longitude,
                'field.Position_status': status,
                'field.dual_fre_satellites': satellite_count
            })

    # 将结果写入输出文件
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['UTC_time', 'latitude', 'longitude', 'field.Position_status', 'field.dual_fre_satellites'])
        writer.writeheader()
        writer.writerows(output_data)

# 输入文件路径和输出文件路径
input_file = 'D:\\personal\\Desktop\\0221bag\\qianxun.txt'
output_file = 'D:\\personal\\Desktop\\0221bag\\q.txt'

# 执行提取和转换操作
extract_and_convert(input_file, output_file)

print(f"数据已从 {input_file} 提取并转换，结果保存到 {output_file}.")
