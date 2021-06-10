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

def find_pairs():
    """
    Pair up records
    Note pairs in the meta file
    """

    print("begin find_pairs")

    study_list = retrieve_ref('study_list')


    for study in study_list:

        df_meta = retrieve_meta(study)
        print(df_meta)
        source_path = list(df_meta['source_path'])

        df_meta['pairedRecord'] = [None] * len(source_path)
        df_meta['recordCoregistered'] = source_path
        df_meta['recordBegin'] = [None] * len(source_path)
        # df_meta['recordEnd'] = [None] * len(source_path)
        df_meta['wearableName'] =  [None] * len(source_path)


        # sort dataframe by the wearable name
        for record in source_path:
            recordList = record.split('_')
            recordWearable = str(recordList[1])
            i = df_meta[ df_meta['source_path']== record].index.values[0]
            df_meta.loc[i, 'wearableName' ] = recordWearable
        df_meta = df_meta.sort_values(by = 'wearableName')



        for recordA in source_path:

            recordAList = recordA.split('_')
            recordABegin = int(recordAList[0])
            recordAWearable = str(recordAList[1])

            # print('recordAList = ')
            # print(recordAList)
            # print('recordABegin = ')
            # print(recordABegin)
            # print('recordAWearable = ')
            # print(recordAWearable)

            recordCoregistered = str(recordA)
            i = df_meta[ df_meta['source_path']== recordA].index.values[0]
            # df_meta.loc[i, 'pairedRecord' ] = str(recordA)
            # df_meta.loc[i, 'recordCoregistered' ] = str(recordCoregistered)
            df_meta.loc[i, 'recordBegin' ] = recordABegin

            recordList = []
            recordList.append(recordA)

            recordBegin = [recordABegin]


            for recordB in source_path:

                recordBList = recordB.split('_')
                recordBBegin = int(recordBList[0])
                recordBWearable = str(recordBList[1])


                if abs(recordABegin - recordBBegin) < 300 and recordAWearable != recordBWearable:

                    # print('pair found: ')

                    # print('recordBList = ')
                    # print(recordBList)
                    # print('recordBBegin = ')
                    # print(recordBBegin)
                    # print('recordBWearable = ')
                    # print(recordBWearable)

                    recordList = list([recordA, recordB])
                    recordBegin = list([recordABegin , recordBBegin])
                    recordWearable = list([recordAWearable , recordBWearable])

                    # print('recordList = ')
                    # print(recordList)
                    # print('recordBegin = ')
                    # print(recordBegin)
                    # print('recordWearable = ')
                    # print(recordWearable)

                    recordBegin = max(recordBegin)

                    recordCoregistered = str(recordA) + ' ' + str(recordB)

                    df_meta.loc[i, 'pairedRecord' ] = str(recordB)
                    df_meta.loc[i, 'recordCoregistered' ] = str(recordCoregistered)
                    df_meta.loc[i, 'recordBegin' ] =  recordBegin


        save_meta(study, df_meta)
        # print('df_meta = ')
        # print(df_meta)

        # drop duplicated entries
        df_meta = df_meta.drop_duplicates('recordBegin', keep='last')
        df_meta = df_meta.sort_values(by = 'recordBegin')
        del df_meta['wearableName']
        save_meta(study, df_meta)
        print('df_meta = ')
        print(df_meta)
