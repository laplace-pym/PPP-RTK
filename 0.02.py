import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data(file_path):
    """
    读取文本文件并返回DataFrame，确保提取所需的列
    """
    data = pd.read_csv(file_path, delimiter=',', encoding='utf-8')

    if 'UTC_time' not in data.columns:
        data = pd.read_csv(file_path, delimiter=',', encoding='utf-8', header=0)

    # 确保UTC_time列是浮动数字类型
    data['UTC_time'] = pd.to_numeric(data['UTC_time'], errors='coerce')

    data = data[['UTC_time', 'field.x', 'field.y']]
    data = data.dropna(subset=['UTC_time'])

    return data


def align_data(file1_data, file2_data):
    """
    根据UTC_time对齐两个数据集，并打印对齐的UTC_time, x, y
    """
    file1_data['UTC_time'] = file1_data['UTC_time'].round(2)
    file2_data['UTC_time'] = file2_data['UTC_time'].round(2)

    aligned_data = pd.merge(file1_data, file2_data, on='UTC_time', suffixes=('_file1', '_file2'))

    if len(aligned_data) == 0:
        print("没有匹配的 UTC_time，请检查数据。")
    else:
        print(f"对齐后的数据行数：{len(aligned_data)}")
        print(aligned_data.head())

    return aligned_data


def calculate_error(df):
    """
    计算误差：sqrt((file1_y - file2_y)^2 + (file1_x - file2_x)^2)
    """
    x_diff = df['field.x_file1'] - df['field.x_file2']
    y_diff = df['field.y_file1'] - df['field.y_file2']
    error = np.sqrt(x_diff ** 2 + y_diff ** 2)
    return error


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


def find_error_below_threshold(df, threshold=0.02, output_file="error_below_threshold.txt"):
    """
    找到误差小于指定阈值（默认为0.02）的UTC_time，并输出到txt文件
    """
    error = calculate_error(df)

    # 筛选误差小于阈值的行
    below_threshold = df[error < threshold]

    if len(below_threshold) > 0:
        print(f"误差小于 {threshold} 的 UTC_time：")
        with open(output_file, 'w') as f:
            f.write("误差小于 {0} 的 UTC_time:\n".format(threshold))
            # 将 UTC_time 写入到文件
            for utc_time in below_threshold['UTC_time']:
                f.write(f"{utc_time}\n")
        print(f"误差小于 {threshold} 的 UTC_time 已保存到 '{output_file}' 文件中。")
    else:
        print(f"没有误差小于 {threshold} 的数据。")


def main(file1_path, file2_path):
    """
    主函数，整合所有步骤
    """
    # 读取数据
    file1_data = read_data(file1_path)
    file2_data = read_data(file2_path)

    # 根据UTC_time对齐数据，并打印对齐的UTC_time, x, y
    aligned_data = align_data(file1_data, file2_data)

    # 如果没有对齐的数据，终止后续处理
    if len(aligned_data) == 0:
        print("没有对齐数据，程序终止。")
        return

    # 截取第1到第20000个点的数据（根据实际数据长度调整）
    aligned_data_subset = aligned_data.iloc[0:len(aligned_data)]

    # 计算误差
    error = calculate_error(aligned_data_subset)

    # 输出误差的统计信息
    print(f"均值误差: {np.mean(error)}")
    print(f"最大误差: {np.max(error)}")
    print(f"最小误差: {np.min(error)}")
    print(f"中位数误差: {np.median(error)}")

    # 计算均方根误差 (RMSE)
    rmse = np.sqrt(np.mean(error ** 2))
    print(f"均方根误差 (RMSE): {rmse}")

    # 绘制误差图
    plot_error(error)

    # 绘制轨迹图
    plot_trajectory(aligned_data_subset)

    # 找到误差小于0.02的UTC_time并输出到txt文件
    find_error_below_threshold(aligned_data_subset, threshold=0.02)


# 输入文件路径
file1_path = 'D:/personal/Desktop/2024.12.2/chushi/q_gaosi4.txt'  # 替换为实际文件路径
file2_path = 'D:/personal/Desktop/2024.12.2/chushi/n_gaosi4.txt'  # 替换为实际文件路径

# 执行主程序
main(file1_path, file2_path)
