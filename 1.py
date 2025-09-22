import pandas as pd
pd.set_option('display.float_format', '{:.4f}'.format)
# 假设文件名为 data.csv
file2_path = 'D:/personal/Desktop/2/2ins_end.txt'

# 读取 CSV 文件
columns = ['UTC_time', 'corrected_latitude', 'corrected_longitude', 'field.fheading', 'field.x', 'field.y']
data = pd.read_csv(file2_path, delimiter=',', encoding='utf-8', names=columns)# 查看数据前几行
print(data.head())