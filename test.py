import math
import random

def index_of(a, list):
    '''
    在给定的列表中查找指定元素的索引
    :param a: 要查找的元素
    :param list: 要查找的列表
    :return: 元素a在list中的索引
    '''
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


# Function to sort by values
def sort_by_values(list1, values):
    '''
    根据给定的值列表对另一个列表进行排序，并返回排好序后的索引列表.
    :param list1: 要排序的列表（存储的是values索引值），这里后续会输入front二维列表第二层的列表
    :param values: 用于排序的值列表
    :return: 排序后的列表，返回的是索引？？？
    '''
    sorted_list = []
    while len(sorted_list) != len(list1):
        if index_of(min(values), values) in list1:  # 判断values中最小值的索引是否为list1中的元素（？？？为毛？？？这样会陷入死循环吧？）
            sorted_list.append(index_of(min(values), values))  # 这里插入的直接就是list1列表根据values列表排序规则排序后的索引？？
        values[index_of(min(values), values)] = math.inf
        # 这个函数会陷入死循环，所以我加了个if语句，当value全为inf时直接break
        if set(values) == {math.inf}:
            break
    return sorted_list


# Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort(values1, values2):
    '''
    :param values1: 多目标优化问题中每个解在第一个目标函数下的取值，如[5, 2, 9, 3, 7, 4]
    :param values2: 多目标优化问题中每个解在第二个目标函数下的取值，如[6, 4, 8, 2, 5, 3]
    :return: 二维列表 front，其中包含 Pareto 前沿中每层非支配解的索引，如[[2], [0, 4], [1, 5], [3]]
    '''
    # 初始化 S, front, n 和 rank 列表
    S = [[] for _ in range(0, len(values1))]  # 记录每个解的被支配解集合
    front = [[]]  # 记录 Pareto 前沿层级
    n = [0 for _ in range(0, len(values1))]  # 记录每个解被支配的次数
    rank = [0 for _ in range(0, len(values1))]  # 记录每个解所处的 Pareto 前沿层级

    # 对每个解计算被支配解集合 S 和支配该解的次数 n
    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                    values1[p] >= values1[q] and values2[p] > values2[q]) or (
                    values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                    values1[q] >= values1[p] and values2[q] > values2[p]) or (
                    values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        # 如果一个解没有被任何其他解支配，则将其归为 Pareto 前沿的第一层
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    # 循环计算 Pareto 前沿集合
    i = 0
    while front[i]:
        Q = []
        for p in front[i]:
            # 遍历被支配解集合 S，更新其 n 值
            for q in S[p]:
                n[q] = n[q] - 1
                # 如果某个解 q 不被其他解支配，则将其归为下一层 Pareto 前沿
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        # 将下一层 Pareto 前沿加入到 front 中
        front.append(Q)

    # 删除最后一个空元素
    del front[len(front) - 1]
    # 返回 Pareto 前沿集合
    return front


def crowding_distance(values1, values2, fronti):
    """
    计算 Pareto 前沿中每个解的拥挤距离
    :param values1: 一个列表，表示所有解在目标函数 1 下的取值
    :param values2: 一个列表，表示所有解在目标函数 2 下的取值
    :param fronti: 一个列表，包含 Pareto 前沿中某一层的非支配解的索引
    :return 一个列表，表示 Pareto 前沿中每个解的拥挤距离
    """
    distance = [0 for _ in range(0, len(fronti))]  # 初始化第i层所有解的拥挤距离为 0
    sorted1 = sort_by_values(fronti, values1[:])  # 根据目标函数 1 的取值，为当前前沿层排序并得到排序后的索引列表
    sorted2 = sort_by_values(fronti, values2[:])  # 根据目标函数 2 的取值，为当前前沿层排序并得到排序后的索引列表

    # 对于前沿中的第一个和最后一个解，将其拥挤距离设为一个较大的数
    distance[0] = 4444444444444444
    distance[len(fronti) - 1] = 4444444444444444

    # 计算前沿中其他解的拥挤距离
    if len(distance) <= 2:
        return distance
    for k in range(1, len(fronti) - 1):
        # 按照目标函数 1 进行计算，并将结果加到该解的拥挤距离上
        distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (max(values1) - min(values1))
        # 按照目标函数 2 进行计算，并将结果加到该解的拥挤距离上
        distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (max(values2) - min(values2))

    return distance  # 返回所有解的拥挤距离列表


values1 = [5, 2, 9, 3, 7, 4, 4]
values2 = [6, 4, 8, 2, 5, 3, 7]
front = fast_non_dominated_sort(values1, values2)  # [[2], [0, 4, 6], [1, 5], [3]]
print(front)
front_1 = []
for i in range(len(front)):
    # sorted1 = sort_by_values(front[i], values1[:])
    # sorted2 = sort_by_values(front[i], values2[:])
    # print("sorted1=", sorted1, "sorted2=", sorted2)
    # distance = crowding_distance(values1, values2, front[i])
    # print("distance=", distance)
    # print("==========================")
    front_i = [index_of(front[i][j],front[i]) for j in range(0,len(front[i]))]
    print(front_i)
