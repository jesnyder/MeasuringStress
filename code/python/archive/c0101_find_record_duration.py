from datetime import datetime
from dateutil import tz
import glob
import os
import pandas as pd
import sys
import time

def find_record_duration():
    """

    """

    print("running find_record_duration")

    path_folders = os.path.join('..', '..',  'source_measurements', 'PMR', 'ref' )
    save_file = os.path.join(path_folders, 'source_list_01' + '.csv' )
    df = pd.read_csv(save_file)
    del df['Unnamed: 0']
    print(df)

    record_begin = []
    record_end = []
    record_duration = []

    for record in df['record']:
        df_record = df[(df['record']==record)]

        starts = []
        ends = []

        for path in df_record['path_long']:
            source_path = os.path.join(path, 'EDA.csv')
            df_source = pd.read_csv(source_path)
            header = list(df_source.columns.values)

            record_start = header[-1]
            print('record start = ' + str(record_start))
            freq = df_source[record_start][0]
            print('frequency = ' + str(freq))
            measurements = df_source[record_start][1:]
            print('measurement number = ' + str(len(measurements)))
            seconds = len(measurements)/freq
            minutes = seconds/60
            print('minutes = ' + str(minutes))
            end = float(record_start) + seconds

            starts.append(float(record_start))
            ends.append(end)

        record_begin.append(max(starts))
        record_end.append(min(ends))
        record_duration.append((min(ends)-max(starts))/60)

    df['starts'] = record_begin
    df['ends'] = record_end
    df['duration'] = record_duration

    print('record_end = ' )
    print(record_end)
    print('len(record_end) = ' + str(len(record_end)))

    del df['begin_unix']
    del df['shared_begin']

    print(df)

    path_folders = os.path.join('..', '..',  'source_measurements', 'PMR', 'ref' )
    if not os.path.isdir(path_folders): os.mkdir(path_folders)

    save_file = os.path.join(path_folders, 'source_list_02' + '.csv' )
    df.to_csv(save_file)

    print("completed find_record_duration")


if __name__ == "__main__":
    find_record_duration()
