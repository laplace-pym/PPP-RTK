import pandas as pd
from datetime import datetime, timedelta

# 文件路径
file2_path = 'D:\\personal\\Desktop\\new\\3bei_end.txt'  # 第二个文件路径
output_path = 'D:\\personal\\Desktop\\new\\3b_end.txt'  # 输出文件路径

# 读取文件2 (假设文件2是CSV格式)
df2 = pd.read_csv(file2_path)

# 假设文件2中的field.b是时间格式（例如：09:29:41.0005）

# 设置一个基准时间，用于将field.b转换为UTC_time格式
base_date = '20241213'  # 假设我们用2024年12月13日作为基准日期

# 将文件2的时间（field.b）转换为与文件1相同的UTC_time格式
def convert_to_utc_time(field_b, base_date):
    time_obj = datetime.strptime(field_b, "%H:%M:%S.%f")
    base_time_obj = datetime.strptime(base_date + "000000.000", "%Y%m%d%H%M%S.%f")
    new_utc_time = base_time_obj + timedelta(hours=time_obj.hour, minutes=time_obj.minute,
                                               seconds=time_obj.second, microseconds=int(time_obj.microsecond))
    return new_utc_time.strftime("%Y%m%d%H%M%S.%f")[:-3]  # 去掉最后3位微秒，保留到毫秒

# 创建一个新的列，表示转换后的UTC_time
df2['UTC_time'] = df2['field.b'].apply(lambda x: convert_to_utc_time(x, base_date))

# 选择输出所需的列
output_df = df2[['UTC_time', 'corrected_latitude', 'corrected_longitude', 'field.x', 'field.y']]

# 输出结果到新的txt文件
output_df.to_csv(output_path, index=False, header=True, sep=',', float_format='%.6f')

print(f"转换并保存的数据已输出到: {output_path}")
