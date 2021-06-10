from c0101_retrieve_ref import retrieve_ref
from c0102_timestamp import timestamp_source
from c0103_trim_record_to_max import trim_record_to_max
from c0104_plot_timestamp import plot_timestamp
from c0105_find_records import find_records
from c0106_record_to_summary import record_to_summary
from c0107_decide_inclusion import decide_inclusion
from c0108_save_meta import save_meta
from c0109_retrieve_meta import retrieve_meta
from c0110_find_temp_end import find_temp_end
from c0110_find_temp_end import find_record_end_from_temp
from c0111_retrieve_analyzed import retrieve_analyzed
from c0112_plot_truncate import plot_truncate
from c0113_plot_acc import plot_acc
from c0114_segment_data import segment_data
from c0115_plot_segment import plot_segment
from c0116_find_pairs import find_pairs
from c0117_find_paired_end import find_paired_end
from c0118_find_paired_duration import find_paired_duration


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def multiple_record_check():
    """
    check the record for multiple records
    """

    print("begin multiple record check")


    study_list = retrieve_ref('study_list')
    format_types = retrieve_ref('format_types')
    segment_list = retrieve_ref('segment_list')
    sensor_list = retrieve_ref('sensor_list')

    timePreStudy = retrieve_ref('timePreStudy')
    timePostStudy = retrieve_ref('timePostStudy')

    for study in study_list:

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])
        source_path_new = list(df_meta['source_path'])
        timeBegin_list = list(df_meta['recordBegin'])
        timeEnd_list = list(df_meta['recordEnd'])

        for record in source_path:

            i = df_meta[ df_meta['source_path'] == record].index.values[0]
            fullLength = float(df_meta.loc[i, 'fullLength' ])
            truncatedLength = float(df_meta.loc[i, 'truncatedLength' ])

            format_type = 'source'
            segment = 'All'
            sensor = 'TEMP'
            df =  retrieve_analyzed(study, format_type, record, segment, sensor)

            new_record_list = []

            if fullLength > truncatedLength + 30:

                df = df.drop(df[df['timeMinutes'] < truncatedLength + 5 ].index)

                # print('df = ')
                # print(df)

                timeUnix = list(df['timeUnix'])
                timeMinutes = list(df['timeMinutes'])
                measurements = list(df['measurement'])

                for i in range(len(measurements)):

                    if i < len(measurements) - 30:

                        if measurements[i] + 3 < measurements[i+28]:

                            print('new record found')

                            df = df.drop(df[df['timeMinutes'] < timeMinutes[i+28] ].index)

                            time_end = find_record_end_from_temp(df)
                            print('time_end = ' + str(time_end))

                            df = df.drop(df[df['timeMinutes'] > time_end ].index)


                            # print('df = ')
                            # print(df)

                            wearable_name = record.split('_')
                            wearable_name = wearable_name[1]

                            recordName = str(str(int(timeUnix[0])) + '_' + str(wearable_name))
                            print('recordName = ' + str(recordName))

                            new_record_list.append(recordName)

                            source_path_new.append(record)
                            timeBegin_list.append(int(timeUnix[0]))
                            print('timeUnix[0:20] = ')
                            print(timeUnix[0:20])
                            timeEnd = min(timeUnix)
                            print('timeEnd = ' + str(timeEnd))
                            timeEnd = min(timeUnix) + 60
                            print('timeEnd = ' + str(timeEnd))
                            timeEnd_list.append(int(timeEnd))

                            break



        df_meta_new = pd.DataFrame()
        df_meta_new['source_path'] = source_path_new
        df_meta_new['recordBegin'] = timeBegin_list
        df_meta_new['recordEnd'] = timeEnd_list

        save_meta(study, df_meta_new)
