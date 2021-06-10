from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_sensor_unit
from c0102_timestamp import timestamp_source
from c0103_trim_record_to_max import trim_record_to_max
from c0104_plot_timestamp import plot_timestamp
from c0105_find_records import find_records
from c0106_record_to_summary import record_to_summary
from c0107_decide_inclusion import decide_inclusion
from c0108_save_meta import save_meta
from c0109_retrieve_meta import retrieve_meta
from c0110_find_temp_end import find_temp_end
from c0111_retrieve_analyzed import retrieve_analyzed
from c0112_plot_truncate import plot_truncate
from c0113_plot_acc import plot_acc

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def find_paired_end():
    """
    Find the end of the paired record
    Add the end of the coregistered record in the meta file
    """

    print("begin find_paired_end")

    study_list = retrieve_ref('study_list')

    format_type = 'truncate'
    sensor = 'TEMP'
    segment = 'All'


    for study in study_list:

        df_meta = retrieve_meta(study)
        # print(df_meta)
        source_path = list(df_meta['source_path'])
        # recordCoregistered = list(df_meta['recordCoregistered'])

        df_meta['recordEnd'] = [None] * len(source_path)


        # there could be two wearables - or one
        # one wearable was turned off before the other
        # check if the participant record has one or two wearables
        # if there are two find the earlier stop time and save to meta file
        for record in source_path:

            # find the max value in the "timeUnix' column of analyzed data"
            df = retrieve_analyzed(study, format_type, record, segment, sensor)
            timeEndRecord = max(list(df['timeUnix']))

            # save that value in the dataframe
            i = df_meta[ df_meta['source_path']== record].index.values[0]
            df_meta.loc[i, 'recordEnd' ] = int(timeEndRecord)


            # print('i = ' + str(i))
            recordCoregistered = df_meta.loc[i, 'recordCoregistered' ]
            # print('recordCoregistered = ')
            # print(recordCoregistered)

            if pd.isnull(df_meta.loc[i , 'recordCoregistered']):
                print('no pair found')

            elif len(df_meta.loc[i , 'recordCoregistered']) > 3 + len(record):

                recordCoregisteredStr = str(df_meta.loc[i , 'recordCoregistered'])
                recordCoregisteredStrList = recordCoregisteredStr.split(' ')
                timeEndRecord = []

                for recordCoregisteredStr in recordCoregisteredStrList:

                    df = retrieve_analyzed(study, analysis_type, recordCoregisteredStr, sensor)
                    timeEndRecord.append(max(list(df['timeUnix'])))

                df_meta.loc[i, 'recordEnd' ] = int(min(timeEndRecord))


        save_meta(study, df_meta)
        print('df_meta = ')
        print(df_meta)
