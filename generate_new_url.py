import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
import json


def generate_unique_id(row):
	return row['trip_id'] + '\001' +  str(row['start_time']) + '\001' + str(row['end_time'])

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
    data_pd = data_pd[['trip_id', 'start_time', 'end_time', 'ego_lane']].drop_duplicates(keep='first')
    data_pd['unique_id'] = data_pd.apply(generate_unique_id, axis=1)
    data_pd['url'] = data_pd.apply(generate_new_url, axis=1)

    unique_id_ego_lane_pd = get_ego_lane_list(data_pd)
    data_pd = data_pd[['trip_id', 'start_time', 'end_time', 'url', 'unique_id']].drop_duplicates(keep='first')
    data_pd = pd.merge( data_pd, unique_id_ego_lane_pd, on=['unique_id'])
    return data_pd[['trip_id', 'start_time', 'end_time', 'url', 'ego_lane']]




data_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/data/'
result_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/result/'

file_name = 'fixed_spots_0906.csv'

file_name_1 = 'job_id=76338856aa.csv'
file_name_2 = 'job_id=76338856ab.csv'
file_name_3 = 'job_id=76338856ac.csv'

save_file_name = 'segment_tirp.csv'

data_pd_1 = pd.read_csv(data_dir_path + file_name_1, sep=',')
data_pd_2 = pd.read_csv(data_dir_path + file_name_2, sep=',')
data_pd_3 = pd.read_csv(data_dir_path + file_name_3, sep=',')


print(file_name_1)

result_data_pd_1 = data_process(data_pd_1)
print(file_name_2)
result_data_pd_2 = data_process(data_pd_2)
print(file_name_3)
result_data_pd_3 = data_process(data_pd_3)


result_data_pd = pd.concat([result_data_pd_1, result_data_pd_2, result_data_pd_3], axis=0)

result_data_pd.to_csv(data_dir_path+save_file_name, sep=',', index=False)