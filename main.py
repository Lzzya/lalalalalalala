import load_data as ldd
import output_data as opd
import copy
import algorithm.init as ai
import random
from algorithm.optimize import single_path_opt

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
    opd.excelAddSheet(init_pop_pd,'excel_output2018070309.xlsx','sheet'+str(i+1))

# 测试当前个体的路径中是否有可以调整后还可行的路径
total_change_redu = []
for path in  init_population[0]:
    print(path.id)
    candidate_path_tc =  single_path_opt(path.path, path.vehicle_id-1)
    if len(candidate_path_tc) != 0:
        change_redu = path.total_cost - min(candidate_path_tc)
        if change_redu > 0:
            print("可降低路径",path.path, change_redu)
            total_change_redu.append(change_redu)

print(total_change_redu)
print(len(total_change_redu),sum(total_change_redu))


print("done")