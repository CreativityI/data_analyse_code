import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
import json


def generate_unique_id(row):
	return row['trip_id'] + '\001' +  str(row['start_time']) + '\001' + str(row['end_time'])

def data_process(file_name, save_file_name,  data_dir_path):
    data_pd = pd.read_csv(data_dir_path + file_name, sep=',')
    
    data_pd['unique_id'] = data_pd.apply(generate_unique_id, axis=1)

    sorted_data_pd = data_pd.groupby(data_pd['unique_id']).apply(lambda x: x.sort_values('timestamp', ascending=True))

    sorted_data_pd = sorted_data_pd.drop('unique_id', axis=1)
    print(data_dir_path+save_file_name)
    sorted_data_pd.to_csv(data_dir_path+save_file_name, sep=',', index=False)




data_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/data/'
result_dir_path = '/Users/didi/Desktop/algorithm/new_data_process/result/'


file_name_1 = 'job_id=76338856aa.csv'
file_name_2 = 'job_id=76338856ab.csv'
file_name_3 = 'job_id=76338856ac.csv'








print(file_name_1)

data_process(file_name_1, 'group_data_human1.csv', data_dir_path )


print(file_name_2)
data_process(file_name_1, 'group_data_human2.csv', data_dir_path )

print(file_name_3)
data_process(file_name_1, 'group_data_human3.csv', data_dir_path )

