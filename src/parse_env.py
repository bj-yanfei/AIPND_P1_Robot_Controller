import helper

env_data = helper.fetch_maze()

#TODO 1模拟环境的行数
rows = len(env_data)

#TODO 2模拟环境的列数
columns = len(env_data[0])

#TODO 3取出模拟环境第三行第六列的元素
row_3_col_6 = env_data[3-1][6-1]


#TODO 4计算模拟环境中，第一行的的障碍物个数。
number_of_barriers_row1 = 0
for num in env_data[0]:
    if num == 2:
        number_of_barriers_row1 += 1

#TODO 5计算模拟环境中，第三列的的障碍物个数。
number_of_barriers_col3 = 0
for index in range(rows):
    if env_data[index][3-1] == 2:
        number_of_barriers_col3 += 1

loc_map = {} #TODO 6按照上述要求创建字典
for row in range(rows):
    for column in range(columns):
        if env_data[row][column] == 1:
            loc_map['start'] = (row, column)
        if env_data[row][column] == 3:
            loc_map['destination'] = (row, column)

robot_current_loc = loc_map['start'] #TODO 7保存机器人当前的位置


if __name__ == "__main__":
    print("迷宫共有", rows, "行", columns, "列，第三行第六列的元素是", row_3_col_6)
    print("迷宫中，第一行共有", number_of_barriers_row1, "个障碍物，第三列共有", number_of_barriers_col3, "个障碍物。")
    print("机器人当前的位置: ", robot_current_loc)
