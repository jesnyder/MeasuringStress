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


def compile_formatted(format_type):
    """
    collapse the information stored as separate csv into a single csv
    to make the information easier to plot in javascript/html
    also to upload less files to github
    """

    print("begin compile_formatted")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    format_types = retrieve_ref('format_types')

    segment_list = retrieve_ref('segment_list')
    timePreStudy = retrieve_ref('timePreStudy')
    timePostStudy = retrieve_ref('timePostStudy')

    # check each study
    for study in study_list:

        df_meta = retrieve_meta(study)
        recordNames = list(df_meta['recordName'])

        for record in recordNames:

            i = df_meta[ df_meta['recordName']== record].index.values[0]
            print('i = ' + str(i))

            for sensor in sensor_list:

                for segment in segment_list:

                    format_type, segmentRef = 'clean', 'All'
                    source = os.path.join('studies', study, 'formatted', format_type, record, segmentRef, sensor + '.csv')
                    df = pd.read_csv(source)

                    df_segmented = segment_df(segment, df)

                    path = ['studies', study, 'formatted', format_type, record, segment]
                    path = build_path(path)
                    file = os.path.join(path, sensor + ".csv")
                    df_segmented.to_csv(file)
                    print('segmented clean file = ' + str(file))



def segment_df(segment, df):
    """
    Accept a segment and a dataframe
    Trim according to the segment name
    Pass back the trimmed dataframe
    """

    segment_list = retrieve_ref('segment_list')
    timePreStudy = retrieve_ref('timePreStudy')
    timePostStudy = retrieve_ref('timePostStudy')


    if segment == segment_list[0]:
        timeEnd = timePreStudy
        df = df.drop(df[df['timeMinutes'] > timeEnd].index)

    if segment == segment_list[1]:
        timeBegin = timePreStudy
        timeEnd = timePostStudy
        df = df.drop(df[df['timeMinutes'] < timeBegin].index)
        df = df.drop(df[df['timeMinutes'] > timeEnd].index)

    if segment == segment_list[2]:
        timeBegin = timePostStudy
        df = df.drop(df[df['timeMinutes'] < timeBegin].index)

    return(df)
