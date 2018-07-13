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

    init_pop_pd = opd.to_dataframe(init_population[i]) #转为dataframe
    opd.excelAddSheet(init_pop_pd,'excel_output2018071204.xlsx','sheet'+str(i+1))

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

# 尝试将一个点插入到其他路径中
for path in  init_population[0]:
    if path.id != "DP0147":
        tt = insert_opt(12, path.path, path.vehicle_id-1)
        if tt != None:
            print(tt.path, tt.total_cost)
# print("done")