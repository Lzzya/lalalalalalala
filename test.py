from algorithm.calculate import path_distance_time
from algorithm.verify import if_path_legal
import load_data as ldd
from algorithm.verify import if_go_to_charge

warehouse, orders, charging, id_type_map = ldd.load_node_info("data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)
vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')
for o in orders:
    o.set_charging(charging, distance_matrix)
#
# test_path = [402,464,25,993,1053,587]
# try_path = [633, 188]
# t = path_distance_time(test_path,distance_matrix, time_matrix)
# t2 = path_distance_time(try_path,distance_matrix, time_matrix)
# t_if = if_path_legal(id_sorted_orders, try_path, distance_matrix, time_matrix, vehicles[1], id_type_map)
# print("该路径是否合法",t_if)
# print(t,t2)

# print(orders[822].charging_binding)
# t = if_go_to_charge(id_sorted_orders, [822], distance_matrix, time_matrix, vehicles[1], id_type_map,0.3)


t = if_path_legal(id_sorted_orders, [822], distance_matrix, time_matrix, vehicles[1], id_type_map)
print(t)
