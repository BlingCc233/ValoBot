import csv

# 读取 CSV 文件
csv_file_path = '/Bot/Assets/database.csv'
data_dict = {}

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        key = int(row[0])  # 第一列作为键，转换为整数
        value = {
            'english': row[1],  # 英文内容
            'chinese': row[2]   # 中文内容
        }
        data_dict[key] = value

# 将字典数据写入 database.py 文件
py_file_path = '/Bot/Assets/database.py'

with open(py_file_path, mode='w', encoding='utf-8') as file:
    file.write('database = {\n')
    for key, value in data_dict.items():
        file.write(f"    {key}: {{'english': '{value['english']}', 'chinese': '{value['chinese']}'}},\n")
    file.write('}\n')

print(f"Data has been written to {py_file_path}")
