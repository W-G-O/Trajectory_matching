import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import pickle

mpl.rcParams["font.sans-serif"] = ["SimHei"]  # 设置显示中文字体
mpl.rcParams["axes.unicode_minus"] = False  # 设置正常显示符号

with open('D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\输出结果/GridModesAdjacentRes.pkl', 'rb') as files:
    grid_modes_adjacent = pickle.load(files)

""""形成形如{"网格id(列,行)"：[1,2,3,4,5,6,7,8,9]}的储存结构"""

mode_x_y_s = {"县道": [[], []], "普铁": [[], []], "省道": [[], []], "高速收费站": [[], []], "高速": [[], []],
              "国道": [[], []], "高铁": [[], []], "火车站": [[], []]}

for x_y in grid_modes_adjacent.keys():
    self_modes_num_10 = grid_modes_adjacent[x_y][4]
    self_modes = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(self_modes)):
        if self_modes_num_10 - 2 ** (len(self_modes) - 1 - i) >= 0:
            self_modes[i] = 1
            self_modes_num_10 = self_modes_num_10 - 2 ** (len(self_modes) - 1 - i)
    if self_modes[0] == 1:
        mode_x_y_s["县道"][0].append(x_y[0])
        mode_x_y_s["县道"][1].append(x_y[1])
    if self_modes[1] == 1:
        mode_x_y_s["普铁"][0].append(x_y[0])
        mode_x_y_s["普铁"][1].append(x_y[1])
    if self_modes[2] == 1:
        mode_x_y_s["省道"][0].append(x_y[0])
        mode_x_y_s["省道"][1].append(x_y[1])
    if self_modes[3] == 1:
        mode_x_y_s["高速收费站"][0].append(x_y[0])
        mode_x_y_s["高速收费站"][1].append(x_y[1])
    if self_modes[4] == 1:
        mode_x_y_s["高速"][0].append(x_y[0])
        mode_x_y_s["高速"][1].append(x_y[1])
    if self_modes[5] == 1:
        mode_x_y_s["国道"][0].append(x_y[0])
        mode_x_y_s["国道"][1].append(x_y[1])
    if self_modes[6] == 1:
        mode_x_y_s["高铁"][0].append(x_y[0])
        mode_x_y_s["高铁"][1].append(x_y[1])
    if self_modes[7] == 1:
        mode_x_y_s["火车站"][0].append(x_y[0])
        mode_x_y_s["火车站"][1].append(x_y[1])
# 将四种交通方式的轨迹图以子图的形式画出来
fig, axs = plt.subplots(2, 4)
#将画布的大小设置为20*10
fig.set_size_inches(20, 8)

fig.suptitle("八种方式的轨迹图")
axs[0, 0].scatter(mode_x_y_s["县道"][0], mode_x_y_s["县道"][1], c="red", s=1)
axs[0, 0].set_title("县道")
axs[0, 1].scatter(mode_x_y_s["普铁"][0], mode_x_y_s["普铁"][1], c="blue", s=1)
axs[0, 1].set_title("普铁")
axs[0, 2].scatter(mode_x_y_s["省道"][0], mode_x_y_s["省道"][1], c="green", s=1)
axs[0, 2].set_title("省道")
axs[0, 3].scatter(mode_x_y_s["高速收费站"][0], mode_x_y_s["高速收费站"][1], c="black", s=1)
axs[0, 3].set_title("高速收费站")
axs[1, 0].scatter(mode_x_y_s["高速"][0], mode_x_y_s["高速"][1], c="purple", s=1)
axs[1, 0].set_title("高速")
axs[1, 1].scatter(mode_x_y_s["国道"][0], mode_x_y_s["国道"][1], c="black", s=1)
axs[1, 1].set_title("国道")
axs[1, 2].scatter(mode_x_y_s["高铁"][0], mode_x_y_s["高铁"][1], c="orange", s=1)
axs[1, 2].set_title("高铁")
axs[1, 3].scatter(mode_x_y_s["火车站"][0], mode_x_y_s["火车站"][1], c="brown", s=1)
axs[1, 3].set_title("火车站")
plt.show()


