import pandas as pd
import matplotlib.pyplot as plt

# 读取txt文件，假设文件是逗号分隔的
df = pd.read_csv('D://personal//Desktop//2//q_dx1_end.txt', delimiter=',')

# 提取 'field.pos_qual' 和 'field.heading_qual' 列
if 'pos_qual' in df.columns :
    pos_qual = df['pos_qual'][:63000000]  # 只取前630个点
    # heading_qual = df['field.heading_qual'][:6300000000]  # 只取前630个点

    # 创建横轴1, 2, 3, ..., 630
    x = range(1, 6310000000)

    # 创建第一张图：field.pos_qual
    plt.figure(figsize=(10, 6))
    plt.plot(x, pos_qual, label='pos_qual', marker='o')
    plt.title('pos_qual')
    plt.xlabel('Index')
    plt.ylabel('Quality Value')
    plt.legend()
    plt.show()

    # # 创建第二张图：field.heading_qual
    # plt.figure(figsize=(10, 6))
    # plt.plot(x, heading_qual, label='field.heading_qual', marker='x')
    # plt.title('field.heading_qual')
    # plt.xlabel('Index')
    # plt.ylabel('Quality Value')
    # plt.legend()
    # plt.show()

# else:
#     print("文件中没有找到相关列：'field.pos_qual' 或 'field.heading_qual'")
