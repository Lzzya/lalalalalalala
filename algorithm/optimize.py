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
# 排列组合c29=36，故枚举
def single_path_opt(path, v_type):
    # 临时
    count_chage = 0
    # 使用
    candidate_path_tc = []
    idx = 0
    vehicle_info = vehicles
    path_len = len(path)
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
                    candidate_path_tc.append(tp.total_cost)
                # else:
                #     ttt =if_path_legal(id_sorted_orders, new_path,
                #                   datetime.datetime(2018, 6, 18, 8, 0, 0),
                #                   distance_matrix, time_matrix,
                #                   vehicles[v_type], id_type_map)
                #     print(ttt)

    print("交换次数",count_chage)
    return candidate_path_tc

# 测试
# t_path =  [14, 389, 538, 446, 495, 676, 969, 852, 692]
# temp123 = single_path_opt(t_path, 1)
# print(temp123)