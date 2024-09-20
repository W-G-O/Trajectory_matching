import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]  # 设置显示中文字体
mpl.rcParams["axes.unicode_minus"] = False  # 设置正常显示符号

document = "普铁_Identity.xlsx"
data = pd.read_excel(document)
type = document[:2]
uids = list(data["UID"])
roadnames = list(data["name"])
lengths = list(data["length"])
distance_min = 50  # 将长度差值小于50米的道路作为双向道路进行处理
width_bins = 50

sum_length_min = min(lengths)
sum_length_max = max(lengths)
grid_road_length = {}
# 形成{"网格id":{"道路1"：[length1,length2],...,"道路N"：[length1,length2]}}的字典
for i in range(len(uids)):
    uid = uids[i]
    roadname = roadnames[i]
    length = lengths[i]
    if str(uid) not in grid_road_length.keys():
        grid_road_length[str(uid)] = {}
    if roadname not in grid_road_length[str(uid)].keys():
        grid_road_length[str(uid)][roadname] = []
    grid_road_length[str(uid)][roadname].append(length)

# 将同一网格中道路并行的情况进行处理，以平均值进行代替
for uid, road_length in grid_road_length.items():
    for road, length in road_length.items():
        length_diff = []
        length_result = []
        del_index = []
        length = sorted(length)
        for i in range(len(length) - 1):
            length_diff.append(abs(length[i] - length[i + 1]))
        for i in range(len(length_diff)):
            length_diff_min_index = np.int_(np.argmin(length_diff))
            if length_diff[length_diff_min_index] <= distance_min:
                length_result.append((length[length_diff_min_index] + length[length_diff_min_index + 1]) / 2)
                length.remove(length[length_diff_min_index])
                length.remove(length[length_diff_min_index])
                length_diff = []
                for j in range(len(length) - 1):
                    length_diff.append(abs(length[j] - length[j + 1]))
                if len(length_diff) == 0:
                    break
            else:
                break
        length_result.extend(length)
        road_length[road] = length_result

print(grid_road_length)

# 得到每个网格中的道路数量
grid_road_num = []
for grid_road_length_key in grid_road_length.keys():
    grid_road_num.append(len(grid_road_length[grid_road_length_key]))
# 得到每条道路在每个网格中的长度
grid_road_length_result = []
# 得到每个网格中道路的平均长度
grid_road_length_mean = []
for uid, road_length in grid_road_length.items():
    grid_road_length_sum = []
    for road, length in road_length.items():
        grid_road_length_result.append(np.sum(length))
        grid_road_length_sum.append(np.sum(length))
    grid_road_length_mean.append(np.mean(grid_road_length_sum))

# # 高速的话GIS中数据直接是双向道路的长度，所以要除以2。其他交通方式不用这一步
# grid_road_length_result = [item / 2 for item in grid_road_length_result]
# grid_road_length_mean = [item / 2 for item in grid_road_length_mean]

print(grid_road_num)
print(grid_road_length_result)
print(grid_road_length_mean)

# 画图1——得到每个网格中的道路数量
min_grid_road_num = np.min(grid_road_num)
max_grid_road_num = np.max(grid_road_num)
num_bins = max_grid_road_num
statistics_grid_road_num = np.int_(np.zeros(num_bins).tolist())

for i in range(len(grid_road_num)):
    num_index = np.int_(grid_road_num[i])-1
    statistics_grid_road_num[num_index] += 1
print(statistics_grid_road_num)

value = np.int_([i + 1 for i in range(num_bins)])
frequency = statistics_grid_road_num

print(value)
print(frequency)

plt.figure(figsize=(20, 12))
current_axes = plt.axes()
current_axes.xaxis.set_visible(False)  # 隐藏横坐标
plt.bar(value, frequency, width=0.5)
plt.title(type + "——每个网格中的道路数量", fontsize=15)
for i in range(len(value)):
    plt.text(value[i], frequency[i], str(frequency[i]), fontsize=15, horizontalalignment="center",
             verticalalignment="bottom")
    plt.text(value[i], -0.1, str(i+1), fontsize=15,
             horizontalalignment="center", verticalalignment="top")
plt.xlabel("Value(个)", fontsize=15)
plt.ylabel("Frequency", fontsize=15)
plt.savefig(type + "——每个网格中的道路数量.png")

# 画图2——得到每条道路在每个网格中长度的分布
min_grid_road_length_result = np.min(grid_road_length_result)
max_grid_road_length_result = np.max(grid_road_length_result)
num_bins = int(max_grid_road_length_result // width_bins + 1)

statistics_grid_road_length_result = np.int_(np.zeros(num_bins).tolist())

for i in range(len(grid_road_length_result)):
    num_index = np.int_(grid_road_length_result[i] // 50)
    statistics_grid_road_length_result[num_index] += 1
print(statistics_grid_road_length_result)

value = np.int_([i + 1 for i in range(num_bins)])
frequency = statistics_grid_road_length_result

print(value)
print(frequency)

plt.figure(figsize=(20, 12))
current_axes = plt.axes()
current_axes.xaxis.set_visible(False)  # 隐藏横坐标
plt.bar(value, frequency, width=0.5)
plt.title(type + "——每条道路在每个网格中的长度", fontsize=15)
for i in range(len(value)):
    plt.text(value[i], frequency[i], str(frequency[i]), fontsize=10, horizontalalignment="center",
             verticalalignment="bottom")
    plt.text(value[i], 0, str(i * 50) + "≤length≤" + str((i + 1) * 50), fontsize=10, rotation=90,
             horizontalalignment="center", verticalalignment="top")
# plt.text(len(value) / 2, -230, "Value(m)", horizontalalignment="center",fontsize=13)
plt.ylabel("Frequency", fontsize=13)
plt.subplots_adjust(bottom=0.15)
plt.savefig(type + "——每条道路在每个网格中的长度.png")

# 画图3——得到每个网格中道路的平均长度
min_grid_road_length_result = np.min(grid_road_length_mean)
max_grid_road_length_result = np.max(grid_road_length_mean)
num_bins = int(max_grid_road_length_result // width_bins + 1)

statistics_grid_road_length_mean = np.int_(np.zeros(num_bins).tolist())

for i in range(len(grid_road_length_mean)):
    num_index = np.int_(grid_road_length_mean[i] // 50)
    statistics_grid_road_length_mean[num_index] += 1
print(statistics_grid_road_length_mean)

value = np.int_([i + 1 for i in range(num_bins)])
frequency = statistics_grid_road_length_mean

print(value)
print(frequency)

plt.figure(figsize=(20, 12))
current_axes = plt.axes()
current_axes.xaxis.set_visible(False)  # 隐藏横坐标
plt.bar(value, frequency, width=0.5)
plt.title(type + "——每个网格中道路的平均长度", fontsize=15)
for i in range(len(value)):
    plt.text(value[i], frequency[i], str(frequency[i]), fontsize=10, horizontalalignment="center",
             verticalalignment="bottom")
    plt.text(value[i], 0, str(i * 50) + "≤length≤" + str((i + 1) * 50), fontsize=10, rotation=90,
             horizontalalignment="center", verticalalignment="top")
# plt.text(len(value) / 2, -210, "Value(m)", horizontalalignment="center",fontsize=13)
plt.ylabel("Frequency", fontsize=13)
plt.subplots_adjust(bottom=0.15)
plt.savefig(type + "——每个网格中道路的平均长度.png")
