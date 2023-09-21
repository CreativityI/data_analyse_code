import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import mean
import ast
import json
from scipy.interpolate import make_interp_spline


def generate_unique_id(row):
	return row['trip_id'] + '-' +  str(row['start_time']) + '-' + str(row['end_time'])

def generate_new_url(row):
    url_str = 'http://voyager.intra.xiaojukeji.com/static/ares-studio/?ds=voy-ws-bagfile&ds.end=' + str(row['end_time']) + '&ds.start=' + str(row['start_time']) + '&ds.trip_id=' + str(row['trip_id'])
    if url_str == 'http://voyager.intra.xiaojukeji.com/static/ares-studio/?ds=voy-ws-bagfile&ds.end=nan&ds.start=nan&ds.trip_id=17130_2':
        print('error')
    return url_str

def get_ego_lane_list(data_pd):
    unique_id_list = data_pd['unique_id'].drop_duplicates(keep='first').to_numpy().tolist()
    unique_id_ego_lane_list = []
    for item_unique_id in unique_id_list:
        item_unique_id_ego_lane_record_dict = {}
        item_data_pd = data_pd[ data_pd['unique_id'] == item_unique_id ]
        item_ego_lane_set = set()
        for i, row in item_data_pd.iterrows(): #i是索引，row是每行的数据
            if np.isnan(row['ego_lane']):
                item_ego_lane_set.add('nan')
            else:
                item_ego_lane_set.add(str(int(row['ego_lane'])))
            
            
        item_ego_lane_str = '/'.join(list(item_ego_lane_set))
        item_unique_id_ego_lane_record_dict['unique_id'] = item_unique_id
        item_unique_id_ego_lane_record_dict['ego_lane'] = item_ego_lane_str
        unique_id_ego_lane_list.append(item_unique_id_ego_lane_record_dict)
    return pd.DataFrame(unique_id_ego_lane_list)

def data_process(data_pd):
    print(data_pd.shape)
    data_pd = data_pd[['trip_id', 'start_time', 'end_time', 'ego_lane']].drop_duplicates(keep='first')
    print(data_pd.shape)
    data_pd['unique_id'] = data_pd.apply(generate_unique_id, axis=1)
    data_pd['url'] = data_pd.apply(generate_new_url, axis=1)

    unique_id_ego_lane_pd = get_ego_lane_list(data_pd)
    print(data_pd.shape)
    data_pd = data_pd[['trip_id', 'start_time', 'end_time', 'url', 'unique_id']].drop_duplicates(keep='first')
    print(data_pd.shape)
    data_pd = pd.merge( data_pd, unique_id_ego_lane_pd, on=['unique_id'])
    print(data_pd.shape)
    return data_pd[['trip_id', 'start_time', 'end_time', 'url', 'ego_lane']]


def read_data_process(data_dir_path, file_name_list):
    result_list = []
    for item_file_name in file_name_list:
        data_pd = pd.read_csv(data_dir_path + item_file_name, sep=',')
        result_list.append(data_pd)
    result_pd = pd.concat(result_list, axis=0)
    return result_pd



# ----- params ---------------------------

# ----- file params ----------------------
data_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/data/'
result_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/result/'

file_name = 'fixed_spots_0906.csv'

file_name_1 = 'job_id=76338856aa.csv'
file_name_2 = 'job_id=76338856ab.csv'
file_name_3 = 'job_id=76338856ac.csv'

file_name_list = [file_name_1, file_name_2, file_name_3]



# ---- pic params -----------------------

# trip_status = 'one_trip' # 只画单 trip
trip_status = 'multi_trip' # 画多 trip
ego_lane_id = 172609 # ego_lane 数据
trip_id = '14079_20230825_152354'
x_params = 'steering_angle'
# x_params = 's'
# y_params = 'speed'
y_params = 'acc'
# y_params = 'right_dist_bw_lm_hb' 
# y_params = 'steering_angle'
x_params_min = -1.5
x_params_max = 2.5
duration = 0.03

save_file_name = 'ego_lane_{ego_lane_id}_{trip_status}_{x_params}_{y_params}.pdf'.format(ego_lane_id=str(ego_lane_id), trip_status=trip_status, x_params=x_params, y_params=y_params)
print(save_file_name)
# ---------- read data --------------

data_pd = read_data_process(data_dir_path, file_name_list)
ego_lane_data_pd = data_pd[data_pd['ego_lane'] == ego_lane_id]



if trip_status == 'one_trip':
    if trip_id == '':
        print('trip id error')
    else:
        ego_lane_data_pd = ego_lane_data_pd[ego_lane_data_pd['trip_id'] == trip_id]

# 检查中间结果
# ego_lane_data_pd.to_csv(result_dir_path+'ego_lane.csv', sep=',', index=False)


ego_lane_data_pd['unique_id'] = ego_lane_data_pd.apply(generate_unique_id, axis=1)

unique_id_list = ego_lane_data_pd['unique_id'].drop_duplicates(keep='first').to_numpy().tolist()

fig = plt.figure(figsize=(25, 10))

all_y_list = []

x_columns = []

ego_lane_data_pd_x_dura_pd = ego_lane_data_pd[ (ego_lane_data_pd[x_params] >= x_params_min) & (ego_lane_data_pd[x_params] <= x_params_max)]

