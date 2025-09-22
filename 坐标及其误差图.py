import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data(file_path):
    """
    读取文本文件并返回DataFrame，确保提取所需的列
    仅筛选出field.x和field.y小于10000的点
    """
    data = pd.read_csv(file_path, delimiter=',', encoding='utf-8')

    # 如果列名中没有'UTC_time'，说明表头没有正确解析
    if 'UTC_time' not in data.columns:
        data = pd.read_csv(file_path, delimiter=',', encoding='utf-8', header=0)

    # 确保UTC_time列是浮动数字类型
    data['UTC_time'] = pd.to_numeric(data['UTC_time'], errors='coerce')  # 将无法转换的值变为NaN

    # 提取所需的列
    data = data[['UTC_time', 'field.x', 'field.y']]

    # 删除含有NaN的行
    data = data.dropna(subset=['UTC_time'])

    # 筛选出field.x和field.y小于10000的点
    data = data[(data['field.x'].abs() < 2000000) & (data['field.y'].abs() < 2000000)]
    return data


def align_data(file1_data, file2_data):
    """
    根据UTC_time对齐两个数据集，并打印对齐的UTC_time, x, y
    """
    file1_data['UTC_time'] = file1_data['UTC_time'].round(2)  # 保留两位小数
    file2_data['UTC_time'] = file2_data['UTC_time'].round(2)  # 保留两位小数

    # 对齐UTC_time，保留完全匹配的行
    aligned_data = pd.merge(file1_data, file2_data, on='UTC_time', suffixes=('_file1', '_file2'))

    if len(aligned_data) == 0:
        print("没有匹配的 UTC_time，请检查数据。")
    else:
        print(f"对齐后的数据行数：{len(aligned_data)}")
        print(aligned_data.head())  # 输出对齐后的数据头部

    # 仅取匹配上的前5000000个时间戳点
    aligned_data = aligned_data.iloc[0:16500]
    return aligned_data


def calculate_error(df):
    """
    计算误差：sqrt((file1_y - file2_y)^2 + (file1_x - file2_x)^2)
    """
    x_diff = df['field.x_file1'] - df['field.x_file2']
    y_diff = df['field.y_file1'] - df['field.y_file2']
    error = np.sqrt(x_diff ** 2 + y_diff ** 2)
    return error


def filter_error(error, threshold=2000000000000):
    """
    过滤掉误差大于阈值的点
    """
    return error[error < threshold]


def plot_error(error):
    """
    生成误差图
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(error)), error, marker='o', linestyle='-', color='b')
    plt.title('Error vs Points')
    plt.xlabel('Point Index')
    plt.ylabel('Error (sqrt(x^2 + y^2))')
    plt.grid(True)
    plt.show()


def plot_trajectory(aligned_data):
    """
    绘制对齐时间戳对应的y, x坐标轨迹图
    """
    plt.figure(figsize=(10, 6))
    plt.plot(aligned_data['field.y_file1'], aligned_data['field.x_file1'], label='Trajectory from File 1', marker='o',
             linestyle='-', color='b')
    plt.plot(aligned_data['field.y_file2'], aligned_data['field.x_file2'], label='Trajectory from File 2', marker='x',
             linestyle='-', color='r')
    plt.title('Trajectory Plot: Y vs X Coordinates')
    plt.xlabel('Y Coordinate')
    plt.ylabel('X Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()


def main(file1_path, file2_path):
    """
    主函数，整合所有步骤
    """
    # 读取数据
    file1_data = read_data(file1_path)
    file2_data = read_data(file2_path)

    # 根据UTC_time对齐数据
    aligned_data = align_data(file1_data, file2_data)

    # 如果没有对齐的数据，终止后续处理
    if len(aligned_data) == 0:
        print("没有对齐数据，程序终止。")
        return

    # 计算误差
    error = calculate_error(aligned_data)

    # 过滤误差大于阈值的点
    filtered_error = filter_error(error)

    # 输出过滤后的误差统计信息
    print(f"均值误差: {np.mean(filtered_error)}")
    print(f"最大误差: {np.max(filtered_error)}")
    print(f"最小误差: {np.min(filtered_error)}")
    print(f"中位数误差: {np.median(filtered_error)}")

    # 计算均方根误差 (RMSE)
    rmse = np.sqrt(np.mean(filtered_error ** 2))
    print(f"均方根误差 (RMSE): {rmse}")

    # 绘制误差图
    plot_error(filtered_error)

    # 绘制轨迹图（仅对过滤后的数据绘制）
    filtered_aligned_data = aligned_data.iloc[:len(filtered_error)]  # 保证对齐数据与误差数据相匹配
    plot_trajectory(filtered_aligned_data)


# 输入文件路径
file1_path = 'D://personal//Desktop//2//gres3.txt'  # 替换为实际文件路径
file2_path = 'D://personal//Desktop//2//k3.txt'  # 替换为实际文件路径

# 执行主程序
main(file1_path, file2_path)
