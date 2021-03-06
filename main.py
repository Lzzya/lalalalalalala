import load_data as ldd
import output_data as opd
import copy
import algorithm.init as ai
import random

#random.seed(time.time())
random.seed(0)

warehouse, orders, charging, id_type_map = ldd.load_node_info("data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)

vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')

for o in orders:
    o.set_charging(charging, distance_matrix)
    #o.set_distance_sorted_order(copy.deepcopy(orders), distance_matrix)

print("generation initial population")
init_population = []
INIT_POPULATION_SIZE = 1

for i in range(INIT_POPULATION_SIZE):
    init_population.append(ai.random_individual(warehouse, id_sorted_orders, angle_sorted_orders, charging, vehicles, id_type_map, distance_matrix, time_matrix))
    init_pop_pd = opd.to_dataframe(init_population[i]) #转为dataframe
    opd.excelAddSheet(init_pop_pd,'excel_output2018070309.xlsx','sheet'+str(i+1))

print("done")