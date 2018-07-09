import matplotlib.pyplot as plt
from utils import search_node

def plot_one_path(warehouse, orders, charging, path, id_type_map):
    order_x_coor = []
    order_y_coor = []
    charging_x_coor = []
    charging_y_coor = []

    for o in orders:
        order_x_coor.append(o.lng)
        order_y_coor.append(o.lat)
    for c in charging:
        charging_x_coor.append(c.lng)
        charging_y_coor.append(c.lat)

    plt.scatter([warehouse.lng], [warehouse.lat], s=5, c='r')
    plt.scatter(order_x_coor, order_y_coor, s=5, c='b')
    plt.scatter(charging_x_coor, charging_y_coor, s=5, c='lime')

    path_x = [warehouse.lng]
    path_y = [warehouse.lat]

    for nid in path:
        node = None
        if (id_type_map[nid] == 2):
            node = search_node(orders, nid)
        elif (id_type_map[nid] == 3):
            node = search_node(charging, nid)
        else:
            raise Exception
        path_x.append(node.lng)
        path_y.append(node.lat)

    path_x.append(warehouse.lng)
    path_y.append(warehouse.lat)

    plt.plot(path_x, path_y, linewidth=1)


    plt.show()

def plot_one_path_liu(warehouse, orders, charging, path, id_type_map):
    order_x_coor = []
    order_y_coor = []
    charging_x_coor = []
    charging_y_coor = []

    for o in orders:
        order_x_coor.append(o.lng)
        order_y_coor.append(o.lat)
    for c in charging:
        charging_x_coor.append(c.lng)
        charging_y_coor.append(c.lat)

    plt.scatter([warehouse.lng], [warehouse.lat], s=5, c='r')
    plt.scatter(order_x_coor, order_y_coor, s=5, c='b')
    plt.scatter(charging_x_coor, charging_y_coor, s=5, c='lime')

    path_x = [warehouse.lng]
    path_y = [warehouse.lat]
    path_id = [warehouse.id]

    for nid in path:
        node = None
        if (id_type_map[nid] == 2):
            node = search_node(orders, nid)
        elif (id_type_map[nid] == 3):
            node = search_node(charging, nid)
        else:
            raise Exception
        path_x.append(node.lng)
        path_y.append(node.lat)
        path_id.append(node.id)

    path_x.append(warehouse.lng)
    path_y.append(warehouse.lat)
    path_id.append(warehouse.id)

    plt.plot(path_x, path_y, linewidth=1)
    for i,j,k in zip(path_x, path_y, path_id):
        plt.text(i,j,'%.0f'%k, ha='center', va='bottom', fontsize=10.5)

    plt.show()


def plot_pathes(warehouse, orders, charging, pathes, id_type_map):
    order_x_coor = []
    order_y_coor = []
    charging_x_coor = []
    charging_y_coor = []

    for o in orders:
        order_x_coor.append(o.lng)
        order_y_coor.append(o.lat)
    for c in charging:
        charging_x_coor.append(c.lng)
        charging_y_coor.append(c.lat)

    plt.scatter([warehouse.lng], [warehouse.lat], s=5, c='r')
    plt.scatter(order_x_coor, order_y_coor, s=5, c='b')
    plt.scatter(charging_x_coor, charging_y_coor, s=5, c='lime')

    for path in pathes:
        path_x = []
        path_y = []
        for nid in path:
            node = None
            if (id_type_map[nid] == 2):
                node = search_node(orders, nid)
            elif (id_type_map[nid] == 3):
                node = search_node(charging, nid)
            else:
                raise Exception
            path_x.append(node.lng)
            path_y.append(node.lat)

        plt.plot(path_x, path_y, linewidth=1)

    plt.show()