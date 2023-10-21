# Program Name: NSGA-II.py
# Description: This is a python implementation of Prof. Kalyanmoy Deb's popular NSGA-II algorithm
# Author: Haris Ali Khan 
# Supervisor: Prof. Manoj Kumar Tiwari

# Importing required modules
import math
import random
import matplotlib.pyplot as plt


# First function to optimize
def function1(x):
    value = -x ** 2
    return value


# Second function to optimize
def function2(x):
    value = -(x - 2) ** 2
    return value


# Function to find index of list
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
    :param list1: 要排序的列表
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


# Function to calculate crowding distance
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


# Function to carry out the crossover
def crossover(a, b):
    '''
    输入参数a和b是两个基因，其中r是一个0到1之间的随机数。该函数根据随机数r的大小，选择将a和b进行加权平均或者差值运算，来生成新的基因。然后，通过调用mutation函数对新的基因进行变异处理。
    :param a:
    :param b:
    :return:
    '''
    r = random.random()
    if r > 0.5:
        return mutation((a + b) / 2)
    else:
        return mutation((a - b) / 2)


# Function to carry out the mutation operator
def mutation(solution):
    '''
    输入参数solution是一个基因。该函数根据mutation_prob的大小，决定是否对基因进行变异处理。mutation_prob是一个0到1之间的随机数，用来表示变异的概率。在这个函数中，如果mutation_prob小于1，则将solution的值替换为min_x和max_x之间的随机数。
    :param solution:
    :return:
    '''
    mutation_prob = random.random()     # 变异概率
    if mutation_prob < 1:   # 这里表示一定会变异
        solution = min_x + (max_x - min_x) * random.random()    # 随机替换掉一个x的取值
    return solution


# Main program starts here
if __name__ == '__main__':
    pop_size = 20  # 种群大小
    max_gen = 921  # 最大迭代次数

    # Initialization
    min_x = -55  # x的取值范围（定义域）
    max_x = 55
    solution = [min_x + (max_x - min_x) * random.random() for _ in range(0, pop_size)]  # 在最大值和最小值之间生成随机的x取值列表
    gen_no = 0  # 当前迭代次数
    while gen_no < max_gen:
        # 计算两个函数在当前x取值下的y值（y1、y2）
        function1_values = [function1(solution[i]) for i in range(0, pop_size)]
        function2_values = [function2(solution[i]) for i in range(0, pop_size)]
        # 对y1和y2两个列表进行非支配排序，返回帕累托前沿中每层非支配解的索引
        non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
        # print("non_dominated_sorted_solution=", non_dominated_sorted_solution)
        print("The best front for Generation number ", gen_no, " is")
        for valuez in non_dominated_sorted_solution[0]:
            print(round(solution[valuez], 3), end=" ")  # 保留3位小数
        print("\n")
        crowding_distance_values = []   # 拥挤距离
        for i in range(0, len(non_dominated_sorted_solution)):
            crowding_distance_values.append(
                crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
        solution2 = solution[:]     # 将x取值列表深拷贝给solution2
        # Generating offsprings
        # 将solution2进行交叉和变异生成子代，返回2*pop_size长度的新的solution2列表，前pop_size是父代，后pop_size是子代
        while len(solution2) != 2 * pop_size:
            a1 = random.randint(0, pop_size - 1)
            b1 = random.randint(0, pop_size - 1)
            solution2.append(crossover(solution[a1], solution[b1]))
        # 计算新的y1和y2列表（新解是由父代和子代拼接成的2*pop_size列表）
        function1_values2 = [function1(solution2[i]) for i in range(0, 2 * pop_size)]
        function2_values2 = [function2(solution2[i]) for i in range(0, 2 * pop_size)]
        # 对新的y1和y2列表进行非支配排序（父代+子代）
        non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:])
        crowding_distance_values2 = []  # 新的拥挤距离（父代+子代）
        for i in range(0, len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(
                crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))
        new_solution = []   #
        for i in range(0, len(non_dominated_sorted_solution2)): # front各层的索引
            non_dominated_sorted_solution2_1 = [
                index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
                range(0, len(non_dominated_sorted_solution2[i]))]
            # 根据拥挤距离对非支配解的每一层进行排序
            front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
            front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                     range(0, len(non_dominated_sorted_solution2[i]))]
            front.reverse()     # 逆序，选择最末pop_size的front值（因为这里已经按照拥挤距离排序了，逆序表示选择拥挤距离较大的值，以尽可能保持解的多样性）
            for value in front:
                new_solution.append(value)
                if len(new_solution) == pop_size:
                    break
            if len(new_solution) == pop_size:
                break
        solution = [solution2[i] for i in new_solution]
        gen_no = gen_no + 1

    # 打印一下最终解的非支配排序结果看一下（结果发现所有的解都是非支配解。。。）
    # final_f1_values = [function1(solution[i]) for i in range(0, pop_size)]
    # final_f2_values = [function2(solution[i]) for i in range(0, pop_size)]
    # sort_result = fast_non_dominated_sort(final_f1_values,final_f2_values)
    # print(sort_result)

    # Lets plot the final front now
    function1 = [i * -1 for i in function1_values]
    function2 = [j * -1 for j in function2_values]
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
