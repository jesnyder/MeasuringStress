from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary





import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def format_truncate():
    """
    define each record
    set the beginning of the record
    set the end of the record
    record the length of the record
    """

    print("begin format_truncate")

    # timestamp and save the source measurements
    # no truncation
    # save as their recordName

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    # check each study
    for study in study_list:

        df_meta = retrieve_meta(study)
        recordNames = list(df_meta['recordName'])

        for record in recordNames:

            i = df_meta[ df_meta['recordName']== record].index.values[0]
            recordBegin = df_meta.loc[i, 'recordBegin' ]
            recordEnd = df_meta.loc[i, 'recordEnd' ]
            print('i = ' + str(i))

            for sensor in sensor_list:

                format_type, segment = 'source', 'All'
                source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                df = pd.read_csv(source)

                df = df[df['timeUnix'] > recordBegin]
                df = df[df['timeUnix'] < recordEnd]

                assert len(list(df['timeUnix'])) > 0, 'during format truncate, dataframe empty'

                format_type, segment = 'truncate', 'All'
                path = ['studies', study, 'formatted', format_type, record, segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df.to_csv(file)
                print('formatted truncated file = ' + str(file))
