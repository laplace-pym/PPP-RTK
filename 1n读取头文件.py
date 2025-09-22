import csv

# 定义需要提取的字段
fields_to_extract = [
#     "field.nov_header.gps_week_number",
# "field.nov_header.gps_week_milliseconds",
# "field.longitude",
# "field.latitude",
"field.data1",
"field.data2",
"field.data3",
    # "field.altitude",
    # "field.azimuth",
    # "field.novatel_msg_header.gps_week_num",
    # "field.novatel_msg_header.gps_seconds",
    # "UTC_time",
    # "field.x",
    # "field.y",
]

def clean_file(input_file):
    with open(input_file, 'rb') as f:
        content = f.read()
    # 删除 NULL 字节
    content = content.replace(b'\x00', b'')
    # 将清理后的内容写入新文件
    with open(input_file, 'wb') as f:
        f.write(content)


def extract_columns(input_file, output_file, fields):
    # 打开输入文件并读取内容
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # 选择需要的字段
        selected_rows = []
        for row in reader:
            selected_row = {field: row[field] for field in fields if field in row}
            selected_rows.append(selected_row)

        # 将选择的列写入输出文件
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            # 写入标题
            writer = csv.DictWriter(outfile, fieldnames=fields)
            writer.writeheader()
            # 写入数据
            writer.writerows(selected_rows)


# 输入文件路径和输出文件路径
input_file = 'D:\\personal\\Desktop\\shuju\\ksxt3.txt'
output_file = 'D:\\personal\\Desktop\\shuju\\a_ksxt3.txt'
# 清理文件中的 NULL 字节

clean_file(input_file)
# 执行提取操作
extract_columns(input_file, output_file, fields_to_extract)

print(f"数据已从 {input_file} 提取并保存到 {output_file}.")



