from copy import deepcopy
from algorithm.verify import if_path_legal
import datetime
import load_data as ldd
from entity.TransportPath import TransportPath

warehouse, orders, charging, id_type_map = ldd.load_node_info("data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)

vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')

for o in orders:
    o.set_charging(charging, distance_matrix)
    #o.set_distance_sorted_order(copy.deepcopy(orders), distance_matrix)

# 根据提供的两个索引，交换path中的相应客户
def single_path_exchage(path , index1 , index2):
    new_path = deepcopy(path)
    new_path[index2], new_path[index1] = path[index1], path[index2]
    return new_path
# 2客户交叉变异枚举，排列组合c29=36，故枚举
def single_path_opt(path, v_type):
    # 临时
    count_chage = 0
    # 使用
    candidate_path_tc = []
    idx = 0
    vehicle_info = vehicles
    path_len = len(path)
    min_cost = 5000
    min_cost_path = None
    for i in range(path_len):
        for j in range(path_len):
            if i < j:
                new_path = single_path_exchage(path , i ,j)
                count_chage += 1
                # 判断当前交换后的路径是否合法
                if if_path_legal(id_sorted_orders, new_path,
                              datetime.datetime(2018, 6, 18, 8, 0, 0),
                              distance_matrix, time_matrix,
                              vehicles[v_type], id_type_map)[0] == True:
                    # print(new_path)
                    # 计算当前路径的总成本你是否降低
                    tp = TransportPath(new_path, v_type + 1)  # 实例化一个运输路径，接下来计算一些属性
                    tp = tp.calc_path_info(idx + 1, distance_matrix, time_matrix, vehicle_info, id_sorted_orders,
                                           id_type_map)
                    # print(tp.total_cost)
                    if tp.total_cost < min_cost:
                        min_cost = tp.total_cost
                        min_cost_path = tp
                # else:
                #     ttt =if_path_legal(id_sorted_orders, new_path,
                #                   datetime.datetime(2018, 6, 18, 8, 0, 0),
                #                   distance_matrix, time_matrix,
                #                   vehicles[v_type], id_type_map)
                #     print(ttt)
    # print("交换次数",count_chage)
    return min_cost_path
# 3个客户重排列变异
def three_permutation(three_points_in_path):
    all_conb = []
    for p in three_points_in_path:
        new_conb = []
        three_p = deepcopy(three_points_in_path)
        if len(three_points_in_path) != 0:
            new_conb.append(p)
            three_p.remove(p)
            for p2 in three_p:
                new_conb2 = deepcopy(new_conb)
                two_p = deepcopy(three_p)
                new_conb2.append(p2)
                two_p.remove(p2)
                new_conb2.append(two_p[0])
                all_conb.append(new_conb2)
    return all_conb

# 从一个列表中取指定位置的连续三个点，然后插入新的三个点
def replace_section(path, new_section, s_idx):
    new_path = deepcopy(path)
    if len(path) > 2:
        if s_idx < len(path) -2: #插入点以后得有3个点
            new_path[s_idx],new_path[s_idx+1],new_path[s_idx+2] = new_section[0],new_section[1],new_section[2]
        else:
            print("插入点位置太靠后，不合理")
    else:
        print("路径长度不足3，不处理")
    return new_path

# 局部三个打乱，返回该规则下找到的成本最低的新路径
def single_path_opt2(path, v_type):
    idx = 0
    candidate_path_tc = []
    vehicle_info = vehicles
    count_change = 0
    min_cost = 5000
    min_cost_path = None
    if len(path) >2:
        for i in range(len(path)-2):
            candidate_paths = three_permutation(path[i:i+3])
            for cp in candidate_paths:
                count_change += 1
                new_path = replace_section(path, cp, i)
                if if_path_legal(id_sorted_orders, new_path,
                                 datetime.datetime(2018, 6, 18, 8, 0, 0),
                                 distance_matrix, time_matrix,
                                 vehicles[v_type], id_type_map)[0] == True:
                    # print("可行",new_path)
                    # 计算当前路径的总成本你是否降低
                    # count_change += 1
                    tp = TransportPath(new_path, v_type + 1)  # 实例化一个运输路径，接下来计算一些属性
                    tp = tp.calc_path_info(idx + 1, distance_matrix, time_matrix, vehicle_info, id_sorted_orders,
                                           id_type_map)
                    if tp.total_cost < min_cost:
                        min_cost = tp.total_cost
                        min_cost_path = tp
                    # print(tp.total_cost)
                    # candidate_path_tc.append(tp.total_cost)
    else:
        print("路径长度不足3，暂不处理")
    # print(count_change)
    return min_cost_path

path = [605, 763, 947, 408, 801, 459, 693, 283, 590, 269]
# zzz = three_permutation(path)
aaa= single_path_opt2(path, 0)
# print(min(aaa))
print("END")