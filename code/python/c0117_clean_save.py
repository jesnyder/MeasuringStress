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


def clean_save():
    """
    for each record
    break the record into a PreStudy, Study, and PostStudy period
    save each segment as a separate .csv
    """

    print("begin clean_save")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    # check each study
    for study in study_list:

        df_meta = retrieve_meta(study)
        recordNames = list(df_meta['recordName'])

        for record in recordNames:

            i = df_meta[ df_meta['recordName']== record].index.values[0]
            print('i = ' + str(i))

            for sensor in sensor_list:

                format_type, segment = 'coregister', 'All'
                source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                df = pd.read_csv(source)

                df = reset_minutes(segment, df)

                for colName in list(df.head()):
                    if 'Unnamed' in colName:
                        del df[colName]

                format_type = 'clean'
                path = ['studies', study, 'formatted', format_type, record, segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df.to_csv(file)
                print('formatted clean file = ' + str(file))




def reset_minutes(segment, df):
    """
    reset the minutes to be from 0
    """

    segment_list = retrieve_ref('segment_list')
    timePreStudy = retrieve_ref('timePreStudy')
    timePostStudy = retrieve_ref('timePostStudy')


    timeMinutes = []
    timeMinutesOriginal = list(df['timeMinutes'])

    for time in timeMinutesOriginal:

        timeReset = time - timeMinutesOriginal[0]
        timeMinutes.append(timeReset)

    df['timeMinutes'] = timeMinutes

    return(df)
