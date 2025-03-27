import os
import pandas as pd
from sqlalchemy import create_engine
# 设置目录路径
dir = r"C:\Users\a122861569\Desktop\123"
data_list = []

# 遍历目录中的每个 CSV 文件
for path in os.listdir(dir):
    path = os.path.join(dir, path)
    if path.endswith('.csv'):
        data = pd.read_csv(path)
        data = data[
            ['user_id', 'register_time', 'pvp_battle_count', 'pvp_lanch_count', 'pvp_win_count', 'pve_battle_count',
             'pve_lanch_count', 'pve_win_count', 'avg_online_minutes', 'pay_price', 'pay_count']
        ]
        data_list.append(data)

# 合并所有数据
data = pd.concat(data_list, ignore_index=True)
data.reset_index(drop=True, inplace=True)
output_file = os.path.join(dir, 'cleaned_data.csv')
# 将清洗后的数据导出到 CSV 文件
data.to_csv(output_file, index=False)