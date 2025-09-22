import datetime

def gps_to_utc(milliseconds):
    """
    Convert GPS time (in milliseconds) to UTC datetime.
    GPS time starts on 1980-01-06, and it's not leap second aware.
    The GPS week number is fixed to 2345.
    """
    gps_epoch = datetime.datetime(1980, 1, 6)  # GPS epoch start date
    seconds_in_week = 7 * 24 * 3600  # Number of seconds in a week
    milliseconds_in_second = 1000  # Number of milliseconds in one second

    # Fixed GPS week number
    gps_week_num = 2345

    # Convert milliseconds to seconds
    gps_seconds = milliseconds / milliseconds_in_second

    # Calculate total number of seconds since GPS epoch
    total_seconds = gps_week_num * seconds_in_week + gps_seconds

    # Calculate UTC datetime from total seconds
    utc_time = gps_epoch + datetime.timedelta(seconds=total_seconds)

    # Subtract 18 seconds from UTC time (to adjust for leap seconds)
    utc_time -= datetime.timedelta(seconds=18)

    # Format UTC time to match the desired format (YYYYMMDDHHMMSS.SS)
    formatted_utc_time = utc_time.strftime("%Y%m%d%H%M%S")

    # Handle the microseconds to ensure it has two digits after the decimal point
    microsecond_fraction = int((utc_time.microsecond) / 10000)  # Get microseconds in 0.01 format
    formatted_utc_time += f".{str(microsecond_fraction).zfill(2)}"  # Ensure two digits after the decimal

    return formatted_utc_time


def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 读取表头（第一行）以获取列名
        header = infile.readline().strip().split(',')

        # 写入输出文件的表头，并在最后添加 'UTC_time' 列
        outfile.write(",".join(header) + ",UTC_time\n")

        # 处理后续的每一行
        for line in infile:
            columns = line.strip().split(',')

            # 找到 gps_seconds 列的索引（此处假设是 'field.nov_header.gps_week_milliseconds'）
            if "field.nov_header.gps_week_milliseconds" in header:
                gps_milliseconds_index = header.index("field.nov_header.gps_week_milliseconds")

                try:
                    # 提取 gps_milliseconds 字段的值（以毫秒为单位）
                    gps_milliseconds = float(columns[gps_milliseconds_index])

                    # 将 gps_milliseconds 转换为 UTC 时间
                    utc_time = gps_to_utc(gps_milliseconds)

                    # 在列末尾添加 UTC 时间
                    columns.append(str(utc_time))
                except ValueError as e:
                    # 如果转换失败，输出错误信息
                    print(f"Error converting values on line: {line.strip()}")

            # 写入修改后的行到输出文件
            outfile.write(",".join(columns) + "\n")


# 指定输入和输出文件路径
input_file = "D:\\personal\\Desktop\\12.18\\ms_1.txt"
output_file = "D:\\personal\\Desktop\\12.18\\ms_utc.txt"

# 处理文件
process_file(input_file, output_file)

print("Processing complete. The converted data has been saved to", output_file)
