def extract_gps_to_tum(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    current_data = {}

    for line in lines:
        line = line.strip()
        if line.startswith("gps_week_number:"):
            current_data["gps_week_number"] = int(line.split(":")[1].strip())
        elif line.startswith("gps_week_milliseconds:"):
            current_data["gps_week_milliseconds"] = int(line.split(":")[1].strip())
        elif line.startswith("longitude:"):
            current_data["longitude"] = float(line.split(":")[1].strip())
        elif line.startswith("latitude:"):
            current_data["latitude"] = float(line.split(":")[1].strip())
        elif line.startswith("height:"):
            current_data["height"] = float(line.split(":")[1].strip())

        # 收集完一组就写入
        if all(k in current_data for k in ["gps_week_number", "gps_week_milliseconds", "longitude", "latitude", "height"]):
            result_line = f"{current_data['gps_week_number']} {current_data['gps_week_milliseconds']} {current_data['longitude']} {current_data['latitude']} {current_data['height']}"
            results.append(result_line)
            current_data = {}

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# gps_week_number gps_week_milliseconds longitude latitude height\n")
        for line in results:
            f.write(line + "\n")

    print(f"提取完成，输出文件已保存为：{output_file}")


# 输入输出路径（你桌面的路径）
input_path = r"D:\personal\Desktop\output.txt"
output_path = r"D:\personal\Desktop\gps_week_output.txt"

extract_gps_to_tum(input_path, output_path)
