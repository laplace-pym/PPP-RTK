import datetime
import re

def gps_to_utc(gps_week_milliseconds, gps_week_number):
    """
    Convert GPS time (week number and milliseconds) to UTC datetime.
    GPS time starts on 1980-01-06, and it's not leap second aware.
    """
    gps_epoch = datetime.datetime(1980, 1, 6)  # GPS epoch start date
    milliseconds_in_week = 7 * 24 * 3600 * 1000  # Number of milliseconds in a week

    # Calculate total number of milliseconds since GPS epoch
    total_milliseconds = gps_week_number * milliseconds_in_week + gps_week_milliseconds

    # Convert total milliseconds to total seconds
    total_seconds = total_milliseconds / 1000.0

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
        # 使用正则按空格/制表符分隔读取表头
        header = re.split(r'\s+', infile.readline().strip())

        # 找到 gps_week_milliseconds 和 gps_week_number 列的索引
        gps_milliseconds_index = header.index("gps_week_milliseconds")
        gps_week_number_index = header.index("gps_week_number")

        # 写入输出文件的表头，并在最后添加 'UTC_time' 列
        outfile.write(",".join(header) + ",UTC_time\n")

        # 处理每一行数据
        for line in infile:
            # 用正则分隔每列数据（支持多个空格/制表符）
            columns = re.split(r'\s+', line.strip())

            try:
                gps_milliseconds = float(columns[gps_milliseconds_index])
                gps_week_number = int(columns[gps_week_number_index])
                utc_time = gps_to_utc(gps_milliseconds, gps_week_number)
                columns.append(str(utc_time))
            except ValueError as e:
                print(f"Error converting values on line: {line.strip()}")
                print(f"Reason: {e}")

            outfile.write(",".join(columns) + "\n")


# 指定输入和输出文件路径
input_file = "D:\\personal\\Desktop\\gps_week_output.txt"
output_file = "D:\\personal\\Desktop\\gnss_utc.txt"

# 处理文件
process_file(input_file, output_file)

print("Processing complete. The converted data has been saved to", output_file)
