import random
from parse_env import env_data
from parse_env import rows
from parse_env import columns
from parse_env import loc_map
from parse_env import robot_current_loc
import a_star

#判断机器人在loc的位置是否可以执行act的操作
#loc -- tuple, 机器人当前位置
#act -- string, 机器人将要执行的操作
#return -- bool， 可以移动返回true
def is_move_valid_special(loc, act):
    #TODO 8
    return is_move_valid(env_data, loc, act)

#判断机器人在loc的位置是否可以执行act的操作
#env_data_ -- list， 模拟环境数据
#loc -- tuple, 机器人当前位置
#act -- string, 机器人将要执行的操作
#return -- bool， 可以移动返回true
def is_move_valid(env_data_, loc, act):
    #TODO 9
    now_row, now_column = loc
    ret = False
    if act == 'u': #上
        if now_row - 1 >= 0 and env_data[now_row-1][now_column] != 2:
            return True
    elif act == 'd': #下
        if now_row + 1 <= rows - 1 and env_data[now_row+1][now_column] != 2:
            return True
    elif act == 'l': #左
        if now_column - 1 >= 0 and env_data[now_row][now_column-1] != 2:
            return True
    elif act == 'r': #右
        if now_column + 1 <= columns - 1 and env_data[now_row][now_column+1] != 2:
            return True

    return False

#获得机器人在当前位置可以移动的方向的list
#env_data_ -- list， 模拟环境数据
#loc -- tuple, 机器人当前位置
#return -- list， 可以移动的方向的list
def valid_actions(env_data_, loc):
    ret = []
    if is_move_valid(env_data_, loc, 'u'):
        ret.append('u')
    if is_move_valid(env_data_, loc, 'd'):
        ret.append('d')
    if is_move_valid(env_data_, loc, 'l'):
        ret.append('l')
    if is_move_valid(env_data_, loc, 'r'):
        ret.append('r')
    return ret

#控制机器人，在loc位置做act操作，返回更新后的位置
#loc -- tuple, 机器人当前位置
#act -- string, 机器人将要执行的操作
#return --tuple， 更新后的位置
def move_robot(loc, act):
    now_row, now_column = loc
    if is_move_valid_special(loc, act):
        if act == 'u': #上
            now_row -= 1
        elif act == 'd': #下
            now_row += 1
        elif act == 'l': #左
            now_column -= 1
        elif act == 'r': #右
            now_column += 1
    return (now_row, now_column)

#判断机器人是否能到达目标位置
def is_can_move(env_data_, now_loc, dest_loc):
    now_row, now_column = now_loc
    dest_row, dest_column = dest_loc
    if env_data_[dest_row][dest_row] != 2:
        if now_row - 1 == dest_row and now_column == dest_column or \
           now_row + 1 == dest_row and now_column == dest_column or \
           now_row == dest_row and now_column - 1 == dest_column or \
           now_row == dest_row and now_column + 1 == dest_column:
           return True

    return False

#随机移动机器人
#env_data_ -- list， 模拟环境数据
#loc -- tuple, 机器人当前位置
def random_choose_actions(env_data_, loc):
    new_loc = loc
    for count in range(300):
        act_list = valid_actions(env_data_, new_loc)
        if len(act_list) != 0:
            act = random.choice(act_list)
            new_loc = move_robot(new_loc, act)
        now_row, now_column = new_loc
        if env_data[now_row][now_column] == 3:
            print("在第{}个回合找到宝藏！".format(count))
            break
    if count == 299:
        print("机器人迷路了!")

#使用A*算法获得规划的路径，并驱动机器人走到目标位置
def auto_move_robat(env_data_, loc):
    path = a_star.a_star(env_data_, 1, 3, 2)
    path.reverse()
    print(path)
    if path[0] == loc:
        now_loc = loc
        for index in range(1, len(path)):
            if is_can_move(env_data_, now_loc, path[index]):
                now_loc = path[index]
            else:
                print("你确定路径是对的吗，我走不过去呢!")
        now_row, now_column = now_loc
        if env_data_[now_row][now_column] == 3:
            print("我找到了宝藏！")


if __name__ == "__main__":
#    random_choose_actions(env_data, robot_current_loc)
    auto_move_robat(env_data, robot_current_loc)