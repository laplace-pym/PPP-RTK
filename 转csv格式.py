import yaml

def convert_to_format2(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.read().split('---\n')  # 以 --- 分割每一条记录

    # 打开输出文件用于写入
    with open(output_file, 'w') as txtfile:
        # 写入文件的头部
        txtfile.write("gps_week_milliseconds,longitude,latitude\n")

        for record in data:
            try:
                # 解析 YAML 格式的记录
                record_data = yaml.safe_load(record.strip())

                # 检查解析结果
                if record_data is None:
                    print("Warning: Encountered a NoneType record, skipping.")
                    continue  # 跳过这条记录

                # 提取 gps_week_milliseconds、longitude 和 latitude
                gps_week_milliseconds = record_data.get('gps_week_milliseconds')
                latitude = record_data.get('latitude')
                longitude = record_data.get('longitude')

                # 确保字段存在且有效
                if gps_week_milliseconds is None or latitude is None or longitude is None:
                    print(f"Warning: Missing data in record: {record}")
                    continue  # 跳过缺少必要字段的记录

                # 写入数据
                line = f"{gps_week_milliseconds},{longitude},{latitude}\n"
                txtfile.write(line)

            except Exception as e:
                print(f"Error processing record: {e}")

# 示例：调用函数
input_file = "D:\\personal\\Desktop\\1229\\m1.txt"  # 输入文件名
output_file = "D:\\personal\\Desktop\\1229\\rm1.txt"  # 输出文件名
convert_to_format2(input_file, output_file)
