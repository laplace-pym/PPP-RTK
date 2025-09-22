import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data(file_path):
    """
    读取文本文件并返回DataFrame，确保提取所需的列
    """
    # 假设文件是用逗号分隔的
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

    return data


def align_data(file1_data, file2_data):
    """
    根据UTC_time对齐两个数据集，并打印对齐的UTC_time, x, y
    """
    # 确保UTC_time列为浮动数字类型，便于对齐
    file1_data['UTC_time'] = file1_data['UTC_time'].astype(float)
    file2_data['UTC_time'] = file2_data['UTC_time'].astype(float)

    # 对齐UTC_time，保留完全匹配的行
    aligned_data = pd.merge(file1_data, file2_data, on='UTC_time', suffixes=('_file1', '_file2'))

    # 打印对齐的UTC_time, x, y
    for _, row in aligned_data.iterrows():
        print(f"UTC_time: {row['UTC_time']} | X_file1: {row['field.x_file1']} | Y_file1: {row['field.y_file1']}")
        print(f"UTC_time: {row['UTC_time']} | X_file2: {row['field.x_file2']} | Y_file2: {row['field.y_file2']}")

    return aligned_data


def calculate_error(df):
    """
    计算误差：sqrt((file1_y - file2_y)^2 + (file1_x - file2_x)^2)
    """
    # 将 x 和 y 交换
    x_diff = df['field.y_file1'] - df['field.y_file2']
    y_diff = df['field.x_file1'] - df['field.x_file2']
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
    横坐标是y坐标，纵坐标是x坐标
    """
    plt.figure(figsize=(10, 6))

    # 绘制 file1 和 file2 对应的轨迹，交换 x 和 y
    plt.plot(aligned_data['field.y_file1'], aligned_data['field.x_file1'], label='Trajectory from File 1', marker='o',
             linestyle='-', color='b')
    plt.plot(aligned_data['field.y_file2'], aligned_data['field.x_file2'], label='Trajectory from File 2', marker='x',
             linestyle='-', color='r')

    # 图例、标签和标题
    plt.title('Trajectory Plot: Y vs X Coordinates')
    plt.xlabel('Y Coordinate')  # 注意横坐标标签变化
    plt.ylabel('X Coordinate')  # 注意纵坐标标签变化
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

    # 根据UTC_time对齐数据，并打印对齐的UTC_time, x, y
    aligned_data = align_data(file1_data, file2_data)

    # 截取第750到第3000个点的数据
    aligned_data_subset = aligned_data.iloc[0:20000]

    # 计算误差
    error = calculate_error(aligned_data_subset)

    # 输出误差的统计信息
    print(f"Mean Error: {np.mean(error)}")
    print(f"Max Error: {np.max(error)}")
    print(f"Min Error: {np.min(error)}")
    print(f"Median Error: {np.median(error)}")

    # 计算均方根误差 (RMSE)
    rmse = np.sqrt(np.mean(error ** 2))
    print(f"Root Mean Square Error (RMSE): {rmse}")

    # 绘制误差图
    plot_error(error)

    # 绘制轨迹图
    plot_trajectory(aligned_data_subset)


# 输入文件路径
file1_path = 'D:\\personal\\Desktop\\20241130\\gaosi\\n_result.txt'  # 替换为实际文件路径
file2_path = 'D:\\personal\\Desktop\\20241130\\gaosi\\q_result.txt'  # 替换为实际文件路径
# file2_path = 'D:\\personal\\Desktop\\xin\\2\\3q_end.txt'  # 替换为实际文件路径

# 执行主程序
main(file1_path, file2_path)
