from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary

import math
import numpy as np
import os
import pandas as pd

def timestamp_source(study, format_type, segment, record, sensor):
    """
    Input: path to a csv
    Output: list of timestamps
    """


    # read in the source
    source = os.path.join('studies', study, 'source', record, sensor + '.csv')
    df_source = pd.read_csv(source)
    # print('df_source = ')
    # print(df_source)

    df_timestamped = build_timestamps(df_source, sensor)

    path = ['studies', study, 'formatted', str(format_type), str(record), str(segment)]
    path = build_path(path)
    file = os.path.join(path, sensor + ".csv")

    # print('timestamped_file = ' + str(timestamped_file))
    df_timestamped.to_csv(file)

    # print('timestamped saved: ' + str(file))

    return(df_timestamped)



def build_timestamps(df_source, sensor):
    """
    from the source dataframe
    build the timestamped lists
    """

    # find the beginning time
    timeStart = list(df_source.columns)
    timeStart = float(timeStart[0])
    # print('timeStart = ' + str(timeStart))

    freq = list(df_source.iloc[0])
    freq = float(freq[0])
    # print('freq = ' + str(freq))

    measurementList = list(df_source.iloc[1:,0])
    # print('measurementList = ')
    # print(measurementList)

    # the ACC sensor takes measurements in the x- , y- , and z- axis
    # calculate the magnitude of the acceleration from the three sensors
    if sensor == 'ACC':
        xMeas = list(df_source.iloc[1:,0])
        yMeas = list(df_source.iloc[1:,1])
        zMeas = list(df_source.iloc[1:,2])

        # take absolute value of acceleration
        xMeas = np.abs(xMeas)
        yMeas = np.abs(yMeas)
        zMeas = np.abs(zMeas)

        measurementList = []

        for i in range(len(xMeas)):
            magACCsquared =  math.pow(xMeas[i],2) + math.pow(yMeas[i],2) + math.pow(zMeas[i],2)
            magACC = math.sqrt(magACCsquared)
            measurementList.append(magACC)


    timeUnix, timeMinutes = [], []

    for i in range(len(measurementList)):
        timeLapsed = i/freq
        timeUnix.append(float(round(timeStart + timeLapsed, 3)))
        timeMinutes.append(round(timeLapsed/60, 5 ))


    # builkd dataframe
    df_timestamped = pd.DataFrame()
    df_timestamped['timeUnix'] = timeUnix
    df_timestamped['timeMinutes'] = timeMinutes
    df_timestamped['measurement'] = measurementList


    if sensor == 'ACC':
        df_timestamped['xMeas'] = xMeas
        df_timestamped['yMeas'] = yMeas
        df_timestamped['zMeas'] = zMeas


    return(df_timestamped)
