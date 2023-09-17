import pandas as pd
import matplotlib.pyplot as plt
import ast
import json

data_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/data/'
result_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/result/'

file_name = 'fixed_spots_0906.csv'
# file_name = 'test.csv'
x_params = 'distance_to_right_hard_boundary'
y_params = ['speed', 'acc' ]


plt_name= 'pic_' + file_name[:-4] + '_' + x_params + '_' + '_'.join(y_params) + '.pdf'

data_pd = pd.read_csv(data_dir_path + file_name, sep=',')

def generate_unique_id(row):
	return row['trip_id'] + str(row['start_time']) + str(row['end_time'])

data_pd['unique_id'] = data_pd.apply(generate_unique_id, axis=1)

sorted_data_pd = data_pd.groupby(data_pd['unique_id']).apply(lambda x: x.sort_values('timestamp', ascending=True))

trip_id_list = sorted_data_pd['unique_id'].drop_duplicates(keep='first').to_numpy().tolist()


# print(trip_id_list)
 
# 为每个参数创建一个子图
# params = ['trip_id', 'start_time', 'end_time', 'observed_spot', 'start_point_pj', 'end_point_pj', 'steering_angle', 'acc', 'timestamp', 'speed', 'avg_lane_width', 'dist_to_center_line', 'distance_to_left_hard_boundary', 'distance_to_right_hard_boundary', 's', 'd', 'left_zone_type', 'right_zone_type', 'left_dist_bw_lm_hb', 'right_dist_bw_lm_hb', 'current_curvature', 'yaw', 'ego_lane_obj_cnt', 'adjacent_lane_obj_cnt']
 



# # ---------------  画多个图检查问题 -----------------------------
# fig = plt.figure(figsize=(100, 100))
# length = len(trip_id_list)
# fig, axs = plt.subplots(length,2, figsize=(25, 20))



# # 对每个参数进行处理
# for index, item_trip_id in enumerate(trip_id_list):
#     cur_item_trip_df = sorted_data_pd[ sorted_data_pd['trip_id'] == item_trip_id ]
#     # 对每个参数进行处理
#     cur_item_x_list = []
#     cur_item_y_dict = {}
#     for item_y in y_params:
#         cur_item_y_dict[item_y] = []

#     for i, row in cur_item_trip_df.iterrows(): #i是索引，row是每行的数据
#         # if row['overtake_situation'] != 'ego_overtake_obj': #所在的row ！=overtake_situation 为超车 跳过循环
#         #     continue                                        # continue for 回到for
#         # 使用ast.literal_eval解析字典，并计算最大的timestamp数量    
#         # time_seq_list = ast.literal_eval(row['time_seq_list']) if isinstance(row['time_seq_list'], str) else row['time_seq_list']  #取出每一行的timestamp的数据 把它变成python能理解的数据结构
        
#         cur_item_x_list.append(row['distance_to_right_hard_boundary'])
#         for item_y in y_params:
#             cur_item_y_dict[item_y].append(row[item_y])


#     subplot_1 = axs[index][0]
#     subplot_1.plot(cur_item_x_list, cur_item_y_dict[y_params[0]])
#     subplot_1.set_title(item_trip_id)
#     subplot_1.set_xlabel(x_params)
#     subplot_1.set_ylabel(y_params[0])

#     subplot_2 = axs[index][1]
#     subplot_2.plot(cur_item_x_list, cur_item_y_dict[y_params[1]])
#     subplot_2.set_title(item_trip_id)
#     subplot_2.set_xlabel(x_params)
#     subplot_2.set_ylabel(y_params[1])

# # ---------------  画多个图检查问题 end -----------------------------

# ---------------  所有 trip id 画 1 个图 -----------------------------
fig = plt.figure(figsize=(50, 30))
subplot_1 = plt.subplot(1,2,1)
subplot_2 = plt.subplot(1,2,2)

# 对每个参数进行处理
for index, item_trip_id in enumerate(trip_id_list):
    cur_item_trip_df = sorted_data_pd[ sorted_data_pd['unique_id'] == item_trip_id ]
    # 对每个参数进行处理
    cur_item_x_list = []
    cur_item_y_dict = {}
    for item_y in y_params:
        cur_item_y_dict[item_y] = []

    for i, row in cur_item_trip_df.iterrows(): #i是索引，row是每行的数据
        # if row['overtake_situation'] != 'ego_overtake_obj': #所在的row ！=overtake_situation 为超车 跳过循环
        #     continue                                        # continue for 回到for
        # 使用ast.literal_eval解析字典，并计算最大的timestamp数量    
        # time_seq_list = ast.literal_eval(row['time_seq_list']) if isinstance(row['time_seq_list'], str) else row['time_seq_list']  #取出每一行的timestamp的数据 把它变成python能理解的数据结构
        
        cur_item_x_list.append(row['distance_to_right_hard_boundary'])
        for item_y in y_params:
            cur_item_y_dict[item_y].append(row[item_y])



    subplot_1.scatter(cur_item_x_list, cur_item_y_dict[y_params[0]], alpha=0.3,color='b')
    subplot_2.scatter(cur_item_x_list, cur_item_y_dict[y_params[1]], alpha=0.3,color='b')

subplot_1.set_xlabel(x_params)
subplot_1.set_ylabel(y_params[0])
subplot_2.set_xlabel(x_params)
subplot_2.set_ylabel(y_params[1])
# ---------------  所有 trip id 画 1 个图 end -----------------------------

plt.tight_layout()
# plt.legend()
# plt.show()
record_file_name = result_dir_path + plt_name
print(record_file_name)
plt.savefig(record_file_name)
plt.cla()




            
        # if row['overtake_situation'] != 'ego_overtake_obj':
        #     continue
        # 使用ast.literal_eval解析字典，并计算最大的timestamp数量    
        # time_seq_list = ast.literal_eval(row['time_seq_list']) if isinstance(row['time_seq_list'], str) else row['time_seq_list']
        # x_values = 0
        # y_values = 0
        # for item_statis in time_seq_list:
        #     # statis_dict = json.loads(item_statis) if isinstance(item_statis, str) else item_statis
        #     vehicle_length = row['vehicle_length']
        #     tail_to_head_ver_dis = statis_dict.get('tail_to_head_ver_dis')
            
        #     if params[0] == 'ego_vel-obj_vel':
        #         y_param =  statis_dict.get('ego_vel') - statis_dict.get('obj_vel')
        #     elif params[0] == 'vehicle_length':
        #         y_param = vehicle_length
        #     else:    
        #         y_param = statis_dict.get(params[0])
        #     x_param = -1 * statis_dict.get(params[1])
        #     if x_param >= 0 and x_param <= vehicle_length + 5:
        #         x_values += 1
        #         y_values += y_param
        # if x_values == 0:
        #     print('human_data')
        #     print(row)
        #     print('\n\n\n')
        # else:
        #     y_values /= x_values
        # values = [statis.get(param) for statis in row['time_seq_list']]  # 提取参数值
        # plt.scatter(x_values, y_values, color='b', linewidth=0.5)


# plt.xlabel(params[1])
# plt.ylabel(params[0])
# # plt.xticks(range(timestamp_max))
 
# plt.tight_layout()
# # plt.legend()
# # plt.show()
# record_file_name = result_dir_path + plt_name
# print(record_file_name)
# plt.savefig(record_file_name)
# plt.cla()