# for unique_id in unique_id_list:
#     cur_data_pd = ego_lane_data_pd_x_dura_pd[ego_lane_data_pd_x_dura_pd['unique_id'] == unique_id]
#     # sorted_data_pd = cur_data_pd.sort_values('timestamp', ascending=True)
#     x_value = cur_data_pd[x_params].to_numpy().tolist()

#     x_columns += x_value

x_columns = np.arange(x_params_min, x_params_max, duration).tolist()

# print(len(unique_id_list))
for unique_id in unique_id_list:
    cur_data_pd = ego_lane_data_pd[ego_lane_data_pd['unique_id'] == unique_id]
    sorted_data_pd = cur_data_pd.sort_values('timestamp', ascending=True)


    # x_value_index = sorted_data_pd[ (sorted_data_pd[x_params] > x_params_min) & (sorted_data_pd[x_params]< x_params_max)].index.tolist()
    # sorted_data_pd = sorted_data_pd.loc[x_value_index]
    sorted_data_pd = sorted_data_pd[ (sorted_data_pd[x_params] >= x_params_min) & (sorted_data_pd[x_params] <= x_params_max)]

    # check_series = sorted_data_pd[x_params] < x_params_min
    # if check_series.any():
    #     print(unique_id)
    #     continue

    x_value = sorted_data_pd[x_params].to_numpy().tolist()
    y_value = sorted_data_pd[y_params].to_numpy().tolist()

    cur_y_list = []
    
    x_columns_index = 0
    x_value_index = 0
    item_y_list = []
    # print('len x columns', len(x_columns))
    # print('len x value', len(x_value))
    while x_columns_index < len(x_columns):
        while x_value_index < len(x_value):
            if x_columns[x_columns_index] - x_value[x_value_index] < -1 * (duration/2):
                if item_y_list == []:
                    cur_y_list.append(np.nan)
                else:
                    cur_y_list.append(mean(item_y_list))
                    item_y_list = []
                x_columns_index += 1
                break
            else:
                item_y_list.append(y_value[x_value_index])
                x_value_index += 1
        
        if x_value_index >= len(x_value):
            if item_y_list != []:
                cur_y_list.append(mean(item_y_list))
                item_y_list = []
            else:
                cur_y_list.append(np.nan)
            x_columns_index += 1
    





    # cur_dict = dict(zip(x_value, y_value))
    # cur_y_list = []
    # for x in x_columns:
    #     cur_y_list.append(cur_dict.get(x, np.nan))

    all_y_list.append(cur_y_list)
    # # 平均值
    # x_value = sorted_data_pd[x_params].to_numpy().tolist()

    # check_series = sorted_data_pd[y_params] < 6
    # if check_series.any():
    #     continue


    # mean_y = sorted_data_pd[y_params].mean()
    # sorted_data_pd[y_params] = sorted_data_pd[y_params] - mean_y
    # y_value = sorted_data_pd[y_params].to_numpy().tolist()

    # 归一化 normalization
    # check_series = sorted_data_pd[y_params] < 6
    # if check_series.any():
    #     continue


    # min_y = sorted_data_pd[y_params].min()
    # max_y = sorted_data_pd[y_params].max()
    # duration = max_y - min_y
    # sorted_data_pd[y_params] = (sorted_data_pd[y_params] - min_y) / duration
    # x_value = sorted_data_pd[x_params].to_numpy().tolist()
    # y_value = sorted_data_pd[y_params].to_numpy().tolist()
    
    
    
    
    plt.plot(x_value, y_value, color='g', linewidth=3, alpha = 0.5)
    # plt.scatter(x_value, y_value, color='g', linewidth=0.01, alpha = 0.5)
zero_value = [0 for i in range(len(x_columns))]
plt.plot(x_columns, zero_value, color='r', linewidth=3, alpha = 0.5)

# print(len(all_y_list))
# print(len(x_value))
all_y_pd = pd.DataFrame(all_y_list)
print(len(all_y_pd.columns))
all_y_pd.columns = x_columns
all_y_pd.fillna(all_y_pd.mean())
mean_x_value = []
mean_y_value = []
for x in x_columns:
    # cur_pd = all_y_pd[ (all_y_pd[x].notnull()) & (all_y_pd[x] != '') ]
    # if cur_pd.shape[0] < 2:
    #     continue
    
    mean_x_value.append(x)
    mean_y_value.append(all_y_pd[x].mean())

print(len(mean_x_value))
print(len(mean_y_value))
# 原始折线图
# plt.plot(x_columns, mean_y_value, color='b', linewidth=3, alpha = 0.5)
# 平滑
x_smooth = np.linspace(x_params_min, x_params_max,300) #300 represents number of points to make between T.min and T.max
y_smooth = make_interp_spline(mean_x_value,mean_y_value)(x_smooth)
plt.plot(x_smooth, y_smooth, color='b', linewidth=3, alpha = 0.5)


# plt.plot(mean_x_value, mean_y_value, color='b', linewidth=3, alpha = 0.5)

plt.xlabel(x_params)
plt.ylabel(y_params)
# plt.xticks(range(timestamp_max))
 
plt.tight_layout()
# plt.legend()
# plt.show()
plt.savefig(result_dir_path + save_file_name)
plt.cla()