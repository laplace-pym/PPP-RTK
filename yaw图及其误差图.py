import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  # 用于计算均方根误差（RMSE）

def read_data(file_path):
    """读取txt文件并返回一个DataFrame"""
    df = pd.read_csv(file_path, sep=',', header=0)
    print(f"Columns in {file_path}: {df.columns.tolist()}")  # 打印列名，检查是否正确
    return df


def normalize_azimuth(df, column_name='field.azimuth'):
    """将角度归整到0到360之间"""
    df[column_name] = df[column_name] % 360
    df[column_name] = df[column_name].apply(lambda x: x if x >= 0 else x + 360)
    return df


def extract_and_align_data(file1, file2):
    """提取并对齐两个文件的数据"""
    # 读取两个文件
    df1 = read_data(file1)
    df2 = read_data(file2)

    # 检查列名是否包含 'UTC_time' 和 'field.azimuth'
    if 'UTC_time' not in df1.columns or 'field.azimuth' not in df1.columns:
        raise KeyError("One or both of 'UTC_time' and 'field.azimuth' columns are missing in file1.")
    if 'UTC_time' not in df2.columns or 'field.azimuth' not in df2.columns:
        raise KeyError("One or both of 'UTC_time' and 'field.azimuth' columns are missing in file2.")

    # 提取需要的列：UTC_time 和 field.azimuth
    df1 = df1[['UTC_time', 'field.azimuth']]
    df2 = df2[['UTC_time', 'field.azimuth']]

    # 将角度归整到 0 到 360 度之间
    df1 = normalize_azimuth(df1)
    df2 = normalize_azimuth(df2)

    # 转换 UTC_time 为标准格式（如果需要，转换为日期时间格式进行对齐）
    df1['UTC_time'] = pd.to_datetime(df1['UTC_time'], format='%Y%m%d%H%M%S.%f')
    df2['UTC_time'] = pd.to_datetime(df2['UTC_time'], format='%Y%m%d%H%M%S.%f')

    # 合并两个数据框架，按 UTC_time 对齐
    merged_df = pd.merge(df1, df2, on='UTC_time', suffixes=('_1', '_2'))

    # 截取前2000个点
    merged_df = merged_df.iloc[0:18500000]

    return merged_df


def plot_data(merged_df):
    """绘制两张图像，处理周期性误差，并计算误差的统计量"""
    # 计算azimuth的误差
    azimuth_error = merged_df['field.azimuth_1'] - merged_df['field.azimuth_2']

    # 处理周期性误差：将误差调整到 -180 到 180 度之间
    azimuth_error = (azimuth_error + 180) % 360 - 180

    # 计算误差的统计量
    max_error = azimuth_error.max()  # 最大误差
    min_error = azimuth_error.min()  # 最小误差
    mean_error = azimuth_error.mean()  # 平均误差
    rmse_error = np.sqrt((azimuth_error ** 2).mean())  # 均方根误差（RMSE）

    print(f"Maximum Azimuth Error: {max_error:.2f} degrees")
    print(f"Minimum Azimuth Error: {min_error:.2f} degrees")
    print(f"Mean Azimuth Error: {mean_error:.2f} degrees")
    print(f"RMSE Azimuth Error: {rmse_error:.2f} degrees")

    # 第1张图：field.azimuth 的值
    plt.figure(figsize=(10, 5))
    plt.plot(merged_df.index, merged_df['field.azimuth_1'], label='field.azimuth_1', color='blue')
    plt.plot(merged_df.index, merged_df['field.azimuth_2'], label='field.azimuth_2', color='orange')
    plt.xlabel('Aligned Points Count')
    plt.ylabel('field.azimuth Value')
    plt.title('Field Azimuth Values vs. Aligned Points')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 第2张图：field.azimuth 的误差，处理周期性问题
    plt.figure(figsize=(10, 5))
    plt.plot(merged_df.index, azimuth_error, label='Azimuth Error', color='red')
    plt.xlabel('Aligned Points Count')
    plt.ylabel('Azimuth Error Value')
    plt.title('Field Azimuth Error vs. Aligned Points')
    plt.legend()
    plt.grid(True)
    plt.show()


# 输入文件路径
file1 = 'D:/personal/Desktop/2024.12.2/chushi/q_5.txt'  # 第一个txt文件路径,blue
file2 = 'D:/personal/Desktop/2024.12.2/chushi/n_gaosi4.txt'  # 第二个txt文件路径

# 提取并对齐数据
try:
    merged_df = extract_and_align_data(file1, file2)
    # 绘制图像
    plot_data(merged_df)
except KeyError as e:
    print(e)
