import numpy as np
import pandas as pd
import pickle


def Generating_trajectories(data, grid_row, grid_col):
    roads = []
    id = data["网格id"]
    # Join_Count = data["Join_Count"]
    roadname = data["roadname"]
    roadspeed = data["roadspeed"]

    examples = []
    for i in range(len(roadname)):
        if type(roadname[i]) is str and (roadname[i] not in examples):
            examples.append(roadname[i])

    for i in range(len(examples)):
        # 导入道路id及名字
        road = {"id": i, "roadname": examples[i]}
        # 获得道路索引
        index = list(np.where(roadname == examples[i])[0])
        # 导入道路速度
        road["speed"] = float(roadspeed[index[0]])
        # 导入道路经过的网格
        grid = list(id[index])
        # 对道路经过的网格依次排序
        grid = Sort_grid(grid, grid_row, grid_col)
        # 形成有序网格
        grid_name = []
        for j in range(len(grid)):
            num = int(grid[j])
            # 从0开始计行数/列数
            row = num // grid_col + 1
            col = num % grid_col
            grid_name.append((row, col))
        road["route"] = grid_name
        # 将途径小于5个网格的道路筛掉,将途径大于等于5个网格的道路以字典的形式形成集合
        if len(index) >= 5:
            roads.append(road)
    return roads


def Sort_grid(init_grid, grid_row, grid_col):
    """有缺陷：无法处理道路中有断点及道路分叉情况"""
    ordered_grid = []
    num_grid = len(init_grid)
    # 找到轨迹起点origin
    origin = init_grid[0]
    for grid_index in range(num_grid):
        grid0 = int(init_grid[grid_index])
        around = [grid0 + 1, grid0 + grid_col - 1, grid0 + grid_col, grid0 + grid_col + 1,
                  grid0 - 1, grid0 - grid_col - 1, grid0 - grid_col, grid0 - grid_col + 1]
        intersections = list(set(around) & set(init_grid))
        if len(intersections) <= 1:
            origin = grid0
            break
        elif len(intersections) == 2:
            if (intersections[0] - intersections[1]) == 1 or (intersections[0] - intersections[1]) == grid_col:
                origin = grid0
                break
        elif len(intersections) == 3:
            # 周围3个网格为：四个角及其相邻网格
            sum1 = (grid0 - 1) + (grid0 - 1 + grid_col) + (grid0 + grid_col)
            sum2 = (grid0 + 1) + (grid0 + 1 + grid_col) + (grid0 + grid_col)
            sum3 = (grid0 - 1) + (grid0 - 1 - grid_col) + (grid0 - grid_col)
            sum4 = (grid0 + 1) + (grid0 + 1 - grid_col) + (grid0 - grid_col)
            if sum(intersections) == sum1 or sum(intersections) == sum2 or sum(
                    intersections) == sum3 or sum(intersections) == sum4:
                origin = grid0
                break
    ordered_grid.append(origin)
    init_grid.remove(origin)

    # 通过搜索周围点进行排序
    for number_searches in range(num_grid - 1):
        origin_around = [origin + 1, origin + grid_col - 1, origin + grid_col, origin + grid_col + 1,
                         origin - 1, origin - grid_col - 1, origin - grid_col, origin - grid_col + 1]
        origin_intersections = list(set(origin_around) & set(init_grid))
        # 对断点情况进行处理
        if len(origin_intersections) == 0:
            if len(init_grid) > 0:
                distance = []
                for i in range(len(init_grid)):
                    distance.append(((init_grid[i] // grid_col) - (origin // grid_col)) ** 2 + (
                            (init_grid[i] % grid_col) - (origin % grid_col)) ** 2)
                distance_min_index = np.argmin(distance)
                distance_min = init_grid[distance_min_index]
                ordered_grid.append(distance_min)
                init_grid.remove(distance_min)
                origin = distance_min
        elif len(origin_intersections) == 1:
            ordered_grid.append(origin_intersections[0])
            init_grid.remove(origin_intersections[0])
            origin = origin_intersections[0]
        elif len(origin_intersections) == 2:
            origin_intersections_num0 = origin_intersections[0]
            origin_around04 = [origin + 1, origin + grid_col,
                               origin - 1, origin - grid_col]
            if origin_intersections_num0 in origin_around04:
                ordered_grid.append(origin_intersections[0])
                init_grid.remove(origin_intersections[0])
                origin = origin_intersections[0]
            else:
                ordered_grid.append(origin_intersections[1])
                init_grid.remove(origin_intersections[1])
                origin = origin_intersections[1]
        elif len(origin_intersections) == 3:
            origin_around4 = [origin + 1, origin + grid_col,
                              origin - 1, origin - grid_col]
            origin_around2 = list(set(init_grid) & set(origin_around4))
            around1 = origin_around2[0]
            around1_around8 = [around1 + 1, around1 + grid_col - 1, around1 + grid_col, around1 + grid_col + 1,
                               around1 - 1, around1 - grid_col - 1, around1 - grid_col, around1 - grid_col + 1]
            if len(list(set(around1_around8) & set(init_grid))) <= 2:
                ordered_grid.append(origin_around2[0])
                init_grid.remove(origin_around2[0])
                origin = origin_around2[0]
            else:
                # 此处有问题，无法解决道路的交叉情况！
                if len(origin_around2) > 1:
                    ordered_grid.append(origin_around2[1])
                    init_grid.remove(origin_around2[1])
                    origin = origin_around2[1]

    return ordered_grid


data = pd.read_excel("D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\排序数据样例\高速示例文件（326行 364列）.xlsx")
grid_row = 326
grid_col = 364
expressways = Generating_trajectories(data, grid_row, grid_col)
print(expressways)

# 将结果保存
with open('D:\课题组\轨迹匹配\地图数据\江南区域_1000×1000\排序数据样例/OrderedRoadRes.pkl', 'wb') as file:
    pickle.dump(expressways, file)
