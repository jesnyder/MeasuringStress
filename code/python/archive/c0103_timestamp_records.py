from datetime import datetime
from dateutil import tz
import glob
import os
import pandas as pd
import sys
import time



def timestamp_records():
    """

    """

    print("running format_source")

    sensors = ['EDA', 'HR', 'TEMP']

    path_folders = os.path.join('..', '..',  'source_measurements', 'PMR', 'ref' )
    save_file = os.path.join(path_folders, 'source_list_02' + '.csv' )
    df = pd.read_csv(save_file)
    del df['Unnamed: 0']
    print(df)

    timestamped_path = []

    for sensor in sensors:
        for record in df['record']:

            df_record = df[(df['record']==record)]
            print('df_record =')
            print(df_record)
            shared_start = max(list(df_record['starts']))
            shared_end = min(list(df_record['ends']))

            for path in df_record['path_long']:

                wearable = list(df[(df['path_long']==path)]['wearable'])[0]

                source_path = os.path.join(path, sensor + '.csv')

                df_source = pd.read_csv(source_path)
                print('df_source = ')
                print(df_source)
                header = list(df_source.columns.values)[0]
                print('header = ')
                print(header)
                information = list(df_source[header])
                freq = information[0]
                print('frequency = ' + str(freq))
                information = information[1:]

                record_start = float(header)
                record_length = len(information)/freq
                record_end = record_start + record_length
                print('record start = ' + str(record_start) + ' record end = ' + str(record_end) + ' length = ' + str(record_length/60) )

                time_unix = []
                for info in information:
                    time_unix.append(record_start + len(time_unix)/freq)

                df_timestamped = pd.DataFrame()
                df_timestamped[str(str(wearable) + '_time_unix')] = time_unix
                df_timestamped[str(str(wearable) + '_measurements')] = information


                path_folders = os.path.join('..', '..',  'source_measurements', 'PMR', 'timestamped', sensor )
                print('path folders = ' + str(path_folders))
                if not os.path.exists(path_folders):
                    os.mkdir(path_folders)

                save_file = os.path.join(path_folders, str(str(wearable) + ' ' + str(record).zfill(2) + '.csv'))
                # os.mkdir(save_file)
                df_timestamped.to_csv(save_file)

                timestamped_path.append(save_file)




if __name__ == "__main__":
    format_source()
