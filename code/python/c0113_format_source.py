from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary

from c0107_timestamp_source import timestamp_source
from c0107_timestamp_source import build_timestamps



import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def format_source():
    """
    define each record
    set the beginning of the record
    set the end of the record
    record the length of the record
    """

    print("begin format_source")

    # timestamp and save the source measurements
    # no truncation
    # save as their recordName

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    # check each study
    for study in study_list:

        df_meta = retrieve_meta(study)
        print(df_meta)

        recordNames = list(df_meta['recordName'])

        for record in recordNames:

            i = df_meta[ df_meta['recordName']== record].index.values[0]
            recordSource = df_meta.loc[i, 'source_path' ]
            recordBegin = df_meta.loc[i, 'recordBegin' ]
            recordEnd = df_meta.loc[i, 'recordEnd' ]

            print('i = ' + str(i))
            print('record = ' + str(record))
            print('recordSource = ' + str(recordSource))

            for sensor in sensor_list:

                format_type, segment = 'source', 'All'
                source = os.path.join('studies', study, format_type, recordSource, sensor + '.csv')
                df_source = pd.read_csv(source)

                df_timestamped = build_timestamps(df_source, sensor)

                # df_timestamped = df_timestamped[df_timestamped['timeUnix'] > recordBegin]
                # df_timestamped = df_timestamped[df_timestamped['timeUnix'] < recordEnd]

                path = ['studies', study, 'formatted', format_type, record, segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df_timestamped.to_csv(file)
                print('formatted source file = ' + str(file))
