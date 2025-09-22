import csv
import yaml

# 读取txt文件并将其按"---"分割
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data.split('---\n')

# 解析每个数据块为字典
def parse_block(block):
    block = block.strip()
    # 使用yaml.safe_load来解析YAML格式的数据
    try:
        return yaml.safe_load(block)
    except yaml.YAMLError as e:
        print(f"Error parsing block: {e}")
        return {}

# 提取需要的字段
def extract_data(block):
    data = {}

    # 提取需要的字段
    data['longitude'] = block.get('longitude', '')
    data['latitude'] = block.get('latitude', '')
    data['height'] = block.get('height', '')
    data['fheading'] = block.get('fheading', '')
    data['pitch'] = block.get('pitch', '')
    data['roll'] = block.get('roll', '')
    data['pos_qual'] = block.get('pos_qual', '')
    data['heading_qual'] = block.get('heading_qual', '')
    data['msvs'] = block.get('msvs', '')
    data['eastvel'] = block.get('eastvel', '')
    data['northvel'] = block.get('northvel', '')
    data['upvel'] = block.get('upvel', '')
    data['time'] = block.get('time', '')  # 提取time字段

    return data

# 将数据写入 CSV 文件
def write_to_csv(data, output_file):
    # 提取所有字段作为header
    headers = data[0].keys()

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def main(input_file, output_file):
    raw_data = read_data(input_file)
    all_data = []

    # 逐个处理每个数据块
    for block in raw_data:
        parsed_block = parse_block(block)
        if parsed_block:
            extracted_data = extract_data(parsed_block)
            all_data.append(extracted_data)

    # 写入CSV文件
    write_to_csv(all_data, output_file)
    print(f"Data successfully written to {output_file}")

# 运行程序
if __name__ == "__main__":
    input_file = 'D:\\personal\\Desktop\\1229\\q2.txt'  # 输入的txt文件路径
    output_file = 'D:\\personal\\Desktop\\1229\\rq2.txt'  # 输出的csv文件路径
    main(input_file, output_file)
