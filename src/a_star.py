"""
本A*算法，是为迷宫寻宝机器人定制，不同之处是机器人只有4个方向可移动：前后左右
估算成本采用曼哈顿距离，且没有对角线移动，即，横向和纵向距离之和
具体执行流程：
1、把起点加入open中，计算起点的f，g，h
2、遍历open，得到f最小的点，并把它作为当前点
3、把当前点移出open，放入close
4、对当前点周围的点（最多4个）做如下处理：
    a、如果该点是障碍物或边界或在close中，忽略
    b、如果该点不在open中，把它加入open，并把当前点设置为他的父节点，计算它的fgh
    c、如果该点已经在open中，检查路径是否更优：
        如果新g小于原有g，更新该点的父节点为当前点，并更新该点的fg

5、当终点放入了open，则成功找到结束
    或者open为空，则查找失败，没有找到路径
6、保存路径，从终点开始，沿着父节点移动直至起点

节点数据结构
当前点坐标(x, y)
父节点坐标(x, y)
f
g
h
约定边界外的点坐标为-1，起点的父节点也为(-1,-1)
"""

import math

init_node =  [(-1, -1),    #0, 当前坐标
              (-1,  -1),    #1, 父节点坐标
              0, 0, 0]      #2, 3, 4  f,g,h

map_data = []
start_node = list(init_node)
end_node = list(init_node)
open_list = []
close_list = []
rows = 0
columns = 0

#获得两个点之间的h值
def get_h(now_node, end_node_):
    now_node_x, now_node_y = now_node[0]
    end_x, end_y = end_node_[0]
    return math.fabs(now_node_x - end_x) + math.fabs(now_node_y - end_y)

def init(env_data, start_flag, end_flag):
    global rows
    rows = len(env_data)
    global columns
    columns = len(env_data[0])
    temp_map = [None] * rows
    for row in range(rows):
        temp_row = [None] * columns
        for column in range(columns):
            if env_data[row][column] == start_flag:
                start_node[0] = (row, column)
            if env_data[row][column] == end_flag:
                end_node[0] = (row, column)
            temp_node = list(init_node)
            temp_node[0] = (row, column)
            temp_row[column] = temp_node
        temp_map[row] = temp_row

    for map_ in temp_map:
        map_data.append(map_)

    start_node[4] = get_h(start_node, end_node)
    start_node[2] = start_node[3] + start_node[4]

    # print("node_map:", map_data)
    # print("rows: {}, columns: {}".format(rows, columns))
    # print("start_node:", start_node)
    # print("end_node:", end_node)

#判断某点是否在open list中
def is_in_list(list_, node_):
    for node in list_:
        if node[0] == node_[0]:
            return True
    return False

#从open list中找到f值最小的点
def get_min_f_node(list_):
    if len(list_):
        ret = 0
        the_min_f = list_[0][2]
        for index in range(len(list_)):
            if the_min_f >= list_[index][2]:
                the_min_f = list_[index][2]
                ret = index
        return list_[ret]

def deal_the_node(env_data, obs_flag, node_, now_node):
    node_x, node_y = node_[0]
    if (node_x >= 0) and (node_x < rows) and \
        (node_y >=0) and (node_y < columns) and \
        (env_data[node_x][node_y] != obs_flag) and \
        not is_in_list(close_list, node_):
        if not is_in_list(open_list, node_):
            node_[1] = now_node[0]
            map_data[node_x][node_y][1] = now_node[0]
            node_[3] = now_node[3] + 1
            node_[4] = get_h(node_, end_node)
            node_[2] = node_[3] + node_[4]
            open_list.append(node_)
        else:
            if now_node[3] + 1 < node_[3]:
                node_[1] = now_node[0]
                map_data[node_x][node_y][1] = now_node[0]
                node_[3] = now_node[3] + 1
                node_[2] = node_[3] + node_[4]


#遍历节点周围的4个点
def deal_neighbor_node(env_data, obs_flag, now_node):
    now_node_x, now_node_y = now_node[0]
    temp_node = list(init_node)
    temp_node[0] = (now_node_x - 1,  now_node_y)
    deal_the_node(env_data, obs_flag, temp_node, now_node) #up

    temp_node = list(init_node)
    temp_node[0] = (now_node_x + 1,  now_node_y)
    deal_the_node(env_data, obs_flag, temp_node, now_node) #down

    temp_node = list(init_node)
    temp_node[0] = (now_node_x,  now_node_y - 1)
    deal_the_node(env_data, obs_flag, temp_node, now_node) #left

    temp_node = list(init_node)
    temp_node[0] = (now_node_x,  now_node_y + 1)
    deal_the_node(env_data, obs_flag, temp_node, now_node) #right

#A*算法
#env_data_ -- list， 模拟环境数据
#start_flag -- int, 环境中起点标记
#end_flag -- int, 环境中终点标记
#obs_flag -- int,环境中障碍物标记
#return -- list， 规划出的路径list
def a_star(env_data, start_flag, end_flag, obs_flag):
    init(env_data, start_flag, end_flag)
    open_list.append(start_node)
    ret = []

    while True:
        if is_in_list(open_list, end_node):
            print("恭喜你，找到了那个路径!")
            break
        if not len(open_list):
            print("很遗憾，没有找到路径!")
            break

        now_node = get_min_f_node(open_list)

        open_list.remove(now_node)
        close_list.append(now_node)

        deal_neighbor_node(env_data, obs_flag, now_node)

    if is_in_list(open_list, end_node):
        now_node_x, now_node_y = end_node[0]
        while True:
            ret.append(map_data[now_node_x][now_node_y][0])
            now_node_x, now_node_y = map_data[now_node_x][now_node_y][1]
            if (now_node_x, now_node_y) == start_node[0]:
                ret.append(start_node[0])
                break
    return ret









