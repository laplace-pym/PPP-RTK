import pandas as pd

# 读取txt文件
txt_file = 'D:\\personal\\Desktop\\qq33.txt'  # 替换为你的txt文件路径
data = pd.read_csv(txt_file)

# 创建一个新的DataFrame，添加其他需要的列
data['LineStringColor'] = 'red'
data['Icon'] = ''
data['LineStringWidth'] = 10

# 选择需要的列，并重命名为Excel中所需的格式
data = data.rename(columns={
    'field.latitude': 'Latitude',
    'field.lontitude': 'Longitude'
})

# 保存为Excel文件
excel_file = 'D:\\personal\\Desktop\\qq33.xlsx'  # 输出的Excel文件名
data.to_excel(excel_file, index=False)

print(f"数据已成功保存为 {excel_file}")
