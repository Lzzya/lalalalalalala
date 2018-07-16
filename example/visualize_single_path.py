# 可视化一个给定的路径

from visualize.v import plot_one_path_liu
import load_data as ldd

warehouse, orders, charging, id_type_map = ldd.load_node_info("../data/input_node.csv")
plot_one_path_liu(warehouse, orders, charging,[42, 670, 35, 402, 588, 112, 706, 1006], id_type_map)
