import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import pickle

mpl.rcParams["font.sans-serif"] = ["SimHei"]  # 设置显示中文字体
mpl.rcParams["axes.unicode_minus"] = False  # 设置正常显示符号

document = "D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\输出结果\网格数据结果.xlsx"
data = pd.read_excel(document)
uids = list(data["网格id"])
judge1_expressway = list(data["whe_高速"])
judge2_national_highway = list(data["whe_国道"])
judge3_provincial_highway = list(data["whe_省道"])
judge4_general_railway = list(data["whe_普铁"])
judge5_highspeed_railway = list(data["whe_高铁"])
judge6_railway_station = list(data["whe_火车站"])
judge7_passenger_transport_buffer = list(data["whe_客运缓冲站"])
judge8_highway_toll_station = list(data["whe_高速收费站"])
judge9_county_highway = list(data["whe_县道"])
number_adjacent_cells = 8
num_row = 326
num_col = 364

""""形成形如{"网格id(列,行)"：[1,2,3,4,5,6,7,8,9]}的储存结构"""

# 步骤1：先将所有网格的交通方式进行存储, 形成{网格id1：num1,网格id2：num2}的结构
grid_self_modes = {}
for i in range(len(uids)):
    judge_any_mode = [judge9_county_highway[i], judge4_general_railway[i], judge3_provincial_highway[i],
                      judge8_highway_toll_station[i], judge1_expressway[i], judge2_national_highway[i],
                      judge5_highspeed_railway[i], judge6_railway_station[i]]
    # 先判断有没有某一种交通方式
    sum_judge_any_mode = sum(judge_any_mode)
    if sum_judge_any_mode == 0:
        continue
    else:
        # 对有交通方式的进行储存
        grid_self_modes[uids[i]] = 0
        for j in range(len(judge_any_mode)):
            grid_self_modes[uids[i]] += judge_any_mode[j] * 2 ** (len(judge_any_mode) - 1 - j)
# print(grid_self_modes)

# 步骤2：进行搜索得到相邻8个格子的信息形成结果
grid_modes_adjacent = {}
grid_ids = list(grid_self_modes.keys())
for i in range(len(grid_ids)):
    grid_id = grid_ids[i]
    adjacent_grid_ids = [grid_id + num_col - 1, grid_id + num_col, grid_id + num_col + 1, grid_id - 1, grid_id,
                         grid_id + 1, grid_id - num_col - 1, grid_id - num_col, grid_id - num_col + 1]
    grid_id_col = int((grid_id - 1) % num_col)
    grid_id_row = int((grid_id - 1) // num_col)
    grid_modes_adjacent[(grid_id_col, grid_id_row)] = []
    for j in range(len(adjacent_grid_ids)):
        if adjacent_grid_ids[j] not in grid_ids:
            grid_modes_adjacent[(grid_id_col, grid_id_row)].append(0)
        else:
            grid_modes_adjacent[(grid_id_col, grid_id_row)].append(grid_self_modes[adjacent_grid_ids[j]])
print(grid_modes_adjacent)

# 将结果保存
with open('D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\输出结果/GridModesAdjacentRes.pkl', 'wb') as file:
    pickle.dump(grid_modes_adjacent, file)
