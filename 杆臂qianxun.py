import math
import pandas as pd

# 常数
a = 6378137.0  # WGS84 椭球的长半轴（单位：米）
f = 1 / 298.257223563  # WGS84 椭球的扁率
M_PI = math.pi  # 圆周率

# 修正经纬度的函数
def correct_latitude_longitude(gpsData):
    latitude = gpsData['latitude']
    longitude = gpsData['longitude']
    phi = gpsData['phi']
    height = gpsData['height']

    # 假设杆臂值为0.145
    arm_length = 0.78

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

# 优化：使用 apply() 进行批量修正
def apply_correction(row):
    gpsData = {
        'latitude': row['field.latitude'],
        'longitude': row['field.longitude'],
        'phi': row['field.fheading'],
        'height': row['field.height']
    }
    corrected_lat, corrected_lon, corrected_height = correct_latitude_longitude(gpsData)
    return pd.Series([corrected_lat, corrected_lon, corrected_height], index=['corrected_latitude', 'corrected_longitude', 'corrected_height'])

# 修正并保存数据
def correct_and_save_data(file_path, output_path):
    # 读取数据
    columns = [ 'field.latitude', 'field.longitude', 'field.height', 'field.fheading', 'UTC_time', 'field.msvs', 'field.pos_qual']
    df = read_file(file_path, columns)

    if df.empty:
        print("文件为空，退出程序")
        return

    # 使用 apply() 方法批量修正数据
    print("开始批量修正数据...")
    corrected_data = df.apply(apply_correction, axis=1)

    # 将修正后的数据加入到原数据框
    df = pd.concat([df, corrected_data], axis=1)

    # 保持原来的 `field.msvs` 和 `field.pos_qual` 不变
    df_output = df[['UTC_time', 'corrected_latitude', 'corrected_longitude', 'corrected_height', 'field.fheading', 'field.msvs', 'field.pos_qual']]

    # 保存修正后的数据到新的txt文件
    try:
        df_output.to_csv(output_path, sep=',', index=False)
        print(f"修正后的数据已保存到 '{output_path}' 文件")
    except Exception as e:
        print(f"保存文件出错: {e}")

# 主程序
def main():
    # 用户输入文件路径
    file_path = "D:\\personal\\Desktop\\2024.12.2\\chushi\\q_1.txt"  # 输入文件路径
    output_path = "D:\\personal\\Desktop\\2024.12.2\\chushi\\q_corrected.txt"  # 输出文件路径

    # 修正并保存数据
    correct_and_save_data(file_path, output_path)

if __name__ == "__main__":
    main()
