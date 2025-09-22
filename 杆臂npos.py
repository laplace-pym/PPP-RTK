import math
import pandas as pd

# 常数
a = 6378137.0  # WGS84 椭球的长半轴（单位：米）
f = 1 / 298.257223563  # WGS84 椭球的扁率
M_PI = math.pi  # 圆周率
height =17.22 # 高度

# 修正经纬度的函数
def correct_latitude_longitude(gpsData):
    latitude = gpsData['latitude']
    longitude = gpsData['longitude']
    phi = gpsData['phi']
    # height = gpsData['height']

    # 假设杆臂值为0.145
    arm_length = -0.635

    # 计算子午圈曲率半径 Rm 和法线曲率半径 Rn
    latitude_rad = latitude * M_PI / 180.0
    sin_lat = math.sin(latitude_rad)

    # 计算 Rm 和 Rn
    Rm = a * (1 - 2 * f + 3 * f * sin_lat * sin_lat)
    Rn = a * (1 + f * sin_lat * sin_lat)

    # 去除杆臂误差的修正
    corrected_latitude = latitude + (arm_length * math.cos(math.radians(phi)) / (Rm + height)) * 180.0 / M_PI
    corrected_longitude = longitude + (arm_length * math.sin(math.radians(phi)) /((Rn + height) * math.cos(latitude_rad))) * 180.0 / M_PI

    return corrected_latitude, corrected_longitude, height

# 读取文件并提取数据
def read_file(file_path, columns):
    try:
        df = pd.read_csv(file_path, sep=",")  # 假设文件是以逗号分隔的
        print(f"文件 {file_path} 成功读取，包含 {len(df)} 行数据")
        df = df[columns]
        return df
    except Exception as e:
        print(f"读取文件出错: {e}")
        return pd.DataFrame()

# 修正并保存数据
def correct_and_save_data(file_path, output_path):
    # 读取数据
    columns = ['UTC_time', 'field.latitude', 'field.longitude', 'field.fheading']
    df = read_file(file_path, columns)

    if df.empty:
        print("文件为空，退出程序")
        return

    corrected_latitudes = []
    corrected_longitudes = []
    corrected_heights = []

    # 逐行处理数据
    for index, row in df.iterrows():
        # print(f"开始处理第 {index} 行数据...")

        if pd.isna(row['field.fheading']):
            print(f"警告: 第 {index} 行缺少 fheading 数据，跳过该行")
            continue

        gpsData = {
            'latitude': row['field.latitude'],
            'longitude': row['field.longitude'],
            'phi': row['field.fheading'],
            # 'height': row['field.height']
        }

        # 修正数据
        corrected_lat, corrected_lon, corrected_height = correct_latitude_longitude(gpsData)

        corrected_latitudes.append(corrected_lat)
        corrected_longitudes.append(corrected_lon)
        corrected_heights.append(corrected_height)

        print(f"第 {index} 行处理完成")

    # 将修正后的数据加入到原数据框
    df['corrected_latitude'] = corrected_latitudes
    df['corrected_longitude'] = corrected_longitudes
    # df['corrected_height'] = corrected_heights

    # 保存修正后的数据到新的txt文件
    df_output = df[['UTC_time', 'corrected_latitude', 'corrected_longitude', 'field.fheading']]
    try:
        df_output.to_csv(output_path, sep=',', index=False)
        print(f"修正后的数据已保存到 '{output_path}' 文件")
    except Exception as e:
        print(f"保存文件出错: {e}")

# 主程序
def main():
    # # 用户输入文件路径
    # file_path = input("请输入输入文件的路径: ")  # 提示用户输入文件路径
    # output_path = input("请输入输出文件的路径: ")  # 提示用户输入输出文件路径

    # 调试：只取前100行进行测试
    file_path = "D:\\personal\\Desktop\\12.13\\1ins_extract_utc.txt"  # 可以硬编码路径进行测试
    output_path = "D:\\personal\\Desktop\\12.13\\1ins_ganbi.txt"

    # 修正并保存数据
    correct_and_save_data(file_path, output_path)

if __name__ == "__main__":
    main()
