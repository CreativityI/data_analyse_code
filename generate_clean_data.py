import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
import json


def generate_unique_id(row):
	return row['trip_id'] + '\001' +  str(row['start_time']) + '\001' + str(row['end_time'])

def get_clean_data(data_pd):
    unique_id_list = data_pd['unique_id'].drop_duplicates(keep='first').to_numpy().tolist()
    
    for item_unique_id in unique_id_list:
        
        item_data_pd = data_pd[ data_pd['unique_id'] == item_unique_id ]
        if item_data_pd['distance_to_left_hard_boundary'].isnull().all() and item_data_pd['distance_to_right_hard_boundary'].isnull().all():
            continue
        else:
            return 
    return pd.DataFrame(unique_id_ego_lane_list)

def data_process(file_name, save_file_name,  data_dir_path):
    data_pd = pd.read_csv(data_dir_path + file_name, sep=',')
    
    data_pd['unique_id'] = data_pd.apply(generate_unique_id, axis=1)

    unique_id_list = data_pd['unique_id'].drop_duplicates(keep='first').to_numpy().tolist()
    
    clean_data_list = []
    for item_unique_id in unique_id_list:
        
        item_data_pd = data_pd[ data_pd['unique_id'] == item_unique_id ]
        if item_data_pd['distance_to_left_hard_boundary'].isnull().all() and item_data_pd['distance_to_right_hard_boundary'].isnull().all():
            continue
        else:
             clean_data_list.append(item_data_pd)

            
    clean_pd = pd.concat(clean_data_list, axis=0)

    clean_pd.drop('unique_id', axis=1)
    print(data_dir_path+save_file_name)
    clean_pd.to_csv(data_dir_path+save_file_name, sep=',', index=False)




data_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/data/'
result_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/result/'


file_name_1 = 'job_id=76338856aa.csv'
file_name_2 = 'job_id=76338856ab.csv'
file_name_3 = 'job_id=76338856ac.csv'


print(file_name_1)

data_process(file_name_1, 'clean_human_1.csv', data_dir_path )


print(file_name_2)
data_process(file_name_1, 'clean_human_2.csv', data_dir_path )

print(file_name_3)
data_process(file_name_1, 'clean_human_3.csv', data_dir_path )

