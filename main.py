import load_data as ldd
import output_data as opd
import copy
import algorithm.init as ai
import random
from algorithm.optimize import single_path_opt
from algorithm.optimize import single_path_opt2
from algorithm.optimize import insert_opt

#random.seed(time.time())
random.seed(0)

warehouse, orders, charging, id_type_map = ldd.load_node_info("data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)

vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')

idx = 0
orders_cp = copy.deepcopy(orders)
for o in orders:
    o.set_charging(charging, distance_matrix)
    #o.set_distance_sorted_order(orders_cp, distance_matrix)

print("generating initial population")
init_population = []
INIT_POPULATION_SIZE = 1

for i in range(INIT_POPULATION_SIZE):
    #init_population.append(ai.random_individual(warehouse, id_sorted_orders, angle_sorted_orders, charging, vehicles, id_type_map, distance_matrix, time_matrix))
    init_population.append(
        ai.better_init_individual(warehouse, id_sorted_orders, charging, vehicles, id_type_map,
                                  distance_matrix, time_matrix))

    # init_pop_pd = opd.to_dataframe(init_population[i]) #转为dataframe
    # opd.excelAddSheet(init_pop_pd,'excel_output2018071204.xlsx','sheet'+str(i+1))

# 测试当前个体的路径中交换带来的变异效果
# total_change_redu = []
# for path in  init_population[0]:
#     print(path.id)
#     candidate_path =  single_path_opt(path.path, path.vehicle_id-1)
#     if candidate_path != None:
#         change_redu = path.total_cost - candidate_path.total_cost
#         if change_redu > 0:
#             print("可降低路径", path.id, "为", candidate_path.path,"下降", change_redu)
#             total_change_redu.append(change_redu)
#
# print(total_change_redu)
# print(len(total_change_redu),sum(total_change_redu))

# 局部3个客户（包含充电站）重组变异
# total_change_redu = []
# for path in  init_population[0]:
#     print(path.id)
#     candidate_path =  single_path_opt2(path.path, path.vehicle_id-1)
#     if candidate_path != None:
#         change_redu = path.total_cost - candidate_path.total_cost
#         if change_redu > 0:
#             # print("可降低路径", path.id, "为", candidate_path.path,"下降", change_redu)
#             total_change_redu.append(change_redu)
#
# # print(total_change_redu)
# print("优化路数：",len(total_change_redu),"优化成本：",sum(total_change_redu))

# 尝试将一个点插入到其他路径中,找到最好的插入路径，
# 并判断插入后总成本有没有下降，下降才输出,输出新路径和被插入路径的id
def find_insert_path(point, point_inpath_id, path_inpath_cost,population):
    min_inc = 5000
    idx = 0
    for path in  population:
        if path.id != point_inpath_id:
            new_path = insert_opt(point, path.path, path.vehicle_id-1)
            if new_path != None:
                path_cost_inc = new_path.total_cost - path.total_cost
                if path_cost_inc < min_inc:
                    min_inc = path_cost_inc
                    min_inc_path = new_path
                    min_inc_path_di = idx
        idx += 1
    if min_inc < path_inpath_cost:
        print(min_inc_path.path, min_inc_path.total_cost)
        return min_inc_path, min_inc_path_di

def path_insert_opt(splited_path, individual):
    t_individual = copy.deepcopy(individual)
    splited_num = 0 #差分后找到插入路径的客户数
    splited_path_orders_num = 0 #一条路径中的客户数
    path_cost_incs = []
    for p in splited_path.path:
        if id_type_map[p] == 2:  # 充电站就不往出插了
            splited_path_orders_num += 1
            for path in individual:
                if path.id != splited_path.id: # 自己不插自己
                    new_path = insert_opt(p, path.path, path.vehicle_id - 1)
                    if new_path != None:
                        splited_num += 1
                        path_cost_inc = new_path.total_cost - path.total_cost
        path_cost_incs.append(path_cost_inc)
    if sum(path_cost_incs) < splited_path.total_cost:
        
        # print(min_inc_path.path, min_inc_path.total_cost)
        # return min_inc_path, min_inc_path_di


    # t_individual = copy.deepcopy(individual)
    # for p in path.path:
    #     if id_type_map[p] == 2: # 充电站就不往出插了
    #         new_path, old_path_id=find_insert_path(p, path.id, path.total_cost, t_individual)
    #         if new_path != None: # 也就是有找到让成本下降的插入方案
    #             t_individual.pop(old_path_id)
    #             t_individual.append(new_path)
    #             print("ttt")
    return t_individual

exam_point = init_population[0][136-1]
ttt = path_insert_opt(exam_point, init_population[0])

# find_insert_path(12, "DP0147", 2183.464, init_population[0])
print("done")