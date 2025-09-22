import matplotlib.pyplot as plt
import numpy as np


def read_file(file_path):
    """
    从文件中读取数据，返回包含字段和数据的字典
    """
    data = {'UTC_time': [], 'field.msvs': []}

    with open(file_path, 'r') as f:
        header = f.readline().strip().split(',')  # 获取标题行
        # 打印标题行，检查列头
        print(f"File header: {header}")

        # 获取对应列的索引
        utc_time_index = header.index('UTC_time')
        msvs_index = header.index('field.msvs')

        # 遍历文件中的数据行
        for line in f:
            columns = line.strip().split(',')
            if len(columns) < len(header):
                continue  # 如果行数据不足，跳过

            utc_time = columns[utc_time_index].strip()
            field_msvs = columns[msvs_index].strip()

            # 尝试将field.msvs转换为int（卫星数量是整数）
            try:
                field_msvs_value = int(field_msvs)
            except ValueError:
                continue  # 如果无法转换为整数，跳过该行

            data['UTC_time'].append(utc_time)
            data['field.msvs'].append(field_msvs_value)

    return data


def align_data(data1, data2):
    """
    对齐两个数据集（data1和data2），根据UTC_time进行时间比对
    """
    aligned_msvs = []
    aligned_utc = []

    # 假设我们要容忍时间戳的微小差异
    for t1, msvs1 in zip(data1['UTC_time'], data1['field.msvs']):
        closest_time = None
        closest_msvs = None

        # 寻找第二组数据中与第一组时间接近的时间戳
        for t2, msvs2 in zip(data2['UTC_time'], data2['field.msvs']):
            time_diff = abs(float(t1) - float(t2))  # 计算时间差
            if time_diff < 0.1:  # 容忍时间戳微小差异
                closest_time = t2
                closest_msvs = msvs2
                break

        if closest_time:
            aligned_msvs.append(closest_msvs)
            aligned_utc.append(t1)

    return aligned_utc, aligned_msvs


def plot_data(utc_time, msvs_values):
    """
    绘制图像，横坐标为对齐的点的个数，纵坐标为field.msvs值
    """
    if len(utc_time) == 0 or len(msvs_values) == 0:
        print("Warning: No data to plot!")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(utc_time)), msvs_values, marker='o', linestyle='-', color='b')
    plt.title("Aligned Data Plot")
    plt.xlabel("Aligned Points")
    plt.ylabel("Number of Satellites (field.msvs)")
    plt.grid(True)
    plt.show()


def main():
    # 读取两个文件的数据
    file1 = "D:\\personal\\Desktop\\20241130\\e\\1n_result.txt"  # 替换成你实际的文件路径
    file2 = "D:\\personal\\Desktop\\20241130\\e\\1q_result.txt"  # 替换成你实际的文件路径
    data1 = read_file(file1)
    data2 = read_file(file2)

    # 对齐数据
    utc_time, msvs_values = align_data(data1, data2)

    # 绘制图像
    plot_data(utc_time, msvs_values)


if __name__ == "__main__":
    main()
