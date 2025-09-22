import csv


# 读取文件并修改 UTC_time
def modify_utc_time(input_filename, output_filename):
    with open(input_filename, mode='r') as infile, open(output_filename, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 处理每一行
        for row in reader:
            if row:  # 忽略空行
                utc_time_str = row[0]  # 假设UTC_time在第一列
                if len(utc_time_str) > 10:  # 确保是符合 UTC_time 格式的字符串
                    # 提取秒数和小数部分
                    utc_time_parts = utc_time_str.split('.')
                    utc_time_base = utc_time_parts[0]
                    utc_time_seconds = int(utc_time_base[-2:])  # 获取秒数

                    # 增加18秒
                    new_seconds = utc_time_seconds + 18
                    if new_seconds >= 60:
                        # 处理秒数溢出到分钟
                        new_seconds -= 60
                        new_minutes = int(utc_time_base[-4:-2]) + 1
                        utc_time_base = utc_time_base[:-4] + f'{new_minutes:02d}' + f'{new_seconds:02d}'
                    else:
                        utc_time_base = utc_time_base[:-2] + f'{new_seconds:02d}'

                    # 重新组合成新的 UTC_time
                    new_utc_time = utc_time_base + '.' + utc_time_parts[1] if len(utc_time_parts) > 1 else ''
                    row[0] = new_utc_time  # 更新 UTC_time 列

                writer.writerow(row)


# 使用函数修改 UTC_time
input_filename = 'D:\\personal\\Desktop\\2\\3ins_end.txt'  # 输入文件
output_filename = 'D:\\personal\\Desktop\\2\\3i_end.txt'  # 输出文件

modify_utc_time(input_filename, output_filename)
