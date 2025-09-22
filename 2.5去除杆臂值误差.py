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
    df = pd.read_csv(file_path, sep=",")  # 假设文件是以逗号分隔的
    df = df[columns]
    return df

# 修正并保存文件1的数据
def correct_file1_data(file1_path, file1_columns, file2_df):
    file1_df = read_file(file1_path, file1_columns)

    # 使用merge对齐数据
    merged_df = pd.merge(file1_df, file2_df[['UTC_time', 'field.fheading']], on="UTC_time", how="inner")

    corrected_latitudes = []
    corrected_longitudes = []
    corrected_heights = []

    # 遍历对齐后的数据，进行修正
    for index, row in merged_df.iterrows():
        gpsData = {
            'latitude': row['field.latitude'],  # 使用文件1中的经纬度数据
            'longitude': row['field.longitude'],
            'phi': row['field.fheading'],  # 从文件2获取fheading
            'height': row['field.height']  # 使用文件1中的height
        }

        corrected_lat, corrected_lon, corrected_height = correct_latitude_longitude(gpsData)

        corrected_latitudes.append(corrected_lat)
        corrected_longitudes.append(corrected_lon)
        corrected_heights.append(corrected_height)

    # 将修正后的数据加入到原数据框
    merged_df['corrected_latitude'] = corrected_latitudes
    merged_df['corrected_longitude'] = corrected_longitudes
    merged_df['corrected_height'] = corrected_heights

    # 保存修正后的数据到新的txt文件
    file1_output_path = 'D:\\personal\\Desktop\\20241130\\utc\\2n_corr.txt'  # 保存路径
    file1_output = merged_df[['UTC_time', 'corrected_latitude', 'corrected_longitude', 'corrected_height', 'satellites_used']]
    file1_output.to_csv(file1_output_path, sep=',', index=False)
    print(f"修正后的文件1已保存到 '{file1_output_path}' 文件")

# 修正并保存文件2的数据
def correct_file2_data(file2_path, file2_columns):
    file2_df = read_file(file2_path, file2_columns)

    corrected_latitudes = []
    corrected_longitudes = []
    corrected_heights = []

    # 遍历文件2的数据，进行修正
    for index, row in file2_df.iterrows():
        gpsData = {
            'latitude': row['field.latitude'],  # 使用文件2中的经纬度数据
            'longitude': row['field.longitude'],
            'phi': row['field.fheading'],  # 使用文件2中的fheading
            'height': row['field.height']  # 使用文件2中的height作为height
        }

        corrected_lat, corrected_lon, corrected_height = correct_latitude_longitude(gpsData)

        corrected_latitudes.append(corrected_lat)
        corrected_longitudes.append(corrected_lon)
        corrected_heights.append(corrected_height)

    # 将修正后的数据加入到原数据框
    file2_df['corrected_latitude'] = corrected_latitudes
    file2_df['corrected_longitude'] = corrected_longitudes
    file2_df['corrected_height'] = corrected_heights

    # 保存修正后的数据到新的txt文件
    file2_output_path = 'D:\\personal\\Desktop\\20241130\\qianxunheading\\2q_corr.txt'  # 保存路径
    file2_output = file2_df[['UTC_time', 'corrected_latitude', 'corrected_longitude', 'corrected_height', 'field.fheading', 'field.msvs']]
    file2_output.to_csv(file2_output_path, sep=',', index=False)
    print(f"修正后的文件2已保存到 '{file2_output_path}' 文件")

# 主程序
def main():
    # 文件1和文件2的路径
    file1_path = 'D:\\personal\\Desktop\\laozong\\n_utc.txt'  # 文件1路径
    file2_path = 'D:\\personal\\Desktop\\laozong\\q_out.txt'  # 文件2路径

    # 文件1和文件2需要提取的列
    file1_columns = ['UTC_time', 'field.latitude', 'field.longitude', 'field.height', 'satellites_used', 'field.fheading']
    file2_columns = ['UTC_time', 'field.latitude', 'field.longitude', 'field.height', 'field.msvs']

    # 读取文件2数据，供文件1使用fheading字段
    file2_df = read_file(file2_path, file2_columns)

    # 修正并保存文件1数据
    correct_file1_data(file1_path, file1_columns, file2_df)

    # 修正并保存文件2数据
    correct_file2_data(file2_path, file2_columns)

if __name__ == "__main__":
    main()
