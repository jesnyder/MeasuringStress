from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary

from c0107_timestamp_source import timestamp_source
from c0108_retrieve_analyzed import retrieve_analyzed


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def find_temp_end():
    """
    plot the timestamped data for the temperature
    """

    print("begin find temp end")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    max_record_time = float(retrieve_ref('max_record_time'))
    min_record_time = float(retrieve_ref('min_record_time'))
    trimBegin = float(retrieve_ref('trimBegin'))

    sensor = 'TEMP'
    segment = 'All'
    format_type = 'source'

    for study in study_list:

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])
        recordLength = list(df_meta['recordLength'])

        df_meta['recordEnd'] = [None] * len(source_path)
        df_meta['truncatedLength'] = [None] * len(source_path)


        for record in source_path:

            index = source_path.index(record)
            length = recordLength[index]

            df_timestamped = retrieve_analyzed(study, format_type, record, segment, sensor)
            df_timestamped = df_timestamped.drop(df_timestamped[df_timestamped['timeMinutes'] > max_record_time].index)


            timeUnix = df_timestamped['timeUnix']
            timeMinutes = df_timestamped['timeMinutes']
            measurements = df_timestamped['measurement']

            time_end = find_record_end_from_temp(df_timestamped)

            df_timestamped = df_timestamped.drop(df_timestamped[df_timestamped['timeMinutes'] > time_end].index)
            # df_timestamped = df_timestamped.drop(df_timestamped[df_timestamped['timeMinutes'] < trimBegin].index)

            path = os.path.join(study, 'formatted', 'truncate')
            if not os.path.isdir(path): os.mkdir(path)
            path = os.path.join(study, 'formatted',  'truncate')
            if not os.path.isdir(path): os.mkdir(path)
            path = os.path.join(study, 'formatted',  'truncate', record)
            if not os.path.isdir(path): os.mkdir(path)
            path = os.path.join(study, 'formatted',  'truncate', record, 'All')
            if not os.path.isdir(path): os.mkdir(path)
            path = os.path.join(study, 'formatted',  'truncate', record, sensor + ".csv")
            df_timestamped.to_csv(path)

            truncatedLength = (max(df_timestamped['timeMinutes']))

            i = df_meta[ df_meta['source_path'] == record].index.values[0]
            df_meta.loc[i, 'truncatedLength' ] = round(truncatedLength, 4)
            df_meta.loc[i, 'recordEnd' ] = timeUnix[0]


        save_meta(study, df_meta)
        # record_to_summary(study, 'Record Time - Truncated (minutes)', str(sum(truncatedLength)))
        # record_to_summary(study, 'Record Time - Truncated (hours)', str(sum(truncatedLength)/60))




def find_record_end_from_temp(df_timestamped):
    """
    Find the record end
    by searching for the dip in the temperature
    """

    max_record_time = float(retrieve_ref('max_record_time'))
    min_record_time = float(retrieve_ref('min_record_time'))


    print('df_timestamped = ')
    print(df_timestamped)


    timeUnix = list(df_timestamped['timeUnix'])
    timeMinutes = list(df_timestamped['timeMinutes'])
    measurements = list(df_timestamped['measurement'])


    time_end = max_record_time
    time_end = max(timeMinutes)

    for i in range(len(measurements) - 12):

        """
        print('i = ' + str(i) + ' len(measurements) = ' + str(len(measurements)))
        print('timeMinutes = ')
        print(timeMinutes)
        print('timeMinutes[i] = ' )
        print(str(timeMinutes[i]))
        print('min_record_time + float(timeMinutes[0] = ' + str(min_record_time + float(timeMinutes[0])))
        """

        if timeMinutes[i] > min_record_time + float(timeMinutes[0]):

            # if the temperature drops more than 2 degrees in 3 seconds
            # end the record
            if measurements[i] - 2  > measurements[i+12]:
                # print('measurement[i] &  measurements[i+12] =' + str(measurements[i]), ' & ', str(measurements[i+12]))
                # print('timeMinutes[i] &  timeMinutes[i+12] =' + str(timeMinutes[i]), ' & ', str(timeMinutes[i+12]))
                time_end = timeMinutes[i]
                timeEndUnix = timeUnix[i]
                break

        else:
            time_end = timeMinutes[i]
            timeEndUnix = timeUnix[i]
            break


        time_end = float(time_end)

        print('time_end = ' + str(time_end))
        print('timeEndUnix = ' + str(timeEndUnix))

        return(time_end)
