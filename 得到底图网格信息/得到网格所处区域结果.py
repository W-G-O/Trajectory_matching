import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import pickle

mpl.rcParams["font.sans-serif"] = ["SimHei"]  # 设置显示中文字体
mpl.rcParams["axes.unicode_minus"] = False  # 设置正常显示符号

document = "D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\输出结果\网格所处地区结果.xlsx"
data = pd.read_excel(document)
uids = list(data["网格id"])
area_ids = list(data["区域id"])
district_ids = list(data["区名"])
city_ids = list(data["市名"])
province_ids = list(data["省名"])
num_row = 326
num_col = 364

""""形成形如{"网格id(列,行)"：区域id}的储存结构"""

# 步骤1：先将所有网格的交通方式进行存储, 形成{网格id1：区域1,网格id2：区域2}的结构
grid_area = {}
for i in range(len(uids)):
    # 对有交通方式的进行储存
    grid_id = uids[i]
    grid_id_col = int((grid_id - 1) % num_col)
    grid_id_row = int((grid_id - 1) // num_col)
    grid_area[(grid_id_col, grid_id_row)] = area_ids[i]
print(grid_area)

# 将结果保存
with open('D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\输出结果/GridAreaRes.pkl', 'wb') as file:
    pickle.dump(grid_area, file)
